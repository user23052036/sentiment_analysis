Yes, exactly. This is a very common point of confusion.

`stratify=y` **does not fix class imbalance**. It **preserves** whatever class distribution your original dataset has in both the training and test sets.

### Without `stratify`

Suppose your dataset has:

| Class | Count |
| ----- | ----: |
| 0     |   900 |
| 1     |   100 |

(90% class 0, 10% class 1)

If you do:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

the split is random. You might get something like:

Training:

* Class 0: 725
* Class 1: 75

Test:

* Class 0: 175
* Class 1: 25

or you might get:

Training:

* Class 0: 730
* Class 1: 70

Test:

* Class 0: 170
* Class 1: 30

The proportions can drift, especially for smaller datasets.

---

### With `stratify=y`

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)
```

The class proportions are preserved.

Original:

* 90% class 0
* 10% class 1

Training:

* 720 class 0
* 80 class 1

Test:

* 180 class 0
* 20 class 1

Both sets maintain the original **90:10** ratio.

---

### What about `class_weight="balanced"`?

This is completely different.

After the split, suppose your training set is:

| Class | Count |
| ----- | ----: |
| 0     |   720 |
| 1     |    80 |

The data is **still imbalanced**.

When you train:

```python
LogisticRegression(class_weight="balanced")
```

the model internally assigns larger weights to the minority class (class 1), making mistakes on those samples more costly during optimization.

It **does not change the dataset**. It only changes how the loss function is computed.

---

### Summary

| Technique                  | What it does                                                           |
| -------------------------- | ---------------------------------------------------------------------- |
| `stratify=y`               | Preserves the original class proportions in the train and test splits. |
| `class_weight="balanced"`  | Gives higher importance to the minority class during training.         |
| Oversampling (e.g., SMOTE) | Increases the number of minority class samples.                        |
| Undersampling              | Reduces the number of majority class samples.                          |

A good mental model is:

* **`stratify`** decides **how to split the data**.
* **`class_weight`** decides **how much each class matters while learning**.

They solve different problems and are often used together on imbalanced datasets.
