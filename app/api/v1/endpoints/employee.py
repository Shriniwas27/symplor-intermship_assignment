from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate
from app.services.employee_service import EmployeeService
from app.api.dependencies import get_current_admin_user, get_current_user
from app.db.models.employee import Employee as EmployeeModel

router = APIRouter()

@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: EmployeeModel = Depends(get_current_admin_user)
):
    """Create a new employee (Admin only)"""
    employee_service = EmployeeService(db)
    return employee_service.create_employee(employee)

@router.get("/", response_model=List[Employee])
def read_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: EmployeeModel = Depends(get_current_user)
):
    """Get all employees"""
    employee_service = EmployeeService(db)
    return employee_service.get_employees(skip=skip, limit=limit)

@router.get("/me", response_model=Employee)
def read_current_employee(current_user: EmployeeModel = Depends(get_current_user)):
    """Get current user's profile"""
    return current_user

@router.get("/{employee_id}", response_model=Employee)
def read_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: EmployeeModel = Depends(get_current_user)
):
    """Get employee by ID"""
    employee_service = EmployeeService(db)
    employee = employee_service.get_employee(employee_id)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    if current_user.id != employee_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return employee

@router.put("/{employee_id}", response_model=Employee)
def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: EmployeeModel = Depends(get_current_admin_user)
):
    """Update employee (Admin only)"""
    employee_service = EmployeeService(db)
    employee = employee_service.update_employee(employee_id, employee_update)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return employee

@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: EmployeeModel = Depends(get_current_admin_user)
):
    """Delete employee (Admin only)"""
    employee_service = EmployeeService(db)
    success = employee_service.delete_employee(employee_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return {"message": "Employee deactivated successfully"}

@router.get("/{employee_id}/balance")
def get_employee_balance(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: EmployeeModel = Depends(get_current_user)
):
    """Get employee's leave balance"""
    if current_user.id != employee_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    employee_service = EmployeeService(db)
    employee = employee_service.get_employee(employee_id)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return {"employee_id": employee_id, "leave_balance": employee.leave_balance}