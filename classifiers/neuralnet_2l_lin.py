from .modifiers.splitting import org_X_test, org_y_test
from .modifiers.splitting import X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor
from .modifiers.splitting import vectorizer
from torcheval.metrics.functional import binary_f1_score
import torch
from torch import nn
from torch.nn import functional as F
from tqdm import tqdm


if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"


input_features = len(X_train_tensor[1]) # for input in model
output_size = 2 # formal or slang
hidden_size = 50 # hidden layers
epochs = 30

##############################################################################################
class NeuralNet_2l_lin(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = nn.Linear(in_features=input_features, out_features=hidden_size)
        self.layer_2 = nn.Linear(in_features=hidden_size, out_features=output_size)
    # forward pass method
    def forward(self, x):
        x = self.layer_2(self.layer_1(x)) # x -> layer_1 -> layer_2 -> output
        return F.softmax(x,dim=1)
##############################################################################################

model = NeuralNet_2l_lin().to(device).double()

# loss function and optimizer ################################################################
loss_fn = nn.NLLLoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=0.01) # learning rate
##############################################################################################

# function to train the model ################################################################
def train_nn_2l_lin():
    model.train()
    message = 'Training NeuralNet_2l_lin model...'
    print(message)
    progressbar = tqdm(total=epochs)
    
    for epoch in range(epochs):
        y_pred = model(X_train_tensor)
        loss = loss_fn(y_pred, y_train_tensor)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        progressbar.update()
    
    # saving trained classifier
    with open('./classifiers/models/NeuralNet_2l_lin.pt', 'wb') as f:
        torch.save(model, f)
    progressbar.close()
    message2 = 'NeuralNet_2l_lin model trained and saved.\n'
    print(f'\n{message2}')   
    return message2
##############################################################################################

# print out test set with predictions and actual labels ######################################
def dm_nn_2l_lin():
    # loading pre-trained classifier
    try:
        model = torch.load('./classifiers/models/NeuralNet_2l_lin.pt')
        model.to(device)
        model.eval()
        y_pred = model(X_test_tensor)
        count = 0
        
        # print out test set with predictions and actual labels
        pred_list = []
        for i in range(len(y_pred)):
            orgPhrase = f'[{i+1}] Phrase: {org_X_test[i]}'
            pred_list.append(orgPhrase)
            print(orgPhrase)
            if torch.argmax(y_pred[i]).item() == 1:
                pr = "slang"
                if pr != str(org_y_test[i]):
                    count += 1
            else:
                pr = "formal"
                if pr != str(org_y_test[i]):
                    count += 1
            prediction = f' |--Prediction: {pr}'
            actual = f' |--Actual:\t{org_y_test[i]}\n'
            pred_list.append(prediction)
            pred_list.append(actual)
            print(prediction)
            print(actual)
        errors = f'Wrong predictions: {count}'    
        # f1 score #####
        pred_list_f1 = [torch.argmax(i) for i in y_pred]
        f1 = binary_f1_score(torch.tensor(pred_list_f1).cpu(), y_test_tensor.cpu(), threshold=0.5)
        f1_score = f'F1 score: {f1}'
        f1_and_pred_list = ['NeuralNet_2l_lin:', f'*{f1_score}', f'*{errors}', '']
        ################
        # pred_list.append(errors)
        print(errors)
        print(f1_score)
        # f1 score and predictions in a list to print in GUI
        for i in pred_list:
            f1_and_pred_list.append(i)
        f1_and_pred_list.append('\n')
        return f1_and_pred_list
    except FileNotFoundError:
        print("Please train the model(s) first!")
##############################################################################################

############# following functions to predict the input phrase ##############
def predictor_nn_2l_lin(input):
    try:
        # loading pre-trained classifier
        model = torch.load('./classifiers/models/NeuralNet_2l_lin.pt')
        model.to(device)
        model.eval()
        input_phrase = vectorizer.transform(input).toarray()
        words = input[0].split(' ')
        words_vect = vectorizer.transform(words).toarray()
        # to tensor
        torch.from_numpy(input_phrase).float()
        torch.from_numpy(words_vect).float()
        # evaluation
        preds = []
        preds.append(f'NeuralNet_2l_lin:\n Phrase:\t         {input[0]}')
        with torch.inference_mode():
            type_prediction = model(torch.from_numpy(input_phrase).to(device))
        if torch.argmax(type_prediction).item() == 1:
            pred = ' |--Prediction:  slang\n |'
        elif torch.argmax(type_prediction).item() == 0:
            pred = ' |--Prediction:  formal\n |'
        preds.append(pred)
        # individual word eval
        for i in range(len(words)):
            type_prediction_word = model(torch.from_numpy(words_vect).to(device))
            if torch.argmax(type_prediction_word[i]).item() == 1:
                w_pred = '\n Prediction:  slang'
                clean = words[i].replace('\n','')
                preds.append(f'\n [{i+1}] Word:    {clean}   {w_pred}')
            elif torch.argmax(type_prediction_word[i]).item() == 0:
                w_pred = '\n Prediction:  formal'
                clean = words[i].replace('\n','')
                preds.append(f'\n [{i+1}] Word:    {clean}   {w_pred}')
        preds.append('\n\n')
        return preds
    except FileNotFoundError:
        print("Please train the model(s) first!")
##############################################################################################

