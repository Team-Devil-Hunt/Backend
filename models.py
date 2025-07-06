from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Float

from sqlalchemy import Table

from sqlalchemy.dialects.postgresql import JSON


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



class ForgotPassword(Base):
    __tablename__ = "forgot_password"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, nullable=False)
    expires = Column(Float, nullable=False)


