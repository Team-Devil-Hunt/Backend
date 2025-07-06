from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from models import Announcement, AnnouncementType
import database

# Create router
router = APIRouter(
    prefix="/api",
    tags=["announcements"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response validation
class AnnouncementResponse(BaseModel):
    id: int
    title: str
    content: str
    date: datetime
    type: str
    priority: str
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Routes
@router.get("/announcements", response_model=List[AnnouncementResponse])
async def get_announcements(
    limit: int = Query(10, description="Number of announcements to return"),
    type: Optional[str] = Query(None, description="Filter by announcement type"),
    priority: Optional[str] = Query(None, description="Filter by priority level"),
    db: Session = Depends(database.get_db)
):
    """
    Get a list of announcements.
    
    This endpoint returns a paginated list of announcements, with optional filtering by type and priority.
    The announcements are ordered by date in descending order (newest first).
    
    Parameters:
    - limit: Maximum number of announcements to return (default: 10)
    - type: Filter by announcement type (e.g., 'academic', 'admin', 'general')
    - priority: Filter by priority level (e.g., 'high', 'medium', 'low')
    
    Returns:
    - List of announcement objects
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
        # Log the error for debugging
        print(f"Error fetching announcements: {str(e)}")
        # Return empty list if there's an error (e.g., table doesn't exist)
        return []
