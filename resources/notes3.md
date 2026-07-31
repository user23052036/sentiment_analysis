# Notes 3 — Datasets, Model Training & Evaluation

## Dataset Map

There are four datasets in this project. They are **not interchangeable**.

| Dataset | Labels | Compatible? | Role |
|---------|--------|-------------|------|
| `training.1600000.processed.noemoticon.csv` | Binary (0/4) | ✅ | Primary training data |
| `testdata.manual.2009.06.14.csv` | Binary (0/4) | ✅ | Final held-out evaluation set |
| `sentiment_analysis_data/test.csv` | 3-class (pos/neg/neutral) | ❌ | Not compatible — different label scheme |
| `sentiment_analysis_data/train.csv` | None (unlabelled) | ❌ for training | Use for inference/prediction only |

**Do not mix the Kaggle `test.csv` (3-class) with the binary model.** Forcing `neutral → 0 or 1` changes the distribution and invalidates evaluation metrics. That is scope creep for this assignment.

---

## Correct Academic Pipeline

```
Train    →  training.1600000.processed.noemoticon.csv  (80/20 internal split)
Validate →  X_test, y_test  (the 20% held-out split)
Final eval → testdata.manual.2009.06.14.csv
Inference  → sentiment_analysis_data/train.csv  (unlabelled, predict only)
```

---

## Train/Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,    # 80% train, 20% test
    random_state=42,  # reproducibility
    stratify=y        # preserve class balance in both splits
)
```

`stratify=y` ensures the 80/20 split maintains the same positive/negative ratio as the full dataset. Without it, random sampling could skew one split toward a class.

---

## Model: Logistic Regression

```python
model = LogisticRegression(max_iter=1300, class_weight="balanced")
model.fit(X_train, y_train)
```

**Why Logistic Regression?**
- TF-IDF vectors are high-dimensional and sparse — logistic regression handles this well because it's a linear model and doesn't need dense inputs
- Binary sentiment (`0`/`1`) is the exact use case logistic regression is designed for
- Interpretable, fast, textbook-standard — appropriate for academic submissions and interviews
- `class_weight="balanced"` adjusts for any minor class imbalance automatically

**Why `max_iter=1300`?**
Logistic Regression uses an iterative solver (LBFGS by default). On a 1.6M dataset with 15k features, the default 100 iterations is insufficient for convergence. 1300 gives the solver enough steps to find the optimal weights.

---

## Saving the Model

```python
from joblib import dump
dump(vectorizer, MODEL_DIR / "tfidf_vectorizer.joblib", compress=3)
dump(model, MODEL_DIR / "logistic_regression.joblib", compress=3)
```

Both the **vectorizer and model** must be saved. The vectorizer holds the vocabulary and IDF weights learned from training data. At inference time, new text must be transformed using the *same* vectorizer, not a newly fitted one.

---

## Evaluation

```python
y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
```

### Metrics to Know for Interviews

| Metric | Formula | What it tells you |
|--------|---------|-------------------|
| **Accuracy** | correct / total | Overall correctness — misleading on imbalanced data |
| **Precision** | TP / (TP + FP) | Of all predicted positives, how many were actually positive |
| **Recall** | TP / (TP + FN) | Of all actual positives, how many did the model catch |
| **F1-Score** | 2 × (P × R) / (P + R) | Harmonic mean of precision and recall — best single metric for binary classification |

### Confusion Matrix Layout

```
                 Predicted 0    Predicted 1
Actual 0    [  True Neg  ,   False Pos  ]
Actual 1    [ False Neg  ,   True Pos   ]
```

`normalize="true"` in `ConfusionMatrixDisplay` normalizes each row by actual class count, showing recall per class rather than raw counts — more informative on large datasets.

---

## Complete Pipeline Summary

```
raw CSV
  ↓  pd.read_csv (latin-1, header=None)
X = df["text of the tweet"],  Y = df["polarity of tweet"]
  ↓  y.map({0:0, 4:1})
  ↓  clean_tweet()         → df["clean_text"]
  ↓  word_tokenize()       → df["tokens"]
  ↓  remove stopwords      → df["tokens_nostop"]
  ↓  " ".join()            → df["tokens_nostop_str"]
  ↓  TfidfVectorizer()     → X (sparse matrix, shape: n_tweets × 15000)
  ↓  train_test_split()    → X_train, X_test, y_train, y_test
  ↓  LogisticRegression.fit(X_train, y_train)
  ↓  model.predict(X_test) → y_pred
  ↓  accuracy_score, classification_report, confusion_matrix
```