
## Decide What X and Y Are

Before writing code, we must **lock the ML formulation**.

### Why this step matters

If X and Y are wrong, everything else becomes wrong.
This is another **viva / exam favorite** question.

---

## Define X and Y (VERY IMPORTANT)

### 🟦 X (Input / Features)

* **Tweet text**
* Comes from **column index 5**
* This will later be converted into **TF-IDF numbers**

Conceptually:

```
X = tweet text
```

---

### 🟥 Y (Output / Labels)

* **Sentiment (polarity)**
* Comes from **column index 0**
* Values:

  * `0 → negative`
  * `4 → positive`

Conceptually:

```
Y = sentiment label
```
---
Excellent questions. You’re thinking **correctly**, not blindly following — that’s exactly how this should be learned.
I’ll answer **only what you asked**, step by step, no extra hints.

---

## “This dataset has no emojis, so can I use UTF-8?”

### Short answer

**You *can* use UTF-8, but Latin-1 is safer.**

### Why?

* This dataset is called **`noemoticon`**, not “no special characters”
* It still contains:

  * `@mentions`
  * URLs
  * apostrophes
  * unusual punctuation
* Pandas with UTF-8 **sometimes crashes mid-file**, not at the top

📌 **Rule of thumb (industry + academia):**
If a text dataset is old Twitter data → use `latin-1`.

If you use UTF-8 and it works → fine.
If it crashes later → switch back.

✅ So your thinking is valid, but `latin-1` is defensive, not random.

---

## “Why `header=None` when I clearly see a header row?”


### What you are seeing in LibreOffice is **NOT a real header**
LibreOffice **auto-generates headers** for readability.

📌 In the actual CSV file:

* The **first row is data**, not column names
* Kaggle version of Sentiment140 **does not store headers**

If you do this:

```python
pd.read_csv(file_path)
```

Pandas will think:

```
row 0 = header
```

and you will **lose the first tweet** silently.

### That’s why we do:

```python
header=None
```

This tells pandas:

> “Do not assume any row is a header.”

---

## “Then what does `names=columns` do?”

> “The file has no headers, so I am assigning my own.”

So now you can safely do:

```python
df["text"]
df["polarity"]
```

Without `names=columns`, you’d be stuck with:

```python
df[0], df[1], df[5]
```

Which is:

* unreadable
* error-prone
* bad for exams

---

## “I don’t understand `y.map({0:0, 4:1})`”

## 🧠 Exam-ready explanation (memorize this)

> “Tweet text is used as input features X.
> Polarity column is used as output labels Y.
> We map polarity 0 to negative (0) and 4 to positive (1).”


📌 Why not keep 4?
Because:

* Logistic Regression outputs probabilities of class **1**
* Accuracy, precision, recall assume binary labels
* Keeping `4` breaks interpretation

---
