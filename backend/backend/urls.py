from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from typing import List, Optional
from datetime import date
from decimal import Decimal
from django.contrib.auth.hashers import make_password
from django.db import connection
from ninja.security import HttpBearer
from django.conf import settings
from ninja.errors import HttpError
from datetime import datetime, timedelta
import jwt # pylint: disable=import-error
import re


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "Token has expired")
        except jwt.InvalidTokenError:
            raise HttpError(401, "Invalid token")

api = NinjaAPI(auth=AuthBearer())

# Schemas
class RegisterSchema(Schema):
    username: str
    password: str
    confirm_password: str

class LoginSchema(Schema):
    username: str
    password: str

class CategorySchema(Schema):
    id: int
    name: str

class ExpenseSchema(Schema):
    id: int
    user_id: int
    category_id: Optional[int]
    amount: Decimal
    description: Optional[str]
    date: date

class IncomeSchema(Schema):
    id: int
    user_id: int
    amount: Decimal
    source: Optional[str]
    description: Optional[str]
    date: date

class ExpenseInSchema(Schema):
    category_id: Optional[int]
    amount: Decimal
    description: Optional[str]
    date: date

class IncomeInSchema(Schema):
    amount: Decimal
    source: Optional[str]
    description: Optional[str]
    date: date



@api.post("/login", auth=None)
def login(request, credentials: LoginSchema):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM users WHERE username = %s AND password = %s",
            [credentials.username, credentials.password]
        )
        user = cursor.fetchone()
        if user:
            payload = {
                'user_id': user[0],
                'exp': datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            return {"token": token}
    return {"error": "Invalid credentials"}

@api.post("/register", auth=None)
def register(request, data: RegisterSchema):
    if len(data.password) < 9:
        raise HttpError(400, "Password must be at least 8 characters long")

    if data.password != data.confirm_password:
        raise HttpError(400, "Passwords do not match")

    if not re.search(r'\d', data.password) or not re.search(r'[a-zA-Z]', data.password):
        raise HttpError(400, "Password must contain both letters and numbers")

    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM auth_user WHERE username = %s", [data.username])
        if cursor.fetchone():
            raise HttpError(409, "Username already exists")

        hashed_password = make_password(data.password)
        cursor.execute(
            "INSERT INTO auth_user (username, password, is_superuser, is_staff, is_active, date_joined) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            [data.username, hashed_password, False, False, True, datetime.now()]
        )
        user_id = cursor.lastrowid

    return {"message": "Registration successful. Please log in."}

# Category endpoints
@api.get("/categories", response=List[CategorySchema])
def list_categories(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM categories")
        categories = [CategorySchema(id=row[0], name=row[1]) for row in cursor.fetchall()]
    return categories

@api.post("/categories")
def create_category(request, payload: CategorySchema):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO categories (name) VALUES (%s)", [payload.name])
        category_id = cursor.lastrowid
    return {"id": category_id}

# Expense CRUD
@api.get("/expenses", response=List[ExpenseSchema])
def list_expenses(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        expenses = [ExpenseSchema(**dict(zip([col[0] for col in cursor.description], row))) for row in cursor.fetchall()]
    return expenses

@api.get("/expenses/{expense_id}", response=ExpenseSchema)
def get_expense(request, expense_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE id = %s", [expense_id])
        row = cursor.fetchone()
        if row:
            return ExpenseSchema(**dict(zip([col[0] for col in cursor.description], row)))
    return {"error": "Expense not found"}

@api.post("/expenses", response=ExpenseSchema)
def create_expense(request, payload: ExpenseInSchema):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO expenses (user_id, category_id, amount, description, date) VALUES (%s, %s, %s, %s, %s)",
            [request.auth, payload.category_id, payload.amount, payload.description, payload.date]
        )
        expense_id = cursor.lastrowid
        cursor.execute("SELECT * FROM expenses WHERE id = %s", [expense_id])
        row = cursor.fetchone()
        return ExpenseSchema(**dict(zip([col[0] for col in cursor.description], row)))

@api.put("/expenses/{expense_id}", response=ExpenseSchema)
def update_expense(request, expense_id: int, payload: ExpenseInSchema):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE expenses SET category_id = %s, amount = %s, description = %s, date = %s WHERE id = %s",
            [payload.category_id, payload.amount, payload.description, payload.date, expense_id]
        )
        if cursor.rowcount:
            cursor.execute("SELECT * FROM expenses WHERE id = %s", [expense_id])
            row = cursor.fetchone()
            return ExpenseSchema(**dict(zip([col[0] for col in cursor.description], row)))
    return {"error": "Expense not found"}

@api.delete("/expenses/{expense_id}")
def delete_expense(request, expense_id: int):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM expenses WHERE id = %s", [expense_id])
        if cursor.rowcount:
            return {"success": True}
    return {"error": "Expense not found"}

# Income CRUD
@api.get("/incomes", response=List[IncomeSchema])
def list_incomes(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM income")
        incomes = [IncomeSchema(**dict(zip([col[0] for col in cursor.description], row))) for row in cursor.fetchall()]
    return incomes

@api.get("/incomes/{income_id}", response=IncomeSchema)
def get_income(request, income_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM income WHERE id = %s", [income_id])
        row = cursor.fetchone()
        if row:
            return IncomeSchema(**dict(zip([col[0] for col in cursor.description], row)))
    return {"error": "Income not found"}

@api.post("/incomes", response=IncomeSchema)
def create_income(request, payload: IncomeInSchema):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO income (user_id, amount, source, description, date) VALUES (%s, %s, %s, %s, %s)",
            [request.auth, payload.amount, payload.source, payload.description, payload.date]
        )
        income_id = cursor.lastrowid
        cursor.execute("SELECT * FROM income WHERE id = %s", [income_id])
        row = cursor.fetchone()
        return IncomeSchema(**dict(zip([col[0] for col in cursor.description], row)))

@api.put("/incomes/{income_id}", response=IncomeSchema)
def update_income(request, income_id: int, payload: IncomeInSchema):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE income SET amount = %s, source = %s, description = %s, date = %s WHERE id = %s",
            [payload.amount, payload.source, payload.description, payload.date, income_id]
        )
        if cursor.rowcount:
            cursor.execute("SELECT * FROM income WHERE id = %s", [income_id])
            row = cursor.fetchone()
            return IncomeSchema(**dict(zip([col[0] for col in cursor.description], row)))
    return {"error": "Income not found"}

@api.delete("/incomes/{income_id}")
def delete_income(request, income_id: int):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM income WHERE id = %s", [income_id])
        if cursor.rowcount:
            return {"success": True}
    return {"error": "Income not found"}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
