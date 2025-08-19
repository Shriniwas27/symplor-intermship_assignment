from datetime import date
from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
from app.db.models.leave import LeaveType, LeaveStatus

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str
    joining_date: date

class EmployeeCreate(EmployeeBase):
    password: Optional[str] = None
    is_admin: Optional[bool] = False

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    leave_balance: Optional[float] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class Employee(EmployeeBase):
    id: int
    leave_balance: float
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True

class EmployeeWithLeaves(Employee):
    leave_requests: List["LeaveRequest"] = []