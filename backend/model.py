import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# Better dataset (more examples)
data = [
    [20,1,0,2,0,0,0,0,0],
    [150,0,1,5,1,1,2,1,1],
    [80,1,0,3,0,0,1,0,0],
    [200,0,1,6,1,1,3,1,1],
    [60,1,0,2,0,0,0,0,0],
    [10,1,0,1,0,0,0,0,0],
    [180,0,1,7,1,1,4,1,1],
    [45,1,0,2,0,0,0,0,0],
    [130,0,1,5,1,1,3,1,1],
    [25,1,0,1,0,0,0,0,0],
    [220,0,1,6,1,1,3,1,1],
[35,1,0,1,0,0,0,0,0],
[170,0,1,5,1,1,2,1,1],
]

columns = [
    'url_length','has_https','has_at_symbol','num_dots',
    'has_suspicious_word','has_ip','num_hyphens','long_url','label'
]

df = pd.DataFrame(data, columns=columns)

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained successfully")