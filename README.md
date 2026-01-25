# SENTIMENT_ANALYSIS — README

## Project summary

A compact end-to-end sentiment analysis pipeline for tweets built with classical NLP and scikit-learn.
It ingests the Sentiment140 training CSV (`training.1600000.processed.noemoticon.csv`), cleans and tokenizes tweets, removes stopwords, vectorizes with TF-IDF, trains a `LogisticRegression` classifier and persists both vectorizer and model as `.joblib` files.

This README explains the code, how to run it, minimal fixes to make it robust, and a critical review (assumptions, failure modes, tradeoffs, and prioritized improvements).

---

# 1 — Repository layout (what I see in your screenshot)

```
SENTIMENT_ANALYSIS/
├─ data/
│  ├─ raw/
│  │  └─ training.1600000.processed.noemoticon.csv
│  └─ manual_test/
├─ models/
│  ├─ logistic_regression.joblib
│  └─ tfidf_vectorizer.joblib
├─ nltk_data/
├─ notebook/
│  └─ _load_data.ipynb
├─ resources/
│  ├─ important_git_flow.md
│  └─ notes*.md
├─ src/
├─ venv/
├─ README.md        <- you will replace this
├─ requirements.txt
└─ .gitignore
```

Use this README as your canonical on-boarding doc for new contributors.

---

# 2 — Quick start (run this first)

1. Clone repo

```bash
git clone <repo-url>
cd SENTIMENT_ANALYSIS
```

2. Create and activate Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

*(If you don't have `requirements.txt`, install the essentials: `pandas scikit-learn joblib nltk matplotlib`.)*

4. Prepare NLTK data (one-time)

```bash
python -m nltk.downloader punkt stopwords -d ./nltk_data
```

This puts required NLTK artifacts under the repo's `nltk_data` folder so code finds them without system installs.

5. Run training notebook or script

* If you use the notebook: open `notebook/_load_data.ipynb` in Jupyter and run cells.
* If you extract the code to `src/train.py` (recommended), run:

```bash
python src/train.py --data data/raw/training.1600000.processed.noemoticon.csv
```

---

# 3 — Files of interest & purpose

* `data/raw/...csv` — raw Sentiment140 CSV (1.6M tweets).
* `notebook/_load_data.ipynb` — interactive exploration / training flow.
* `src/` — place for cleaned scripts (train/eval/infer). Currently empty in screenshot — move stable code here.
* `models/` — saved artifacts (tfidf vectorizer, logistic regression model).
* `nltk_data/` — local NLTK tokenizers & corpora to avoid runtime downloads.
* `requirements.txt` — pin versions for reproducibility.

---

# 4 — How the pipeline works (high-level)

1. Read CSV (encoding `latin-1` because of emojis/non-UTF chars).
2. Clean text: lowercase, remove URLs, mentions, non-letter chars, extra whitespace.
3. Tokenize (`nltk.word_tokenize`), remove stopwords.
4. Convert token lists back to strings for `TfidfVectorizer`.
5. Vectorize (TF-IDF, `max_features=15000`).
6. Train `LogisticRegression(max_iter=1300, class_weight='balanced')`.
7. Save `vectorizer.joblib` and `logistic_regression.joblib`.
8. Evaluate with accuracy, classification report, confusion matrix and plot.

---

