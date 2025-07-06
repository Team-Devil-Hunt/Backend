from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Float

from sqlalchemy import Table, Enum
from sqlalchemy.dialects.postgresql import JSON
from enum import Enum as PyEnum
from sqlalchemy import Text

class EventType(str, PyEnum):
    SEMINAR = 'seminar'
    WORKSHOP = 'workshop'
    CONFERENCE = 'conference'
    COMPETITION = 'competition'
    CULTURAL = 'cultural'
    ACADEMIC = 'academic'

class EventStatus(str, PyEnum):
    UPCOMING = 'upcoming'
    ONGOING = 'ongoing'
    REGISTRATION_OPEN = 'registration_open'
    REGISTRATION_CLOSED = 'registration_closed'
    COMPLETED = 'completed'


class AdmissionStats(Base):
    __tablename__ = "admission_stats"
    id = Column(Integer, primary_key=True, index=True)
    next_deadline = Column(String, nullable=False)
    programs_offered = Column(Integer, nullable=False)
    application_time = Column(String, nullable=False)
    acceptance_rate = Column(String, nullable=False)

class AdmissionDeadline(Base):
    __tablename__ = "admission_deadlines"
    id = Column(Integer, primary_key=True, index=True)
    program = Column(String, nullable=False)
    level = Column(String, nullable=False)  # Undergraduate/Graduate/Postgraduate
    date = Column(DateTime, nullable=False)
    requirements = Column(String, nullable=False)
    notes = Column(String, nullable=True)

class AdmissionFAQ(Base):
    __tablename__ = "admission_faqs"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(String, nullable=False)

class Award(Base):
    __tablename__ = "awards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    details = Column(String, nullable=True)
    recipient = Column(String, nullable=False)
    recipient_type = Column(String, nullable=False)  # 'faculty' | 'student'
    year = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # 'award' | 'grant' | ...
    organization = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    department = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    categories = Column(JSON, nullable=True)
    publications = Column(JSON, nullable=True)
    link = Column(String, nullable=True)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    expires = Column(Float, nullable=False)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    users = relationship("User", back_populates="role")
    permissions = relationship("RolePermission", back_populates="role")
    events = relationship("Event", back_populates="organizer_role")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)

    roles = relationship("RolePermission", back_populates="permission")


class RolePermission(Base):
    __tablename__ = "roles_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    username = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="users")



class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type = Column(Enum(EventType), nullable=False)
    status = Column(Enum(EventStatus), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    venue = Column(String, nullable=False)
    speaker = Column(String, nullable=True)
    organizer_role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    max_participants = Column(Integer, nullable=True)
    registered_count = Column(Integer, default=0)
    registration_required = Column(Boolean, default=False)
    registration_deadline = Column(DateTime, nullable=True)
    fee = Column(Float, nullable=True)
    external_link = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organizer_role = relationship("Role", back_populates="events")
    registrations = relationship("EventRegistration", back_populates="event")


class EventRegistration(Base):
    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    student_id = Column(String, nullable=True)
    department = Column(String, nullable=True)
    year = Column(String, nullable=True)
    special_requirements = Column(String, nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    
    event = relationship("Event", back_populates="registrations")
    user = relationship("User")


class ForgotPassword(Base):
    __tablename__ = "forgot_password"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, nullable=False)
    expires = Column(Float, nullable=False)


class FacultyDesignation(str, PyEnum):
    PROFESSOR = "Professor"
    ASSOCIATE_PROFESSOR = "Associate Professor"
    ASSISTANT_PROFESSOR = "Assistant Professor"
    LECTURER = "Lecturer"


class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    designation = Column(Enum(FacultyDesignation), nullable=False)
    department = Column(String, nullable=False)
    expertise = Column(JSON, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    office = Column(String, nullable=True)
    image = Column(String, nullable=True)
    website = Column(String, nullable=True)
    publications = Column(Integer, default=0)
    experience = Column(Integer, default=0)  # years of experience
    rating = Column(Float, default=0.0)
    is_chairman = Column(Boolean, default=False)
    bio = Column(Text, nullable=True)
    short_bio = Column(Text, nullable=True)
    education = Column(JSON, nullable=True)  # List of degrees
    courses = Column(JSON, nullable=True)    # List of courses taught
    research_interests = Column(JSON, nullable=True)  # List of research interests
    recent_publications = Column(JSON, nullable=True)  # List of publications
    awards = Column(JSON, nullable=True)  # List of awards
    office_hours = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


