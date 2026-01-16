"""Small CLI to train + evaluate with one command."""
from pathlib import Path
from .train import train
from .evaluate import evaluate_model
from .utils import load_joblib




def run_all(data_path: Path, model_dir: Path):
model, vectorizer, (X_test, y_test) = train(data_path, model_dir)
metrics = evaluate_model(model, X_test, y_test)
print("Accuracy:", metrics["accuracy"])
print(metrics["report"])
print("Confusion matrix:\n", metrics["confusion_matrix"])




if __name__ == "__main__":
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--data", type=Path, default=None)
parser.add_argument("--model-dir", type=Path, default=None)
args = parser.parse_args()


data_path = args.data or Path("../data/raw/training.1600000.processed.noemoticon.csv")
model_dir = args.model_dir or Path("../models")
run_all(data_path, model_dir)