# Import the necessary libraries and modules
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from joblib import dump

dataset = pd.read_csv("../../Data/NF-CSE-CIC-IDS2018.csv")
train = dataset
print(train.head)
train = train.drop(['Attack'],axis=1)
print(train.head)
# Load the training and test data into Pandas DataFrames
df_train = dataset
df_test = train

# Extract the relevant features and labels from the training and test data
X_train = df_train[["OUT_BYTES", "PROTOCOL"]]
y_train = df_train["Label"]
X_test = df_test[["OUT_BYTES", "PROTOCOL"]]
y_test = df_test["Label"]

# Fit a Random Forest classifier to the training data
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Evaluate the model's performance on the test data
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the model as a pickle file
dump(clf, "../Data/classifier.pkl")