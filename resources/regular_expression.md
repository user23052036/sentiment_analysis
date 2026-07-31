# Regular Expressions — Everything You Need for This Project

## What `re` Is

`re` is Python's built-in module for pattern matching in strings. You describe a pattern, and `re` finds or replaces text that matches it.

The only function used in this project is:

```python
re.sub(pattern, replacement, string)
```

It finds every match of `pattern` inside `string` and replaces it with `replacement`. It returns the modified string — it does not change the original.

```python
import re
result = re.sub(r"cat", "dog", "I have a cat and a cat")
# result → "I have a dog and a dog"
```

---

## The `r""` Prefix

Every pattern in this project starts with `r`. This is a **raw string** — it tells Python not to interpret backslashes specially.

Without `r`:  `"\n"` means a newline character.
With `r`:     `r"\n"` means a literal backslash followed by `n`.

Since regex patterns use `\` heavily, always write them as `r"..."`.

---

## Building Blocks Used in This Project

You only need to know six things to read every pattern in `clean_tweet`.

### 1. `\S` — any non-whitespace character

Matches anything that is **not** a space, tab, or newline. Letters, digits, punctuation, symbols — all match.

```
\S  →  matches  a  3  @  .  /  :
\S  →  no match  (space)  (newline)
```

### 2. `\w` — any word character

Matches letters (`a-z`, `A-Z`), digits (`0-9`), and underscore `_`. Does **not** match spaces, `@`, `.`, `-`, etc.

```
\w  →  matches  a  Z  5  _
\w  →  no match  @  .  (space)
```

### 3. `\s` — any whitespace character

The opposite of `\S`. Matches spaces, tabs, and newlines.

```
\s  →  matches  (space)  (tab)  (newline)
\s  →  no match  a  3  @
```

### 4. `+` — one or more (quantifier)

Placed after a symbol, it means "match this thing **one or more times in a row**."

```
\S+  →  matches one or more non-whitespace characters in a row
         "hello"  "http://x.com"  "@user123"
\w+  →  matches one or more word characters in a row
         "hello"  "user123"  "Dr"
\s+  →  matches one or more whitespace characters in a row
         "   "  " \t "
```

### 5. `[...]` — character class (match any one of these)

Square brackets define a set. One character is matched if it belongs to the set.

```
[abc]    →  matches  a  or  b  or  c
[a-z]    →  matches any lowercase letter  a through z
[a-z\s]  →  matches any lowercase letter OR any whitespace character
```

### 6. `[^...]` — negated character class (match anything NOT in this set)

A `^` at the start of `[...]` inverts it.

```
[^a-z\s]  →  matches anything that is NOT a lowercase letter and NOT whitespace
              numbers, uppercase letters, punctuation, symbols — all match
              a  b  (space)  (newline)  →  no match
```

---

## The Four Patterns in `clean_tweet`, Explained

```python
def clean_tweet(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)       # 1. remove URLs
    text = re.sub(r"@\w+", "", text)          # 2. remove @mentions
    text = re.sub(r"[^a-z\s]", "", text)      # 3. keep only letters + spaces
    text = re.sub(r"\s+", " ", text).strip()  # 4. collapse whitespace
    return text
```

---

### Line 1 — `text.lower()`

Not regex. Python string method. Converts every character to lowercase so `Love`, `LOVE`, and `love` are all treated as the same word.

---

### Line 2 — `r"http\S+"`  →  remove URLs

| Part | Meaning |
|------|---------|
| `http` | Match the literal characters `h`, `t`, `t`, `p` in sequence |
| `\S+` | Then match one or more non-whitespace characters |

A URL like `https://t.co/abc123` starts with `http` and continues with non-space characters until the URL ends. This pattern captures the whole thing.

```
Input:   "check this out http://t.co/abc123 now"
Pattern: http\S+  →  matches "http://t.co/abc123"
Replace: ""
Output:  "check this out  now"
```

The trailing double-space will be cleaned up by line 4.

---

### Line 3 — `r"@\w+"`  →  remove @mentions

| Part | Meaning |
|------|---------|
| `@` | Match the literal `@` character |
| `\w+` | Then match one or more word characters (the username) |

```
Input:   "thanks @JohnDoe for the help"
Pattern: @\w+  →  matches "@JohnDoe"
Replace: ""
Output:  "thanks  for the help"
```

---

### Line 4 — `r"[^a-z\s]"`  →  keep only lowercase letters and spaces

| Part | Meaning |
|------|---------|
| `[^a-z\s]` | Match any character that is NOT a lowercase letter and NOT whitespace |

By replacing all such characters with `""`, everything except letters and spaces is deleted — numbers, punctuation, symbols, uppercase letters (already removed by `.lower()`), etc.

```
Input:   "i love ml! it's great :)"
Pattern: [^a-z\s]  →  matches  !  '  :  )
Replace: ""
Output:  "i love ml its great "
```

Note: `'` in `it's` is also removed. The apostrophe is not in `[a-z\s]`, so it gets stripped. This is an acceptable trade-off for tweet-scale text.

---

### Line 5 — `r"\s+"`  →  collapse whitespace

| Part | Meaning |
|------|---------|
| `\s+` | Match one or more consecutive whitespace characters (spaces, tabs, newlines) |

Previous steps leave gaps where URLs, mentions, and punctuation were removed. This collapses any run of whitespace into a single space.

`.strip()` then removes any leading or trailing space from the whole string.

```
Input:   "i love   ml   its great "
Pattern: \s+  →  matches "   "  and "   "
Replace: " "
Output:  "i love ml its great "
After .strip():  "i love ml its great"
```

---

## Full Worked Example

Tweet: `"@user check http://t.co/abc Love it!! :D"`

| Step | Operation | Result |
|------|-----------|--------|
| `.lower()` | lowercase everything | `"@user check http://t.co/abc love it!! :d"` |
| `re.sub(r"http\S+", "")` | remove URL | `"@user check  love it!! :d"` |
| `re.sub(r"@\w+", "")` | remove mention | `" check  love it!! :d"` |
| `re.sub(r"[^a-z\s]", "")` | remove non-letter non-space | `" check  love it  d"` |
| `re.sub(r"\s+", " ").strip()` | collapse + trim whitespace | `"check love it d"` |

---

## Quick Reference Card

| Symbol | Matches |
|--------|---------|
| `\S` | any non-whitespace character |
| `\w` | any letter, digit, or underscore |
| `\s` | any whitespace (space, tab, newline) |
| `+` | one or more of the preceding |
| `[abc]` | any one character inside the brackets |
| `[a-z]` | any lowercase letter |
| `[^...]` | any character NOT listed in brackets |
| `r"..."` | raw string — use for all regex patterns |

| Pattern | What it removes | Used for |
|---------|----------------|---------|
| `http\S+` | URLs | remove links |
| `@\w+` | @mentions | remove usernames |
| `[^a-z\s]` | everything except letters/spaces | strip punctuation, numbers, symbols |
| `\s+` | runs of whitespace | normalize spacing |