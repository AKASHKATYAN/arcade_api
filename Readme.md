# 💳 FastAPI Card Recharge API

A simple **FastAPI-based backend project** that simulates a card system with features like:

* Creating cards
* Viewing card details
* Recharging card balance
* Storing data in a JSON file (as a lightweight database)

This project is **beginner-friendly** and designed so it can be **easily migrated to SQL databases** (PostgreSQL / MySQL) later without major code changes.

---

## 🚀 Features

* FastAPI RESTful API
* JSON file used as database (no DB setup required)
* Proper HTTP methods (GET / POST / PUT)
* Input validation using Pydantic
* Clean and scalable API structure

---

## 🛠 Tech Stack

* **Python 3.9+**
* **FastAPI**
* **Uvicorn**
* **Pydantic**
* JSON (temporary data storage)

---

## 📁 Project Structure

```text
project/
│── main.py              # FastAPI app
│── utils.py             # JSON read/write helpers
│── data.json            # Acts as database
│── requirements.txt     # Project dependencies
│── README.md            # Project documentation
```

---

## 📦 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd project
```

### 2️⃣ Create & activate virtual environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Server

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

Swagger UI (API docs):

```
http://127.0.0.1:8000/docs
```

---

## 🔌 API Endpoints

### 🔹 Create Card

**POST** `/create_card/`

```json
{
  "card_id": "1234567890",
  "balance": 1000
}
```

---

### 🔹 View Card Details

**GET** `/view_cards/?card_id=1234567890`

**Response**

```json
{
  "card_id": "1234567890",
  "balance": 1500
}
```

---

### 🔹 Recharge Card

**PUT** `/recharge/`

```json
{
  "card_id": "1234567890",
  "amount": 500
}
```

**Response**

```json
{
  "card_id": "1234567890",
  "balance": 1500
}
```

---

## 📄 Sample `data.json`

```json
[
  {
    "card_id": "1234567890",
    "balance": 1000
  },
  {
    "card_id": "9876543210",
    "balance": 2000
  }
]
```

---

## ⚠️ Validations & Errors

* Duplicate card creation not allowed
* Recharge amount must be **positive**
* Returns proper HTTP status codes:

  * `400` → Bad request
  * `404` → Card not found

---

## 🔮 Future Enhancements

* Replace JSON with PostgreSQL / MySQL
* Add transaction history
* Authentication & authorization
* Admin dashboard
* Docker support

---

## 🧠 Design Philosophy

* Follow REST standards
* Keep business logic DB-agnostic
* Easy learning → easy scaling

---

## 👨‍💻 Author

**Akash Katyan**
FastAPI & Backend Development Learner

---

