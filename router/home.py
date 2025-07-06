from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from enum import Enum

from models import User, Role
from typing import Optional, Any

# Try to import optional models
try:
    from models import Announcement, AnnouncementType
except ImportError:
    # If models don't exist, create dummy classes to prevent errors
    class Announcement:
        pass
    
    class AnnouncementType:
        ACADEMIC = 'academic'
import database

router = APIRouter(
    prefix="/api",
    tags=["home"],
    responses={404: {"description": "Not found"}},
)

# Request/Response Models
class StatsResponse(BaseModel):
    students: int
    faculty: int
    programs: int
    research: int

class OverviewResponse(BaseModel):
    title: str
    description: Optional[str] = None
    stats: StatsResponse
    heroImage: Optional[str] = None

    class Config:
        from_attributes = True

class AnnouncementResponse(BaseModel):
    id: int
    title: str
    content: str
    date: datetime
    type: str
    priority: str
    image: Optional[str] = None

    class Config:
        from_attributes = True

class QuickLinkResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    href: str
    icon: Optional[str] = None
    category: str

    class Config:
        from_attributes = True

# Routes
@router.get("/overview", response_model=OverviewResponse)
async def get_overview(db: Session = Depends(database.get_db)):
    """
    Get home page overview data with actual user counts based on roles.
    Public endpoint - no authentication required.
    """
    # Default values
    title = "Welcome to Our Department"
    description = "Leading in education and research excellence"
    hero_image = "/images/default-hero.jpg"
    
    # Get role names for students and faculty
    student_roles = db.query(Role).filter(Role.name.ilike('%student%')).all()
    faculty_roles = db.query(Role).filter(
        Role.name.ilike('%faculty%') | 
        Role.name.ilike('%teacher%') | 
        Role.name.ilike('%professor%') |
        Role.name.ilike('%lecturer%')
    ).all()
    
    # Get role IDs
    student_role_ids = [role.id for role in student_roles]
    faculty_role_ids = [role.id for role in faculty_roles]
    
    # Count users by role
    student_count = db.query(User).filter(User.role_id.in_(student_role_ids)).count() if student_role_ids else 0
    faculty_count = db.query(User).filter(User.role_id.in_(faculty_role_ids)).count() if faculty_role_ids else 0
    
    # Initialize default counts
    research_count = 0
    programs_count = 0
    
    # Try to get user counts (students and faculty)
    try:
        # Get student and faculty counts from users table
        student_count = db.query(User).filter(User.role_id.in_(student_role_ids)).count() if student_role_ids else 0
        faculty_count = db.query(User).filter(User.role_id.in_(faculty_role_ids)).count() if faculty_role_ids else 0
        
        # Get program count (using role count as a placeholder)
        programs_count = db.query(Role).count()
        
        # Try to get research count if announcements table exists
        try:
            research_count = db.query(Announcement).filter(Announcement.type == AnnouncementType.ACADEMIC).count()
        except:
            # If announcements table doesn't exist, use a default value
            research_count = 0
            
    except Exception as e:
        # If any database error occurs, use default values
        student_count = 0
        faculty_count = 0
        research_count = 0
        programs_count = 0
    
    return {
        "title": title,
        "description": description,
        "stats": {
            "students": student_count,
            "faculty": faculty_count,
            "programs": programs_count,
            "research": research_count
        },
        "heroImage": hero_image
    }

@router.get("/announcements", response_model=List[AnnouncementResponse])
async def get_announcements(
    limit: int = 10,
    type: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    """
    Get list of announcements.
    Public endpoint - no authentication required.
    Returns empty list if announcements table doesn't exist.
    """
    try:
        query = db.query(Announcement)
        
        # Apply filters if provided
        if type:
            query = query.filter(Announcement.type == type)
        if priority:
            query = query.filter(Announcement.priority == priority)
        
        # Get most recent announcements first
        announcements = query.order_by(Announcement.date.desc()).limit(limit).all()
        return announcements
        
    except Exception as e:
        # If any error occurs (e.g., table doesn't exist), return empty list
        return []

@router.get("/quick-links", response_model=List[QuickLinkResponse])
async def get_quick_links(
    category: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(database.get_db)
):
    """
    Get list of quick links.
    Public endpoint - no authentication required.
    Returns empty list if quick_links table doesn't exist.
    """
    try:
        query = db.query(QuickLink)
        
        # Apply category filter if provided
        if category:
            query = query.filter(QuickLink.category == category)
        
        # Get most recently added links first
        links = query.order_by(QuickLink.created_at.desc()).limit(limit).all()
        return links
        
    except Exception as e:
        # If any error occurs (e.g., table doesn't exist), return empty list
        return []
