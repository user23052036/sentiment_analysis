"""Utility helpers: filesystem, NLTK setup, model persistence, logging."""
import logging
from pathlib import Path
import joblib
import os
import nltk


logger = logging.getLogger("sentiment")
logger.setLevel(logging.INFO)
if not logger.handlers:
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(ch)




def ensure_dir(path: Path):
path = Path(path)
path.mkdir(parents=True, exist_ok=True)
return path




def setup_nltk(nltk_data_dir: str):
"""Ensure required NLTK resources exist; download if missing."""
nltk_data_dir = Path(nltk_data_dir)
ensure_dir(nltk_data_dir)
nltk.data.path.insert(0, str(nltk_data_dir))


resources = [
("tokenizers/punkt", "punkt"),
("corpora/stopwords", "stopwords"),
]


for path, name in resources:
try:
nltk.data.find(path)
logger.info(f"NLTK resource found: {name}")
except LookupError:
logger.info(f"Downloading NLTK resource: {name} -> {nltk_data_dir}")
nltk.download(name, download_dir=str(nltk_data_dir))




def save_joblib(obj, path: Path):
ensure_dir(path.parent)
joblib.dump(obj, str(path))
logger.info(f"Saved: {path}")




def load_joblib(path: Path):
return joblib.load(str(path))