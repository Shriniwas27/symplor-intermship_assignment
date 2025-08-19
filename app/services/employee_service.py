from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.db.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.core.security import get_password_hash

class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        """Create a new employee"""
        
        existing_employee = self.db.query(Employee).filter(Employee.email == employee_data.email).first()
        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee with this email already exists"
            )
        
        
        db_employee = Employee(
            name=employee_data.name,
            email=employee_data.email,
            department=employee_data.department,
            joining_date=employee_data.joining_date,
            is_admin=employee_data.is_admin or False
        )
        
       
        if employee_data.password:
            db_employee.hashed_password = get_password_hash(employee_data.password)
        
        try:
            self.db.add(db_employee)
            self.db.commit()
            self.db.refresh(db_employee)
            return db_employee
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee creation failed"
            )
    
    def get_employee(self, employee_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        return self.db.query(Employee).filter(Employee.id == employee_id).first()
    
    def get_employee_by_email(self, email: str) -> Optional[Employee]:
        """Get employee by email"""
        return self.db.query(Employee).filter(Employee.email == email).first()
    
    def get_employees(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Employee]:
        """Get list of employees"""
        query = self.db.query(Employee)
        if active_only:
            query = query.filter(Employee.is_active == True)
        return query.offset(skip).limit(limit).all()
    
    def update_employee(self, employee_id: int, employee_update: EmployeeUpdate) -> Optional[Employee]:
        """Update employee"""
        employee = self.get_employee(employee_id)
        if not employee:
            return None
        
        update_data = employee_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(employee, field, value)
        
        try:
            self.db.commit()
            self.db.refresh(employee)
            return employee
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee update failed"
            )
    
    def delete_employee(self, employee_id: int) -> bool:
        """Soft delete employee (deactivate)"""
        employee = self.get_employee(employee_id)
        if not employee:
            return False
        
        employee.is_active = False
        self.db.commit()
        return True
    
    def update_leave_balance(self, employee_id: int, new_balance: float) -> Optional[Employee]:
        """Update employee leave balance"""
        employee = self.get_employee(employee_id)
        if not employee:
            return None
        
        employee.leave_balance = new_balance
        self.db.commit()
        self.db.refresh(employee)
        return employee