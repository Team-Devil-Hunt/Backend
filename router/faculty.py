from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

from models import Faculty, FacultyDesignation
import database

router = APIRouter(
    prefix="/api/faculty",
    tags=["faculty"],
    responses={404: {"description": "Not found"}},
)

# Request/Response Models
class FacultyDesignationEnum(str, Enum):
    PROFESSOR = "Professor"
    ASSOCIATE_PROFESSOR = "Associate Professor"
    ASSISTANT_PROFESSOR = "Assistant Professor"
    LECTURER = "Lecturer"

class FacultyBase(BaseModel):
    name: str
    designation: FacultyDesignationEnum
    department: str
    expertise: List[str]
    email: str
    phone: Optional[str] = None
    office: Optional[str] = None
    image: Optional[str] = None
    website: Optional[str] = None
    publications: int = 0
    experience: int = 0
    is_chairman: bool = False
    bio: Optional[str] = None
    education: Optional[List[str]] = None
    courses: Optional[List[str]] = None
    research_interests: Optional[List[str]] = None

class FacultyCreate(FacultyBase):
    pass

class Publication(BaseModel):
    title: str
    journal: str
    year: int
    doi: Optional[str] = None

class FacultyResponse(FacultyBase):
    id: int
    rating: float = 0.0
    short_bio: Optional[str] = None
    recent_publications: Optional[List[Publication]] = None
    awards: Optional[List[str]] = None
    office_hours: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class FacultyListResponse(BaseModel):
    faculty: List[FacultyResponse]
    roles: List[str]
    expertise_areas: List[str]

# Helper function to convert FacultyDesignation
# Routes
@router.get("", response_model=FacultyListResponse)
async def get_faculty(
    department: Optional[str] = None,
    designation: Optional[FacultyDesignationEnum] = None,
    db: Session = Depends(database.get_db)
):
    """
    Get all faculty members with optional filtering by department and designation.
    Public endpoint - no authentication required.
    """
    # Build query
    query = db.query(Faculty)
    
    if department:
        query = query.filter(Faculty.department.ilike(f"%{department}%"))
    
    if designation:
        query = query.filter(Faculty.designation == designation)
    
    # Execute query
    faculty = query.order_by(Faculty.name).all()
    
    # Get unique roles and expertise areas for filters
    roles = [d.value for d in FacultyDesignation]
    
    # Get unique expertise areas (flatten all expertise lists and get unique values)
    expertise_areas = set()
    for f in faculty:
        if f.expertise:
            expertise_areas.update(f.expertise)
    
    return {
        "faculty": faculty,
        "roles": sorted(roles),
        "expertise_areas": sorted(list(expertise_areas))
    }


@router.get("/{faculty_id}", response_model=Dict[str, Any])
async def get_faculty_profile(
    faculty_id: int = Path(..., title="The ID of the faculty member to get"),
    db: Session = Depends(database.get_db)
):
    """
    Get detailed profile of a specific faculty member by ID.
    Public endpoint - no authentication required.
    """
    # Query the faculty member
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Faculty member with ID {faculty_id} not found"
        )
    
    # Convert SQLAlchemy model to dict
    faculty_dict = {}
    for column in Faculty.__table__.columns:
        faculty_dict[column.name] = getattr(faculty, column.name)
    
    # Add the role name
    faculty_dict["role"] = faculty.designation.value
    
    # Ensure all required fields have values
    if faculty_dict.get("recent_publications") is None:
        faculty_dict["recent_publications"] = []
    if faculty_dict.get("awards") is None:
        faculty_dict["awards"] = []
    if faculty_dict.get("education") is None:
        faculty_dict["education"] = []
    if faculty_dict.get("courses") is None:
        faculty_dict["courses"] = []
    if faculty_dict.get("research_interests") is None:
        faculty_dict["research_interests"] = []
    if faculty_dict.get("expertise") is None:
        faculty_dict["expertise"] = []
    
    return {"faculty": faculty_dict}
