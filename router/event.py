from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

from models import Event, EventRegistration, EventType, EventStatus, User, Role
import database
from middleware import permission_required

router = APIRouter(
    prefix="/api/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)

# Request/Response Models
class EventTypeEnum(str, Enum):
    SEMINAR = 'seminar'
    WORKSHOP = 'workshop'
    CONFERENCE = 'conference'
    COMPETITION = 'competition'
    CULTURAL = 'cultural'
    ACADEMIC = 'academic'

class EventStatusEnum(str, Enum):
    UPCOMING = 'upcoming'
    ONGOING = 'ongoing'
    REGISTRATION_OPEN = 'registration_open'
    REGISTRATION_CLOSED = 'registration_closed'
    COMPLETED = 'completed'

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: EventTypeEnum
    status: EventStatusEnum
    start_date: datetime
    end_date: datetime
    venue: str
    speaker: Optional[str] = None
    max_participants: Optional[int] = None
    registration_required: bool = False
    registration_deadline: Optional[datetime] = None
    fee: Optional[float] = None
    external_link: Optional[str] = None
    tags: Optional[List[str]] = []

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    organizer: str
    registered_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RegistrationRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    student_id: Optional[str] = None
    department: Optional[str] = None
    year: Optional[str] = None
    special_requirements: Optional[str] = None

class RegistrationResponse(BaseModel):
    success: bool
    registration_id: int
    message: str

# Helper function to convert EventType and EventStatus enums
def convert_event_type(event_type: EventTypeEnum) -> EventType:
    return EventType[event_type.name]

def convert_event_status(status: EventStatusEnum) -> EventStatus:
    return EventStatus[status.name]

# Routes
@router.get("", response_model=List[EventResponse])
async def get_events(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    """Get all events with optional pagination (Public endpoint)"""
    events = db.query(Event).offset(skip).limit(limit).all()
    
    # Convert each event to a dictionary and add the organizer field
    result = []
    for event in events:
        event_dict = {c.name: getattr(event, c.name) for c in event.__table__.columns}
        # Get the organizer's name from the role
        organizer_role = db.query(Role).filter(Role.id == event.organizer_role_id).first()
        event_dict['organizer'] = organizer_role.name if organizer_role else 'Unknown Organizer'
        result.append(event_dict)
    
    return result

@router.post("", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    current_user: dict = Depends(permission_required("MANAGE_EVENTS")),
    db: Session = Depends(database.get_db)
):
    """Create a new event (Requires MANAGE_EVENTS permission)"""
    # Debug: Print current_user to see what we're getting
    print("Current User:", current_user)
    
    # Debug: Print current_user to see what we're getting
    print("Current User:", current_user)
    
    # Get role_id from the nested role structure
    try:
        role_id = current_user.get('role', {}).get('id')
        if not role_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User role not found in token"
            )
        
        # Convert the role_id to integer if it's a string
        role_id = int(role_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user role structure in token"
        )
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role_id format in token"
        )
    
    db_event = Event(
        **event.dict(exclude={"type", "status"}),
        type=convert_event_type(event.type),
        status=convert_event_status(event.status),
        organizer_role_id=role_id,  # Use the validated role_id
        registered_count=0
    )
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # Get the organizer's role name
    organizer_role = db.query(Role).filter(Role.id == db_event.organizer_role_id).first()
    organizer_name = organizer_role.name if organizer_role else 'Unknown Organizer'
    
    # Convert to dict and add the organizer's name
    response_data = {c.name: getattr(db_event, c.name) for c in db_event.__table__.columns}
    response_data['organizer'] = organizer_name
    
    return response_data

@router.post("/{event_id}/register", response_model=RegistrationResponse)
async def register_for_event(
    event_id: int,
    registration: RegistrationRequest,
    current_user: dict = Depends(permission_required("REGISTER_EVENT")),
    db: Session = Depends(database.get_db)
):
    """Register for an event (Requires REGISTER_EVENT permission)"""
    
    # Check if event exists and registration is open
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if event.registration_required and event.status != EventStatus.REGISTRATION_OPEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration is not open for this event"
        )
    
    if event.registration_deadline and event.registration_deadline < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration deadline has passed"
        )
    
    if event.max_participants and event.registered_count >= event.max_participants:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is at full capacity"
        )
    
    # Get user_id from current_user
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID not found in token"
            )
        
        # Check if user is already registered
        existing_registration = db.query(EventRegistration).filter(
            EventRegistration.event_id == event_id,
            EventRegistration.user_id == user_id
        ).first()
        
        if existing_registration:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already registered for this event"
            )
        
        registration_data = registration.dict()
        registration_data.update({
            "event_id": event_id,
            "user_id": user_id  # Use the extracted user_id
        })
        
    except Exception as e:
        # Re-raise HTTPException as is
        if isinstance(e, HTTPException):
            raise
        # Convert other exceptions to 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your registration: {str(e)}"
        )
    
    db_registration = EventRegistration(**registration_data)
    db.add(db_registration)
    # Update the registered count
    event.registered_count += 1
    db.commit()
    db.refresh(db_registration)
    
    # Ensure the response matches the RegistrationResponse model
    return RegistrationResponse(
        success=True,
        registration_id=db_registration.id,
        message="Successfully registered for the event"
    )
