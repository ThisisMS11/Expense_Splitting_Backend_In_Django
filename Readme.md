# Expense Splitting Backend

This is a backend application for managing and splitting expenses among users. The backend supports functionalities like user registration, adding expenses, splitting costs, tracking payments, and downloading balance sheets.

## Project Setup

### Prerequisites

- Python 3.x
- Django
- Django REST Framework
- Pipenv or pip for managing dependencies

> I have used sqlite for this project to keep things simpler.

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ThisisMS11/Expense_Splitting_Backend_In_Django.git
   cd Expense_Splitting_Backend_In_Django
   ```

2. **Install dependencies**:
   Using Pipenv:
   ```bash
   pipenv install
   ```

   Using pip:
   ```bash
   pip install -r requirements.txt
   ```


3. **Apply migrations**:
   Run the following command to set up the database:
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser**:
   You can create an admin user for accessing the Django admin interface:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   Start the server by running:
   ```bash
   python manage.py runserver
   ```

6. **Access the API**:
   You can now access the API at `http://localhost:8000/api/`.

---

## API Documentation

### **Authentication and Users**

#### 1. **User Registration** (`/users/register`)

- **Method**: `POST`
- **Description**: Register a new user.
- **Request Body**:
  ```json
  {
    "name": "string",
    "email": "string",
    "password": "string",
    "mobile_number": "string",
  }
  ```
- **Response**: Returns user details upon successful registration.
  ```json
  {
    "username": "string",
    "mobile_number": "string"
  }
  ```

#### 2. **Token Authentication** (`/users/token`)

- **Method**: `POST`
- **Description**: Obtain an authentication token.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
  }
  ```

#### 3. **Token Refresh** (`/users/token/refresh`)

- **Method**: `POST`
- **Description**: Refresh the access token using the refresh token.
- **Request Body**:
  ```json
  {
    "refresh": "jwt_refresh_token"
  }
  ```
- **Response**:
  ```json
  {
    "access": "new_jwt_access_token"
  }
  ```

#### 4. **User Information** (`/api/users/info`)

- **Method**: `GET`
- **Description**: Retrieve the logged-in user's information.
- **Headers**:
  - `Authorization: Bearer <token>`
- **Response**:
  ```json
  {
    "email": "string",
    "mobile_number": "string",
  }
  ```
---

### **Expense Management**

#### 1. **Add Expense** (`/api/expense/add`)

- **Method**: `POST`
- **Description**: Add a new expense and split it among participants.
- **Request Body**:
  ```json
  {
    "description": "string",
    "amount": "decimal",
    "participants": ["user_id1", "user_id2", ...],
    "split_method": "EQUAL/EXACT/PERCENTAGE",
    "exact_amounts": {"user_id": "amount_due"},
    "percentages": {"user_id": "percentage_due"}
  }
  ```
- **Response**:
  ```json
  {
    "id": "int",
    "description": "string",
    "amount": "decimal",
    "splits": [
      {
        "user": "username",
        "amount_due": "decimal",
        "amount_paid": "decimal",
        "status": "PENDING/COMPLETED"
      }
    ]
  }
  ```

#### 2. **User Expenses** (`/expense/user-expenses`)

- **Method**: `GET`
- **Description**: Get the logged-in user's expenses.
- **Headers**:
  - `Authorization: Bearer <token>`
- **Response**:
  ```json
  [
    {
      "id": "int",
      "description": "string",
      "amount": "decimal",
      "splits": [
        {
          "user": "username",
          "amount_due": "decimal",
          "amount_paid": "decimal",
          "status": "PENDING/COMPLETED"
        }
      ]
    }
  ]
  ```

#### 3. **Overall Expenses** (`/expense/overall-expenses`)

- **Method**: `GET`
- **Description**: Get an overview of all expenses.
- **Headers**:
  - `Authorization: Bearer <token>`
- **Response**:
  ```json
  [
    {
      "id": "int",
      "description": "string",
      "amount": "decimal",
      "splits": [
        {
          "user": "username",
          "amount_due": "decimal",
          "amount_paid": "decimal",
          "status": "PENDING/COMPLETED"
        }
      ]
    }
  ]
  ```

#### 4. **Pay Expense** (`/expense/user-pay-expense/<int:expense_id>`)

- **Method**: `POST`
- **Description**: Pay a portion or all of the amount owed for an expense.
- **Headers**:
  - `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "payment_amount": "decimal"
  }
  ```
- **Response**:
  ```json
  {
    "status": "PENDING/PARTIALLY_PAID/COMPLETED",
    "amount_due": "decimal",
    "amount_paid": "decimal"
  }
  ```

#### 5. **Download Balance Sheet** (`/expense/balance-sheet/download/`)

- **Method**: `GET`
- **Description**: Download the balance sheet as PDF.
- **Headers**:
  - `Authorization: Bearer <token>`
- **Response**: Downloads the file in the pdf format.

---


[Postman Collection Link](https://drive.google.com/file/d/1ia3xMPLT3JatoR2eVt0HbYBu4-u8nnAQ/view?usp=sharing)

