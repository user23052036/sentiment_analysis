
# Git Recovery & Safety Notes (ML / Data Projects)

> Purpose of this file:
> Prevent **data loss**, **panic**, and **GitHub push failures** in ML projects.

---

## 0. Core Mental Model (NON-NEGOTIABLE)

Git has **three different realities**. Confusing them causes 90% of disasters.

### The three realities

* **Commit**
  → A permanent snapshot of files at a moment in time
  → Once created, it does **not change**

* **HEAD**
  → A pointer saying “this is the commit I’m currently on”

* **Working tree**
  → Actual files on disk right now

### Dangerous command to respect

```bash
git reset --hard
```

What it really does:

* Moves `HEAD` to another commit
* Replaces your **working tree** with that commit’s snapshot
* **Deletes all uncommitted changes**

> 🔥 Rule:
> **If code is not committed or stashed, Git considers it disposable**

---

## 1. Before ANY destructive command

Before running **reset, rebase, checkout, force push**, always ask:

> “Is my current work safely stored as a commit?”

### Always run:

```bash
git status
git log --oneline --decorate -5
```

### Interpret the result

* If `git status` shows modified files → **you can lose them**
* If everything is committed → safe to proceed

### If you see uncommitted work

You have two safe options:

```bash
git commit -m "WIP"
```

or

```bash
git stash
```

---

## 2. Safe ways to undo commits (CRITICAL DIFFERENCES)

These commands **only differ by one word**, but consequences are huge.

### Undo last commit but KEEP code staged

```bash
git reset --soft HEAD~1
```

Meaning:

* Commit is removed
* Files stay staged
* **No data loss**

Use when:

* commit message was wrong
* you want to amend commit

---

### Undo commit and unstage files but KEEP code

```bash
git reset --mixed HEAD~1
```

Meaning:

* Commit removed
* Files stay in working tree
* **Still safe**

Use when:

* you want to reorganize commits

---

### ⚠️ Undo commit AND DELETE code (DANGEROUS)

```bash
git reset --hard HEAD~1
```

Meaning:

* Commit removed
* Working tree overwritten
* **Uncommitted work is permanently deleted**

Only use when:

* you are 100% sure nothing valuable is uncommitted

---

## 3. “I lost my code” — Recovery section (MOST IMPORTANT)

If you panic, **STOP TYPING**. Recovery depends on not making it worse.

### Step 1: Use reflog (Git’s black box recorder)

```bash
git reflog
```

What reflog shows:

* Every place `HEAD` has ever pointed
* Even commits no longer on a branch

Example:

```
29aac6b HEAD@{1}: commit: added TF-IDF logic
93cc51a HEAD@{0}: reset: moving to 93cc51a
```

This means:

* Commit still exists
* It is recoverable

---

### Step 2: Restore the commit

Fast restore (overwrites working tree):

```bash
git reset --hard 29aac6b
```

Safer restore (creates rescue branch):

```bash
git checkout -b recovery 29aac6b
```

> 🧠 Key insight:
> **Commits don’t vanish immediately. Pointers move — data stays.**

---

## 4. GitHub 100MB file rejection (ML-specific)

### Typical symptoms

* Push rejected
* Error says file exceeds 100 MB

### Common misunderstanding

`.gitignore` **does NOT** remove files already committed.

It only affects:

* future files
* untracked files

---

## 5. Find large tracked files

### List biggest files in repo

```bash
git ls-tree -r --long HEAD | sort -k4 -n | tail -20
```

### Quickly check common ML folders

```bash
git ls-files | grep -E '^(data/|models/)'
```

If files appear here → GitHub will reject push.

---

## 6. Remove large files WITHOUT deleting locally

This is the **correct fix**.

```bash
git rm --cached path/to/large_file
```

For folders:

```bash
git rm -r --cached data/
git rm -r --cached models/
```

What this does:

* Removes file from Git history going forward
* Keeps file on your disk
* Shrinks repo for GitHub

---

## 7. Lock it permanently with `.gitignore`

For ML projects, this is **mandatory**.

```
# environments
venv/

# datasets & artifacts
data/
sentiment_analysis_data/
models/
nltk_data/

# notebooks
.ipynb_checkpoints/

# misc
~lock.*
```

Purpose:

* Prevent accidental recommits
* Enforce clean repo boundaries

---

## 8. Commit the cleanup

```bash
git add .gitignore
git commit -m "remove datasets and ignore local artifacts"
```

After this:

* Repo becomes pushable
* History is clean

---

## 9. Force push (only when required)

```bash
git push origin master --force
```

Why force is needed:

* Local history changed
* GitHub must accept rewritten history

Safe **only if**:

* you are the only contributor
* or team explicitly agrees

---

## 10. ML Repo Hygiene Rules (burn into memory)

### NEVER commit

* datasets
* trained models
* NLP corpora
* caches

### ALWAYS commit

* code
* notebooks (cleaned)
* README explaining dataset download

---

## 11. Final sanity checks before pushing

```bash
git status
git count-objects -vH
```

If:

* working tree clean
* repo size reasonable

→ push safely.

---

## 12. Emergency checklist (panic protocol)

1. Stop typing
2. `git status`
3. `git reflog`
4. Recover commit
5. Then think

---

## Final mentor truth

Git did **exactly** what you told it to do.
It does not protect you from bad decisions.

Once you understand:

* snapshots
* pointers
* tracked vs untracked

Git stops being scary and starts being boring — which is ideal.

---
