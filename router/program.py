from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from enum import Enum

from database import get_db
from models import Program, Course

from middleware import permission_required
# Program schemas
# Valid program levels
VALID_PROGRAM_LEVELS = ["Undergraduate", "Graduate", "Postgraduate"]


class CareerProspect(BaseModel):
    title: str
    description: str
    salary_range: Optional[str] = None
    companies: Optional[List[str]] = None


class ProgramBase(BaseModel):
    title: str
    level: str
    duration: str
    short_description: str
    description: Optional[str] = None
    specializations: Optional[List[str]] = None
    learning_objectives: Optional[List[str]] = None
    career_prospects: Optional[List[CareerProspect]] = None
    
    @field_validator('level')
    def validate_level(cls, v):
        if v not in VALID_PROGRAM_LEVELS:
            raise ValueError(f"Level must be one of {VALID_PROGRAM_LEVELS}")
        return v


class ProgramCreate(ProgramBase):
    pass


class ProgramResponse(ProgramBase):
    id: int
    total_students: int = 0
    total_courses: int = 0
    total_credits: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Computer Science",
                "level": "Undergraduate",
                "duration": "4 years",
                "total_students": 250,
                "total_courses": 40,
                "total_credits": 120,
                "short_description": "A comprehensive program covering all aspects of computer science",
                "description": "This program provides a strong foundation in computer science principles...",
                "specializations": ["Artificial Intelligence", "Data Science", "Cybersecurity"],
                "learning_objectives": ["Develop problem-solving skills", "Master programming languages"],
                "career_prospects": [
                    {
                        "title": "Software Engineer",
                        "description": "Design and develop software applications",
                        "salary_range": "$70,000 - $150,000",
                        "companies": ["Google", "Microsoft", "Amazon"]
                    }
                ],
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }
    }


# Course schemas
# Valid course difficulty levels
VALID_COURSE_DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]


class CourseBase(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    credits: int
    duration: str
    difficulty: str = "Intermediate"
    
    @field_validator('difficulty')
    def validate_difficulty(cls, v):
        if v not in VALID_COURSE_DIFFICULTIES:
            raise ValueError(f"Difficulty must be one of {VALID_COURSE_DIFFICULTIES}")
        return v
    prerequisites: Optional[List[str]] = None
    specialization: Optional[str] = None
    semester: int
    year: int
    program_id: int


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    rating: float = 0.0
    enrolled_students: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "code": "CS101",
                "title": "Introduction to Programming",
                "description": "A foundational course in programming concepts",
                "credits": 3,
                "duration": "16 weeks",
                "difficulty": "Beginner",
                "rating": 4.5,
                "enrolled_students": 120,
                "prerequisites": ["None"],
                "specialization": "Computer Science",
                "semester": 1,
                "year": 2025,
                "program_id": 1,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }
    }

program_router = APIRouter(
    prefix="/api/programs",
    tags=["programs"],
    responses={404: {"description": "Not found"}},
)

course_router = APIRouter(
    prefix="/api/courses",
    tags=["courses"],
    responses={404: {"description": "Not found"}},
)


@program_router.get("", response_model=List[ProgramResponse])
async def get_programs(db: Session = Depends(get_db)):
    """
    Get all academic programs
    """
    programs = db.query(Program).all()
    return programs


@program_router.post("", response_model=ProgramResponse, status_code=status.HTTP_201_CREATED)
async def create_program(
    program: ProgramBase,
    db: Session = Depends(get_db),
    current_user: dict = Depends(permission_required("MANAGE_COURSE_PROGRAMS"))
):

    """
    Create a new academic program (requires MANAGE_COURSE_PROGRAMS permission)
    """
    # Convert career_prospects to dict before saving to database

    career_prospects_data = None
    if program.career_prospects:
        career_prospects_data = [cp.model_dump() for cp in program.career_prospects]
    
    # No need for special handling anymore - level is a simple string
    
    # Create the program with all fields - level is now just a string
    db_program = Program(
        title=program.title,
        level=program.level,  # Simple string now
        duration=program.duration,
        short_description=program.short_description,
        description=program.description,
        specializations=program.specializations,
        learning_objectives=program.learning_objectives,
        career_prospects=career_prospects_data
    )
    
    db.add(db_program)
    db.commit()
    
    # Refresh the program using session.refresh instead of raw SQL
    # This should work now that we've set the level correctly
    try:
        db.refresh(db_program)
    except Exception as e:
        # If refresh fails, we'll return the program without refreshing
        # The program has already been committed to the database
        pass
        
    return db_program


