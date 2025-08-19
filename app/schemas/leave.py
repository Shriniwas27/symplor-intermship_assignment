from datetime import date
from typing import Optional
from pydantic import BaseModel, validator
from app.db.models.leave import LeaveType, LeaveStatus


class LeaveRequestBase(BaseModel):
    start_date: date
    end_date: date
    leave_type: LeaveType
    reason: Optional[str] = None
    
    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class LeaveRequestCreate(LeaveRequestBase):
    employee_id: int

class LeaveRequestUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    leave_type: Optional[LeaveType] = None
    reason: Optional[str] = None

class LeaveRequestAction(BaseModel):
    admin_comment: Optional[str] = None

class LeaveRequest(LeaveRequestBase):
    id: int
    employee_id: int
    status: LeaveStatus
    days_requested: int
    admin_comment: Optional[str] = None
    
    class Config:
        from_attributes = True

class LeaveRequestWithEmployee(LeaveRequest):
    employee: "Employee" = None


from app.schemas.employee import Employee
LeaveRequestWithEmployee.model_rebuild()