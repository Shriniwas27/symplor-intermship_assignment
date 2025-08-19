from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.leave import LeaveRequest, LeaveRequestCreate, LeaveRequestAction
from app.services.leave_service import LeaveService
from app.api.dependencies import get_current_admin_user, get_current_user
from app.db.models.employee import Employee as EmployeeModel

router = APIRouter()

@router.post("/", response_model=LeaveRequest, status_code=status.HTTP_201_CREATED)
def create_leave_request(
    leave_request: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: EmployeeModel = Depends(get_current_user)
):
    """Apply for leave"""

    if not current_user.is_admin and leave_request.employee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only apply for your own leave"
        )
    
    leave_service = LeaveService(db)
    return leave_service.create_leave_request(leave_request)

@router.get("/", response_model=List[LeaveRequest])
def read_leave_requests(
    employee_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: EmployeeModel = Depends(get_current_user)
):
    """Get leave requests"""
    leave_service = LeaveService(db)
    
    if not current_user.is_admin:
        employee_id = current_user.id
    
    return leave_service.get_leave_requests(employee_id=employee_id, skip=skip, limit=limit)

@router.get("/me", response_model=List[LeaveRequest])
def read_my_leave_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: EmployeeModel = Depends(get_current_user)
):
    """Get current user's leave requests"""
    leave_service = LeaveService(db)
    return leave_service.get_leave_requests(employee_id=current_user.id, skip=skip, limit=limit)

@router.get("/{leave_id}", response_model=LeaveRequest)
def read_leave_request(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: EmployeeModel = Depends(get_current_user)
):
    """Get leave request by ID"""
    leave_service = LeaveService(db)
    leave_request = leave_service.get_leave_request(leave_id)
    
    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )
    
    
    if not current_user.is_admin and leave_request.employee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return leave_request

@router.post("/{leave_id}/approve", response_model=LeaveRequest)
def approve_leave_request(
    leave_id: int,
    action: LeaveRequestAction,
    db: Session = Depends(get_db),
    current_admin: EmployeeModel = Depends(get_current_admin_user)
):
    """Approve leave request (Admin only)"""
    leave_service = LeaveService(db)
    return leave_service.approve_leave_request(leave_id, action.admin_comment)

@router.post("/{leave_id}/reject", response_model=LeaveRequest)
def reject_leave_request(
    leave_id: int,
    action: LeaveRequestAction,
    db: Session = Depends(get_db),
    current_admin: EmployeeModel = Depends(get_current_admin_user)
):
    """Reject leave request (Admin only)"""
    leave_service = LeaveService(db)
    return leave_service.reject_leave_request(leave_id, action.admin_comment)