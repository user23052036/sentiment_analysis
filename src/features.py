"""Vectorizer creation / persistence and feature extraction."""
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
from .config import MAX_FEATURES
from .utils import save_joblib




def build_vectorizer(max_features: int = MAX_FEATURES) -> TfidfVectorizer:
vec = TfidfVectorizer(stop_words="english", max_features=max_features)
return vec




def fit_vectorizer(vectorizer: TfidfVectorizer, texts, save_to: Path = None):
X = vectorizer.fit_transform(texts)
if save_to is not None:
save_joblib(vectorizer, save_to)
return X




def transform_with_vectorizer(vectorizer, texts):
return vectorizer.transform(texts)