# 🧠 User Management API (Refactored)

This project is a refactored version of a legacy Flask-based User Management API. It focuses on improved **code quality**, **security**, and **maintainability**, while preserving all original functionalities.

---

## 🚀 Features

- CRUD operations on users
- User login with hashed password
- Search users by name
- SQLite backend with simple setup
- Fully self-contained `app.py`

---

## 🛠️ Setup Instructions

### ✅ Prerequisites

- Python 3.8+
- pip

### 📦 Installation

```bash
# Clone or download the repository
cd messy-migration

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# Run the Flask server
python app.py
The API will be live at:
📍 http://localhost:5000

