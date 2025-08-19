from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
from app.db.models.leave import LeaveRequest, LeaveStatus
from app.db.models.employee import Employee
from app.schemas.leave import LeaveRequestCreate, LeaveRequestUpdate
from app.services.employee_service import EmployeeService

class LeaveService:
    def __init__(self, db: Session):
        self.db = db
        self.employee_service = EmployeeService(db)
    
    def _calculate_business_days(self, start_date: date, end_date: date) -> int:
        """Calculate business days between two dates (excluding weekends)"""
        total_days = 0
        current_date = start_date
        
        while current_date <= end_date:
            
            if current_date.weekday() < 5:  
                total_days += 1
            current_date = datetime(current_date.year, current_date.month, current_date.day)
            current_date = current_date.replace(day=current_date.day + 1).date()
        
        return total_days
    
    def _check_overlapping_leaves(self, employee_id: int, start_date: date, end_date: date, exclude_request_id: int = None) -> bool:
        """Check if there are overlapping approved/pending leave requests"""
        query = self.db.query(LeaveRequest).filter(
            and_(
                LeaveRequest.employee_id == employee_id,
                LeaveRequest.status.in_([LeaveStatus.PENDING, LeaveStatus.APPROVED]),
                or_(
                    and_(LeaveRequest.start_date <= start_date, LeaveRequest.end_date >= start_date),
                    and_(LeaveRequest.start_date <= end_date, LeaveRequest.end_date >= end_date),
                    and_(LeaveRequest.start_date >= start_date, LeaveRequest.end_date <= end_date)
                )
            )
        )
        
        if exclude_request_id:
            query = query.filter(LeaveRequest.id != exclude_request_id)
        
        return query.first() is not None
    
    def create_leave_request(self, leave_data: LeaveRequestCreate) -> LeaveRequest:
        """Create a new leave request with validation"""
        employee = self.employee_service.get_employee(leave_data.employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        
        if not employee.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot apply leave for inactive employee"
            )
        
        if leave_data.end_date <= leave_data.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End date must be after start date"
            )
        
        if leave_data.start_date < employee.joining_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot apply for leave before joining date"
            )
        
        
        days_requested = self._calculate_business_days(leave_data.start_date, leave_data.end_date)
        
        if days_requested <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid leave duration"
            )
        
        if days_requested > employee.leave_balance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient leave balance. Available: {employee.leave_balance} days, Requested: {days_requested} days"
            )
        
        
        if self._check_overlapping_leaves(leave_data.employee_id, leave_data.start_date, leave_data.end_date):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Overlapping leave request exists"
            )
        
        
        db_leave_request = LeaveRequest(
            employee_id=leave_data.employee_id,
            start_date=leave_data.start_date,
            end_date=leave_data.end_date,
            leave_type=leave_data.leave_type,
            reason=leave_data.reason,
            days_requested=days_requested
        )
        
        self.db.add(db_leave_request)
        self.db.commit()
        self.db.refresh(db_leave_request)
        return db_leave_request
    
    def get_leave_request(self, leave_id: int) -> Optional[LeaveRequest]:
        """Get leave request by ID"""
        return self.db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    
    def get_leave_requests(self, employee_id: int = None, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
        """Get leave requests with optional employee filter"""
        query = self.db.query(LeaveRequest)
        if employee_id:
            query = query.filter(LeaveRequest.employee_id == employee_id)
        return query.offset(skip).limit(limit).all()
    
    def approve_leave_request(self, leave_id: int, admin_comment: str = None) -> Optional[LeaveRequest]:
        """Approve a leave request"""
        leave_request = self.get_leave_request(leave_id)
        if not leave_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found"
            )
        
        if leave_request.status != LeaveStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending leave requests can be approved"
            )
        
        
        leave_request.status = LeaveStatus.APPROVED
        leave_request.admin_comment = admin_comment
        

        employee = self.employee_service.get_employee(leave_request.employee_id)
        if employee:
            employee.leave_balance -= leave_request.days_requested
        
        self.db.commit()
        self.db.refresh(leave_request)
        return leave_request
    
    def reject_leave_request(self, leave_id: int, admin_comment: str = None) -> Optional[LeaveRequest]:
        """Reject a leave request"""
        leave_request = self.get_leave_request(leave_id)
        if not leave_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found"
            )
        
        if leave_request.status != LeaveStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending leave requests can be rejected"
            )
        
        leave_request.status = LeaveStatus.REJECTED
        leave_request.admin_comment = admin_comment
        
        self.db.commit()
        self.db.refresh(leave_request)
        return leave_request
    
    def get_employee_leave_balance(self, employee_id: int) -> float:
        """Get employee's current leave balance"""
        employee = self.employee_service.get_employee(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        return employee.leave_balance