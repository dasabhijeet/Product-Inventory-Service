# 📦 Inventory Management API

A lightweight Inventory Management REST API built with **FastAPI** and **SQLite**, supporting product management, stock tracking, and inventory logging with safe transactional updates using threadpool execution.

---

## 🚀 Features

- Product CRUD (Create, Read, Update, Delete)
- Stock management (Add / Remove inventory)
- Inventory logging for every stock change
- Transaction-safe updates
- SQLite-based persistent storage
- Threadpool execution for safe blocking DB operations
- Minimal and clean architecture

---

## 🛠 Tech Stack

- Python
- FastAPI
- SQLite
- Uvicorn

---

## 📁 Project Structure

app.py  
mysql_utils.py  
.env  
requirements.txt  

---

## ⚙️ Setup & Run

### 1. Install dependencies

pip install fastapi uvicorn python-dotenv

---

### 2. Run the server

uvicorn app:app --reload

OR

python app.py

<img width="557" height="493" alt="image" src="https://github.com/user-attachments/assets/58a9044b-945e-4686-8d98-386bbd8ab163" />

---

### 3. Open API docs

http://127.0.0.1:8000/docs

<img width="1288" height="656" alt="image" src="https://github.com/user-attachments/assets/81cc5b1f-2075-44a4-a4b2-0397df038ef2" />

---

## 📌 API Endpoints

### 🛒 Products

POST /products  
GET /products  
GET /products/{id}  
PUT /products/{id}  
DELETE /products/{id}  

<img width="1338" height="676" alt="image" src="https://github.com/user-attachments/assets/378c40b9-8a94-4048-846f-8357dc103acb" />

---

### 📦 Inventory

POST /inventory/add  
POST /inventory/remove  

---

## 📊 Inventory Logging

Every stock operation is recorded in `inventory_logs`:

- ADD → stock increase
- REMOVE → stock decrease

Each log contains:
- product_id
- type (ADD / REMOVE)
- quantity
- timestamp

---

## 🧠 Design Notes

- SQLite used for simplicity and local execution
- Threadpool used to safely handle blocking DB operations in async FastAPI routes
- Transactions ensure inventory consistency
- Minimal architecture for clarity and readability

---

## ⚠️ Notes

- This project is designed for assignment/demo purposes
- No authentication included
- No distributed system components
