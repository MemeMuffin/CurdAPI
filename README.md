# 🛍️ FastAPI CRUD API with User Permissions

A full-featured FastAPI app that handles user login and registration with JWT, and CRUD operations for a product model. Product routes are protected using permission scopes.

## ⚙️ Features

- User registration and login
- JWT token with scopes (e.g., `active`)
- Full CRUD on product routes
- Route protection using FastAPI `Security` and JWT scopes
- SQLite database using SQLModel

## 🔐 Scopes

- `active`: required to access product routes

## 🛠️ Tech Stack

- FastAPI
- SQLModel
- SQLite
- OAuth2 with scopes
- JWT (PyJWT)
- Pydantic

## 📦 Installation

```bash
git clone <your-repo-url>
cd <repo-folder>
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt


📮 API Endpoints
🔐 Auth
POST /register

POST /token

GET /login/me/

🛍️ Products
GET /user/products/getproducts/ - List all products

POST /user/products/createproduct/ - Create a new product

PATCH /user/products/updateproduct/ - Update a product

DELETE /user/products/deleteproduct/ - Delete a product

🛡️ Note: All product routes require a valid token with active scope.

