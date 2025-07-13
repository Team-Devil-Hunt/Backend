from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, time
import re

from database import get_db
from models import ClassSchedule, ClassType, ClassStatus, User, Faculty, FacultyDesignation, Course
from middleware import permission_required

router = APIRouter(
    prefix="/api/schedule",
    tags=["schedule"],
)

# Pydantic models for request and response
class ClassScheduleBase(BaseModel):
    courseCode: str
    courseName: str
    type: str  # "Lecture" | "Lab" | "Tutorial"
    batch: str
    semester: str
    day: str
    startTime: str
    endTime: str
    room: str
    instructorId: int
    status: str = "Upcoming"  # "In Progress" | "Upcoming" | "Completed" | "Cancelled"

class ClassScheduleCreate(ClassScheduleBase):
    pass

class ClassScheduleResponse(ClassScheduleBase):
    id: str
    instructorName: str
    instructorDesignation: str
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        # Format datetime objects to time strings (HH:MM)
        start_time = obj.start_time.strftime("%H:%M") if obj.start_time else ""
        end_time = obj.end_time.strftime("%H:%M") if obj.end_time else ""
        
        return cls(
            id=str(obj.id),
            courseCode=obj.course_code,
            courseName=obj.course_name,
            type=obj.type.value,
            batch=obj.batch,
            semester=obj.semester,
            day=obj.day,
            startTime=start_time,
            endTime=end_time,
            room=obj.room,
            instructorId=obj.instructor_id,
            instructorName=obj.instructor_name,
            instructorDesignation=obj.instructor_designation,
            status=obj.status.value
        )

class ClassesListResponse(BaseModel):
    classes: List[ClassScheduleResponse]
    batches: List[str]
    semesters: List[str]
    rooms: List[str]


@router.get("", response_model=ClassesListResponse)
async def get_classes(
    db: Session = Depends(get_db),
    batch: Optional[str] = None,
    semester: Optional[str] = None,
    room: Optional[str] = None,
    day: Optional[str] = None,
    status: Optional[str] = None
):

    """
    Get all class schedules with optional filtering
    """
    query = db.query(ClassSchedule)
    
    # Apply filters if provided
    if batch:
        query = query.filter(ClassSchedule.batch == batch)
    if semester:
        query = query.filter(ClassSchedule.semester == semester)
    if room:
        query = query.filter(ClassSchedule.room == room)
    if day:
        query = query.filter(ClassSchedule.day == day)
    if status:
        query = query.filter(ClassSchedule.status == status)
    
    # Get the class schedules
    classes = query.all()
    
    # Get distinct values for filters
    batches = [batch[0] for batch in db.query(distinct(ClassSchedule.batch)).all()]
    semesters = [semester[0] for semester in db.query(distinct(ClassSchedule.semester)).all()]
    rooms = [room[0] for room in db.query(distinct(ClassSchedule.room)).all()]
    
    # Convert to response model
    class_responses = [ClassScheduleResponse.from_orm(cls) for cls in classes]
    
    return ClassesListResponse(
        classes=class_responses,
        batches=batches,
        semesters=semesters,
        rooms=rooms
    )


@router.post("", response_model=ClassScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_class(
    class_data: ClassScheduleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(permission_required("MANAGE_NOTICES"))
):
    """
    Create a new class schedule (requires MANAGE_NOTICES permission)
    """
    
    # Check if course exists
    course = db.query(Course).filter(Course.code == class_data.courseCode).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with code '{class_data.courseCode}' not found"
        )
    
    # Get instructor details
    instructor = db.query(User).filter(User.id == class_data.instructorId).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    
    # Get instructor designation
    faculty = db.query(Faculty).filter(Faculty.id == instructor.id).first()
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instructor is not a faculty member"
        )
    
    # Parse time strings to datetime objects
    try:
        # Convert time strings like "14:30" to datetime objects
        start_time = datetime.strptime(class_data.startTime, "%H:%M")
        end_time = datetime.strptime(class_data.endTime, "%H:%M")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid time format. Use HH:MM format (24-hour)"
        )
    
    # Create new class schedule
    db_class = ClassSchedule(
        course_code=class_data.courseCode,
        course_name=class_data.courseName,
        type=class_data.type,
        batch=class_data.batch,
        semester=class_data.semester,
        day=class_data.day,
        start_time=start_time,
        end_time=end_time,
        room=class_data.room,
        instructor_id=class_data.instructorId,
        instructor_name=instructor.name,
        instructor_designation=faculty.designation.value,
        status=class_data.status
    )
    
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    
    return ClassScheduleResponse.from_orm(db_class)


@router.put("/{class_id}", response_model=ClassScheduleResponse)
async def update_class(
    class_id: int,
    class_data: ClassScheduleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(permission_required("MANAGE_NOTICES"))
):
    """
    Update a class schedule (requires MANAGE_NOTICES permission)
    """
    
    
    # Get the class schedule
    db_class = db.query(ClassSchedule).filter(ClassSchedule.id == class_id).first()
    if not db_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class schedule not found"
        )
    
    # Get instructor details if changed
    if db_class.instructor_id != class_data.instructorId:
        instructor = db.query(User).filter(User.id == class_data.instructorId).first()
        if not instructor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Instructor not found"
            )
        
        # Get instructor designation
        faculty = db.query(Faculty).filter(Faculty.id == instructor.id).first()
        if not faculty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Instructor is not a faculty member"
            )
        
        db_class.instructor_id = class_data.instructorId
        db_class.instructor_name = instructor.name
        db_class.instructor_designation = faculty.designation.value
    
    # Parse time strings to datetime objects
    try:
        # Convert time strings like "14:30" to datetime objects
        start_time = datetime.strptime(class_data.startTime, "%H:%M")
        end_time = datetime.strptime(class_data.endTime, "%H:%M")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid time format. Use HH:MM format (24-hour)"
        )
    
    # Update other fields
    db_class.course_code = class_data.courseCode
    db_class.course_name = class_data.courseName
    db_class.type = class_data.type
    db_class.batch = class_data.batch
    db_class.semester = class_data.semester
    db_class.day = class_data.day
    db_class.start_time = start_time
    db_class.end_time = end_time
    db_class.room = class_data.room
    db_class.status = class_data.status
    
    db.commit()
    db.refresh(db_class)
    
    return ClassScheduleResponse.from_orm(db_class)


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(permission_required("MANAGE_NOTICES"))
):
    """
    Delete a class schedule (requires MANAGE_NOTICES permission)
    """
    
    
    # Get the class schedule
    db_class = db.query(ClassSchedule).filter(ClassSchedule.id == class_id).first()
    if not db_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class schedule not found"
        )
    
    # Delete the class schedule
    db.delete(db_class)
    db.commit()
    
    return None
