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

# vectorize data #############################################################################
vectorizer = TfidfVectorizer(dtype='float64', min_df=1)
X = vectorizer.fit_transform(data['phrase']).toarray()
le = LabelEncoder()
y = le.fit_transform(data['type'])
y = np.array(y, dtype=np.int64)

# print(y) -> shows the encoded labels. 1 for slang, 0 for formal.
# print(le.inverse_transform([0])) -> 'formal'
# print(le.inverse_transform(y)) -> shows the decoded labels.
##############################################################################################

# train test split ###########################################################################
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# second split of unvectorized data to print out the phrases
train, test = train_test_split(data, test_size=0.1, random_state=42)
org_X_train = [x for x in train['phrase']]
org_X_test = [x for x in test['phrase']]
org_y_train = [x for x in train['type']]
org_y_test = [x for x in test['type']]
##############################################################################################

# convert train and test to tensors ##########################################################
X_train_tensor = torch.from_numpy(X_train).to(device)
X_test_tensor = torch.from_numpy(X_test).to(device)

y_train_tensor = torch.from_numpy(y_train).to(device)
y_test_tensor = torch.from_numpy(y_test).to(device)
X_train_tensor.dtype, y_train_tensor.dtype
##############################################################################################

