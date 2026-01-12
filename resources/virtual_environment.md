
### Creating Python Virtual Environment

* **First check your Python versions**

  ```bash
  python --version
  python3 --version
  ```

* **Why virtual environments are used**

  Virtual environments isolate project dependencies.
  Each project gets its own Python packages, preventing version conflicts between different projects.

* **Create a virtual environment (recommended)**

  ```bash
  python3 -m venv venv
  ```

  This guarantees the **Python 3 interpreter** and avoids accidental use of Python 2.

---

### Activating the Virtual Environment

* **Linux / macOS**

  ```bash
  source venv/bin/activate
  ```

After activation, your terminal prompt will show:

```text
(venv)
```

---

### Verifying the Virtual Environment

* **Check which Python is being used**

  ```bash
  which python
  ```

* **Confirm Python executable path**

  ```bash
  python -c "import sys; print(sys.executable)"
  ```

  Output should point to:

  ```text
  .../venv/bin/python
  ```

---

### Installing Packages (inside venv)

```bash
pip install package_name
```

To verify installation:

```bash
pip list
```

---

### Deactivating the Virtual Environment

```bash
deactivate
```

The `(venv)` prefix will disappear from the terminal.

---

### Key Notes

* Always activate the venv **before** installing packages
* Never use `sudo pip install`
* Create **one venv per project**

