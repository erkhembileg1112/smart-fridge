import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import datetime

df = pd.read_csv("inventory.csv")

today = datetime.date.today()

def days_left(date):
    exp_date = pd.to_datetime(date).date()
    return (exp_date - today).days

df["DaysLeft"] = df["Expiration"].apply(days_left)

def label_status(days):
    if days < 0:
        return "Expired"
    elif days <= 2:
        return "Expiring Soon"
    else:
        return "Fresh"

df["Label"] = df["DaysLeft"].apply(label_status)

le = LabelEncoder()
df["CategoryEncoded"] = le.fit_transform(df["Category"])

X = df[["DaysLeft", "CategoryEncoded"]]
y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

joblib.dump(model, "food_model.pkl")
joblib.dump(le, "encoder.pkl")