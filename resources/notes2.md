# Notes 2 — TF-IDF Vectorization

## Core Problem

ML models cannot process raw text. Every tweet must be converted into a **fixed-length numeric vector**. TF-IDF does this while preserving semantic weight — words that matter more get higher values.

---

## Input → Output

```python
df["tokens_nostop_str"] = df["tokens_nostop"].apply(lambda x: " ".join(x))

vectorizer = TfidfVectorizer(max_features=15000)
X = vectorizer.fit_transform(df["tokens_nostop_str"])
# X.shape → (1048572, 15000)
```

- **Rows** = tweets (1,048,572)
- **Columns** = unique words in vocabulary (15,000)
- **Cell value** = TF-IDF score for that word in that tweet

---

## Step-by-Step: What TF-IDF Does

### Step 1 — Vocabulary Creation
Scans all tweets and builds a dictionary of unique words:

```
love    → column 0
hate    → column 1
machine → column 2
learning→ column 3
boring  → column 4
```

`max_features=15000` keeps only the top 15,000 most informative words. This controls memory, speeds up training, and reduces overfitting from rare noise words.

---

### Step 2 — TF (Term Frequency)

> "How important is this word *within this tweet*?"

```
TF(word, tweet) = count of word in tweet / total words in tweet
```

**Example** — tweet: `"machine learning machine"`
- TF(machine) = 2/3 = 0.67
- TF(learning) = 1/3 = 0.33

---

### Step 3 — IDF (Inverse Document Frequency)

> "How rare is this word *across all tweets*?"

```
IDF(word) = log( total tweets / tweets containing that word )
```

- **Rare word** → high IDF → high final score
- **Common word** (`the`, `is`, `and`) → low IDF → nearly zero final score

This is why TF-IDF automatically down-weights useless words.

---

### Step 4 — TF-IDF Score

```
TF-IDF(word, tweet) = TF × IDF
```

Each tweet becomes a sparse vector:

```
"i love machine learning"
→ [love=0.31, machine=0.52, learning=0.52, hate=0.0, boring=0.0, ...]
```

Most values are `0.0` (word not present in that tweet) — this is why `X` is a **sparse matrix**, which uses far less memory than a dense array.

---

## Key Parameters

| Parameter | Value | Effect |
|-----------|-------|--------|
| `max_features` | 15000 | Limits vocabulary to top 15k words — controls memory and reduces noise |
| `stop_words="english"` | *(optional)* | Skips common English words during vectorization, making manual stopword removal redundant |

In this project, stopwords were removed manually before TF-IDF, so `stop_words` is not passed to the vectorizer. Either approach is valid; doing both is redundant but harmless.

---

## Why X is a Sparse Matrix

With 1M+ tweets and 15k vocabulary columns, a dense matrix would be ~1M × 15k × 8 bytes ≈ **120 GB**. Since most words don't appear in most tweets, over 99% of values are zero. A sparse matrix stores only the non-zero values, making this tractable in RAM.

```python
print(type(X))          # scipy.sparse.csr_matrix
print(X.nnz / (X.shape[0] * X.shape[1]))  # sparsity ratio — typically ~0.001
```

---

## Pipeline State After TF-IDF

```
df["tokens_nostop_str"]  →  space-joined cleaned tokens (string)
X                         →  TF-IDF sparse matrix, shape (n_tweets, 15000)
y                         →  binary sentiment labels (0 or 1)
```

`X` and `y` are now ready for model training.