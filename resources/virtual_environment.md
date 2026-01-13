
# Python Virtual Environment & Jupyter Reference

## 1. Checking Python Versions

```bash
python --version
python3 --version
```

Always prefer **Python 3**.

---

## 2. Why Virtual Environments Are Used

Virtual environments isolate project dependencies.

* Each project gets its own packages
* No version conflicts
* Safe experimentation
* Clean project boundaries

**Rule:** one virtual environment per project.

---

## 3. Creating a Virtual Environment

```bash
python3 -m venv venv
```

Why:

* Forces Python 3
* Avoids accidental Python 2 usage

---

## 4. Activating the Virtual Environment

### Linux / macOS

```bash
source venv/bin/activate
```

After activation, your terminal shows:

```text
(venv)
```

---

## 5. Verifying the Virtual Environment

### Check active Python

```bash
which python
```

### Confirm executable path

```bash
python -c "import sys; print(sys.executable)"
```

Expected output:

```text
.../venv/bin/python
```

---

## 6. Installing Packages (inside venv)

```bash
pip install package_name
```

Verify installed packages:

```bash
pip list
```

---

## 7. Deactivating the Virtual Environment

```bash
deactivate
```

The `(venv)` prefix disappears.

---

## 8. Key Rules (Terminal Usage)

* Always activate venv before installing packages
* Never use `sudo pip install`
* Never install project packages globally
* One venv per project

---

# Jupyter Notebook (`.ipynb`) + Virtual Environment

> Terminal venv and Jupyter kernel are **not automatically connected**.

---

## 9. Installing Jupyter Support in the venv (One-Time)

After activating the venv:

```bash
pip install ipykernel
```

This allows Jupyter to run Python code from this venv.

---

## 10. Registering the venv as a Jupyter Kernel

```bash
python -m ipykernel install --user --name venv --display-name "Python (venv)"
```

This makes the venv selectable as a notebook kernel.

---

## 11. Selecting the Correct Kernel

In VS Code / Jupyter:

* Open `.ipynb`
* Click **Kernel Picker**
* Select **Python (venv)**

---

## 12. Verifying Notebook Uses the venv

Run inside a notebook cell:

```python
import sys
print(sys.executable)
```

Expected output:

```text
.../venv/bin/python
```

---

## 13. Installing Packages for Notebooks

Always install packages **inside the activated venv**:

```bash
pip install numpy pandas
```

Then restart the notebook kernel.

---

## 14. Important Notes for `.ipynb`

* Each venv needs `ipykernel` once
* Notebook kernel must match terminal venv
* `pip list` shows only venv-installed packages
* System packages ≠ venv pollution (Linux behavior)

---

## 15. Mental Model (Critical)

```
Terminal venv  ≠  Jupyter kernel
You must connect them explicitly.
```

---

## 16. Recommended Workflow

1. Create venv
2. Activate venv
3. Install `ipykernel`
4. Select venv kernel in notebook
5. Install project packages
6. Restart kernel

---
