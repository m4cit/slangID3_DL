from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import torch

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

# loading data
data = pd.read_csv (r'./classifiers/modifiers/data/processed_data.csv')

# train test split ###########################################################################
train, test = train_test_split(data, test_size=0.1, random_state=42)
X_train = [x for x in train['phrase']]
y_train = [x for x in train['type']]
X_test = [x for x in test['phrase']]
y_test = [x for x in test['type']]

org_X_train = X_train
org_X_test = X_test
org_y_train = y_train
org_y_test = y_test
##############################################################################################

# vectorize data #############################################################################
vectorizer = TfidfVectorizer(dtype='float64', min_df=1)
le = LabelEncoder()

X_train = vectorizer.fit_transform(X_train).toarray()
y_train = le.fit_transform(y_train)
y_train = np.array(y_train, dtype=np.int64)

X_test = vectorizer.transform(X_test).toarray()
y_test = le.transform(y_test)
y_test = np.array(y_test, dtype=np.int64)

# print(y_train) -> shows the encoded labels. 1 for slang, 0 for formal.
# print(le.inverse_transform([0])) -> 'formal'
# print(le.inverse_transform(y_train)) -> shows the decoded labels.
##############################################################################################

# convert train and test to tensors ##########################################################
X_train_tensor = torch.from_numpy(X_train).to(device)
X_test_tensor = torch.from_numpy(X_test).to(device)

y_train_tensor = torch.from_numpy(y_train).to(device)
y_test_tensor = torch.from_numpy(y_test).to(device)
X_train_tensor.dtype, y_train_tensor.dtype
##############################################################################################