@program_router.get("/{program_id}", response_model=ProgramResponse)
async def get_program(program_id: int, db: Session = Depends(get_db)):
    """
    Get a specific academic program by ID
    """
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with ID {program_id} not found"
        )
    return program


@program_router.put("/{program_id}", response_model=ProgramResponse)
async def update_program(
    program_id: int,
    program_update: ProgramCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(permission_required("MANAGE_COURSE_PROGRAMS"))
):
    """
    Update an academic program (requires MANAGE_COURSE_PROGRAMS permission)
    """
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with ID {program_id} not found"
        )
    
    # Get the program data - level is already a string from validation
    program_data = program_update.model_dump()
    
    # Update all attributes
    for key, value in program_data.items():
        setattr(db_program, key, value)
    
    # Commit the changes
    db.commit()
    
    # Try to refresh the program
    try:
        db.refresh(db_program)
    except Exception as e:
        # If refresh fails, we'll return the program without refreshing
        # The program has already been committed to the database
        pass
    return db_program


@program_router.delete("/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(permission_required("MANAGE_COURSE_PROGRAMS"))
):
    """
    Delete an academic program (requires MANAGE_COURSE_PROGRAMS permission)
    """
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with ID {program_id} not found"
        )
    
    # Check if there are courses associated with this program
    courses_count = db.query(Course).filter(Course.program_id == program_id).count()
    if courses_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete program with ID {program_id} as it has {courses_count} courses associated with it"
        )
    
    db.delete(db_program)
    db.commit()
    return None




# Course endpoints
@course_router.get("", response_model=List[CourseResponse])
async def get_courses(db: Session = Depends(get_db)):
    """
    Get all courses
    """
    courses = db.query(Course).all()
    return courses


@course_router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(permission_required("MANAGE_COURSE_PROGRAMS"))
):
    """
    Create a new course (requires MANAGE_COURSE_PROGRAMS permission)
    """
    # Check if program exists
    program = db.query(Program).filter(Program.id == course.program_id).first()
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with ID {course.program_id} not found"
        )
    
    # Check if course code already exists
    existing_course = db.query(Course).filter(Course.code == course.code).first()
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course with code {course.code} already exists"
        )
    
    db_course = Course(**course.model_dump())
    
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    
    # Update program stats
    program.total_courses += 1
    program.total_credits += course.credits
    db.commit()
    
    return db_course


@course_router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    """
    Get a specific course by ID
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found"
        )
    return course


@course_router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_update: CourseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(permission_required("MANAGE_COURSE_PROGRAMS"))
):
    """
    Update a course (requires MANAGE_COURSE_PROGRAMS permission)
    """
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found"
        )
    
    # Check if program exists if program_id is being updated
    if course_update.program_id != db_course.program_id:
        program = db.query(Program).filter(Program.id == course_update.program_id).first()
        if not program:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Program with ID {course_update.program_id} not found"
            )
    
    # Check if course code already exists if code is being updated
    if course_update.code != db_course.code:
        existing_course = db.query(Course).filter(Course.code == course_update.code).first()
        if existing_course:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Course with code {course_update.code} already exists"
            )
    
    # Update course attributes
    for key, value in course_update.model_dump().items():
        setattr(db_course, key, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course


@course_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(permission_required("MANAGE_COURSE_PROGRAMS"))
):
    """
    Delete a course (requires MANAGE_COURSE_PROGRAMS permission)
    """
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found"
        )
    
    # Update program stats
    program = db.query(Program).filter(Program.id == db_course.program_id).first()
    if program:
        program.total_courses -= 1
        program.total_credits -= db_course.credits
        db.commit()
    
    db.delete(db_course)
    db.commit()
    return None
