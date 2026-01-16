"""Loading raw CSV and producing cleaned DataFrame and labels."""
from pathlib import Path
import pandas as pd
from typing import Tuple
from .preprocess import clean_tweet, tokenize, remove_stopwords
from .config import DEFAULT_DATA_PATH
from .utils import ensure_dir




COLUMNS = ["polarity", "id", "date", "query", "user", "text"]




def load_data(path: Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
path = Path(path)
if not path.exists():
raise FileNotFoundError(f"Data file not found: {path}")


# Read without assuming a header. The dataset sometimes has no header row.
df = pd.read_csv(path, header=None, encoding="latin-1", names=COLUMNS, low_memory=False)


# If the first row contains header-like strings (rare), drop it.
try:
# Keep rows where polarity parses as integer-like values
mask = df["polarity"].apply(lambda x: str(x).strip().lstrip("+-").isdigit())
if not mask.any():
raise ValueError("No numeric polarity values found")
if not mask.iloc[0]:
df = df[mask].copy()
df["polarity"] = df["polarity"].astype(int)
except Exception:
# fallback: coerce to numeric and drop NA rows
df["polarity"] = pd.to_numeric(df["polarity"], errors="coerce")
df = df.dropna(subset=["polarity"]).copy()
df["polarity"] = df["polarity"].astype(int)


# Standardize polarity (0->0, 4->1). If other labels appear, map them to 0/1 conservatively.
df = df[df["polarity"].isin([0, 4])].copy()
df["label"] = df["polarity"].map({0: 0, 4: 1})


# Add cleaned text column
df["clean_text"] = df["text"].apply(clean_tweet)


return df




def load_and_prepare(path: Path = DEFAULT_DATA_PATH) -> Tuple[pd.Series, pd.Series, pd.DataFrame]:
df = load_data(path)
X_series = df["clean_text"].astype(str)
y_series = df["label"].astype(int)
return X_series, y_series, df