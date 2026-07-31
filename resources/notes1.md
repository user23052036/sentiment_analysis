# Notes 1 — Data Loading & Preprocessing

## ML Formulation: Lock X and Y First

Everything downstream depends on this. Getting X or Y wrong invalidates the entire pipeline.

| Variable | Meaning | Column | Raw Values |
|----------|---------|--------|------------|
| **X** | Tweet text (input features) | index 5 — `text of the tweet` | raw strings |
| **Y** | Sentiment polarity (label) | index 0 — `polarity of tweet` | `0` = negative, `4` = positive |

After loading, `y` is remapped: `{0 → 0, 4 → 1}` so labels are standard binary (0/1) for scikit-learn classifiers.

---

## Loading the Dataset

```python
df = pd.read_csv(DATA_PATH, encoding="latin-1")
```

**Why `latin-1` and not `UTF-8`?**
This is old Twitter data. Even without emojis, it contains apostrophes, unusual punctuation, and `@mentions` that can cause `UTF-8` to crash mid-file silently. `latin-1` is the defensive, industry-standard choice for legacy Twitter CSVs.

**Why `header=None`?**
LibreOffice auto-generates column headers for display only. The actual CSV has no header row — row 0 is data. Without `header=None`, pandas treats the first tweet as the column names and silently drops it.

**Why `names=columns`?**
Assigns readable names so you can write `df["text"]` and `df["polarity"]` instead of `df[5]` and `df[0]`. Essential for maintainable code and exam readability.

**Why `y.map({0: 0, 4: 1})`?**
Logistic Regression outputs probabilities for class `1`. All sklearn metrics (accuracy, precision, recall) assume binary labels `{0, 1}`. Keeping `4` breaks probability interpretation and scoring.

---

## Data Cleaning

```python
def clean_tweet(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)      # remove URLs
    text = re.sub(r"@\w+", "", text)         # remove @mentions
    text = re.sub(r"[^a-z\s]", "", text)     # keep only letters + spaces
    text = re.sub(r"\s+", " ", text).strip() # collapse whitespace
    return text

df["clean_text"] = df["text of the tweet"].apply(clean_tweet)
```

Each step removes noise that has no semantic value for sentiment classification. After this, `df["clean_text"]` contains lowercase, alphanumeric-only tweet text.

---

## Tokenization with NLTK Punkt

**What is Punkt?**
A statistical sentence/word boundary detection model. It knows that `Dr.` and `U.S.` are not sentence endings, while `Hello!` is.

**Why not `text.split(".")`?**
Naive splitting breaks on abbreviations (`Dr.`, `Mr.`), numbers (`3.14`), URLs, and ellipses. Punkt uses learned patterns from real text to tokenize correctly.

**Project-local NLTK setup:**
```python
PROJECT_ROOT = os.path.abspath("..")          # go one level up from /src to /sentiment_analysis
NLTK_DATA_DIR = os.path.join(PROJECT_ROOT, "nltk_data")  # store data inside the project
nltk.data.path.insert(0, NLTK_DATA_DIR)       # highest priority — checked before system paths
```

This makes the project self-contained. `os.path.join` handles `/` vs `\` across operating systems.

---

## Stopword Removal

```python
stop_words = set(stopwords.words("english"))
df["tokens_nostop"] = df["tokens"].apply(
    lambda tokens: [w for w in tokens if w not in stop_words]
)
```

Removes high-frequency, low-information words (`the`, `is`, `and`, `I`, pronouns, verbs like `am`). These appear in almost every tweet regardless of sentiment, so they would dilute features. TF-IDF also handles this via IDF weighting, but explicit removal reduces vocabulary size and speeds up vectorization.

---

## Pipeline State After Preprocessing

```
df["text"]   →  raw tweet string
df["clean_text"]          →  lowercased, URLs/mentions/punctuation removed
df["tokens"]              →  list of word tokens
df["tokens_nostop"]       →  tokens with stopwords removed
```