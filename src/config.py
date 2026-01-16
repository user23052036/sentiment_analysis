"""Project configuration constants."""
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw"
DEFAULT_DATA_PATH = DATA_DIR / "training.1600000.processed.noemoticon.csv"


MODEL_DIR = PROJECT_ROOT / "models"
NLTK_DATA_DIR = PROJECT_ROOT / "nltk_data"


# Training / model params
RANDOM_STATE = 42
TEST_SIZE = 0.2
MAX_FEATURES = 15000
LOGREG_MAX_ITER = 1300


# Ensure model dir exists at import time is avoided here; utils will create it when needed.