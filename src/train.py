"""Training entrypoint. Produces saved model and vectorizer files."""
import argparse
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from .config import MODEL_DIR, RANDOM_STATE, TEST_SIZE, LOGREG_MAX_ITER
from .data_loader import load_and_prepare
from .features import build_vectorizer, fit_vectorizer
from .utils import ensure_dir, save_joblib, setup_nltk, logger




def train(data_path: Path, model_dir: Path):
setup_nltk(str(model_dir.parents[0] / "nltk_data"))
ensure_dir(model_dir)


X_texts, y, df = load_and_prepare(data_path)


vectorizer = build_vectorizer()
X = fit_vectorizer(vectorizer, X_texts)


X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)


logger.info(f"X_train shape: {X_train.shape}")


model = LogisticRegression(max_iter=LOGREG_MAX_ITER, n_jobs=-1)
model.fit(X_train, y_train)


# Save artifacts
save_joblib(vectorizer, model_dir / "tfidf_vectorizer.joblib")
save_joblib(model, model_dir / "logistic_regression.joblib")


logger.info("Model training complete")


# Return objects for immediate evaluation if caller wants
return model, vectorizer, (X_test, y_test)




if __name__ == "__main__":
parser = argparse.ArgumentParser()
parser.add_argument("--data", type=Path, default=None)
parser.add_argument("--model-dir", type=Path, default=MODEL_DIR)
args = parser.parse_args()


data_path = args.data or Path("../data/raw/training.1600000.processed.noemoticon.csv")
train(data_path, args.model_dir)