"""Model evaluation utilities."""
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from pathlib import Path
from .utils import load_joblib




def evaluate_model(model, X_test, y_test):
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
return {"accuracy": acc, "report": report, "confusion_matrix": cm}




if __name__ == "__main__":
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=Path, required=True)
parser.add_argument("--vectorizer", type=Path, required=True)
parser.add_argument("--data", type=Path, required=False)
args = parser.parse_args()


model = load_joblib(args.model)
vec = load_joblib(args.vectorizer)
print("Loaded model and vectorizer. Use evaluate_model(model, X_test, y_test) after transforming test texts.")