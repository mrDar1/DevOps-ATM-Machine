# DevOps ATM Machine

> a python Tkinther app emulates an ATM machine devops themed

**Authors:** David Snir & Yuval Dar

---

## 📁 Project Structure

```bash
DevOps ATM Machine/
│
├── .venv/               # virtual environment
├── Images/              # assets (icons, graphics)
├── Tests/               # unit tests
│
├── main.py              # starts app
├── models.py            # logic — account & bank classes
├── storage.py           # read & writes to "data.json" (create new if not exist)
├── ui.py                # minimal functional UI
├── figma_ui.py          # Figma-designed UI (advanced layout, currently have 2-pages)
├── style.py             # color & font const
│
├── .env                 # admin secret password (not tracked)
├── .gitignore           # ignores .venv, .env, data.json
```

---

### Prerequisites

- Python 3.8+ (we use pyenv for python 3.14.3 version)
- pip

### Installation

```bash
# clone
git clone https://github.com/your-username/devops-atm-machine.git
cd devops-atm-machine

# activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
python main.py
```
<!--

---

## environment variables
// still not sure if to use it like that or hash it:

create a `.env` file in the root directory:

```env
ADMIN_PASSWORD=your_secret_password
```

> **Never commit `.env` file.** It's already listed in `.gitignore`.

-->
---

## 👥 Authors

| Name | GitHub |
|---|---|
| David Snir | [@davidsnir](https://github.com/davidsnir) |
| Yuval Dar | [@yuvaldar](https://github.com/yuvaldar) |

---

