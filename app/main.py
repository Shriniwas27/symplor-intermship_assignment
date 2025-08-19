from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import os

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import get_db, engine
from app.db.base import Base
from app.db.models.employee import Employee
from app.core.security import get_password_hash, create_access_token
from app.services.employee_service import EmployeeService
from app.services.leave_service import LeaveService


Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("Application starting up...")
    
    db = next(get_db())
    try:
        employee_service = EmployeeService(db)
        admin = employee_service.get_employee_by_email(settings.default_admin_email)
        if not admin:
            admin_data = {
                "name": "System Admin",
                "email": settings.default_admin_email,
                "department": "IT",
                "joining_date": "2024-01-01",
                "is_admin": True,
                "password": settings.default_admin_password
            }
            from app.schemas.employee import EmployeeCreate
            admin_create = EmployeeCreate(**admin_data)
            employee_service.create_employee(admin_create)
            print(f"Default admin created: {settings.default_admin_email}")
        else:
            print("Default admin already exists")
    except Exception as e:
        print(f"Error creating default admin: {e}")
    finally:
        db.close()
    
    yield
    
    print("Application shutting down...")

app = FastAPI(
    title="Leave Management System",
    description="A comprehensive leave management system for startups",
    version="1.0.0",
    lifespan=lifespan
)


if settings.backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router, prefix="/api/v1")


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/employees", response_class=HTMLResponse)
async def employees_page(request: Request):
    """Employees page"""
    return templates.TemplateResponse("employees.html", {"request": request})

@app.get("/leaves", response_class=HTMLResponse)
async def leaves_page(request: Request):
    """Leaves page"""
    return templates.TemplateResponse("leaves.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Leave Management System is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)