from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from models import User, Faculty, FacultyDesignation
import database

from middleware import permission_required

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
    designation: FacultyDesignationEnum
    department: str
    expertise: List[str]
    office: Optional[str] = None
    image: Optional[str] = None
    website: Optional[str] = None
    publications: int = 0
    experience: int = 0
    rating: float = 0.0
    is_chairman: bool = False
    bio: Optional[str] = None
    short_bio: Optional[str] = None
    education: Optional[List[str]] = None
    courses: Optional[List[str]] = None
    research_interests: Optional[List[str]] = None
    recent_publications: Optional[List[dict]] = None
    awards: Optional[List[str]] = None
    office_hours: Optional[str] = None

    class Config:
        from_attributes = True

class FacultyCreate(FacultyBase):
    pass

class Publication(BaseModel):
    title: str
    journal: str
    year: int
    doi: Optional[str] = None

from fastapi import Body

class FacultyResponse(FacultyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.put("/{faculty_id}/update", response_model=FacultyResponse)
async def update_faculty_profile(
    faculty_id: int,
    faculty_update: FacultyBase = Body(...),
    officer: dict = Depends(permission_required("CREATE_USER")),
    db: Session = Depends(database.get_db)
):
    user = db.query(User).filter(User.id == faculty_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Faculty not found")

    newFaculty = Faculty(
        id=faculty_id,
        designation=faculty_update.designation,
        department=faculty_update.department,
        expertise=faculty_update.expertise,
        office=faculty_update.office,
        image=faculty_update.image,
        website=faculty_update.website,
        publications=faculty_update.publications,
        experience=faculty_update.experience,
        rating=faculty_update.rating,
        is_chairman=faculty_update.is_chairman,
        bio=faculty_update.bio,
        short_bio=faculty_update.short_bio,
        education=faculty_update.education,
        courses=faculty_update.courses,
        research_interests=faculty_update.research_interests,
        recent_publications=faculty_update.recent_publications,
        awards=faculty_update.awards,
        office_hours=faculty_update.office_hours,
    )
    db.add(newFaculty)
    db.commit()
    db.refresh(newFaculty)
    return newFaculty

    
    

class FacultyListResponse(BaseModel):
    faculty: List[FacultyResponse]
    roles: List[str]
    expertise_areas: List[str]

    class Config:
        from_attributes = True

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
    faculty = query.all()
    
    # Get unique roles and expertise areas for filters
    roles = [d.value for d in FacultyDesignation]
    
    # Get unique expertise areas (flatten all expertise lists and get unique values)
    expertise_areas = set()
    for f in faculty:
        if f.expertise:
            if isinstance(f.expertise, list):
                expertise_areas.update(f.expertise)
            elif isinstance(f.expertise, str):
                try:
                    import json
                    expertise_areas.update(json.loads(f.expertise))
                except Exception:
                    pass
    
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
    
    # Ensure all required fields have values
    for key in ["recent_publications", "awards", "education", "courses", "research_interests", "expertise"]:
        if faculty_dict.get(key) is None:
            faculty_dict[key] = []
    
    return {"faculty": faculty_dict}
