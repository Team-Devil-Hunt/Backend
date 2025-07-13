from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from models import Assignment, AssignmentSubmission, User
from database import get_db
from middleware import permission_required, get_user_from_session

router = APIRouter(prefix="/api/assignments", tags=["assignments"])

# Pydantic models
class AttachmentSchema(BaseModel):
    name: str
    url: str

class AssignmentBase(BaseModel):
    title: str
    courseCode: str
    courseTitle: str
    semester: int
    batch: str
    deadline: datetime
    description: str
    attachments: Optional[List[AttachmentSchema]] = None
    submissionType: str  # "file" | "link" | "text"
    status: str  # "active" | "past" | "draft"

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: int
    facultyName: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

class SubmissionBase(BaseModel):
    assignmentId: int
    submissionContent: str
    submissionType: str  # "file" | "link" | "text"

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionResponse(SubmissionBase):
    id: int
    studentId: int
    submittedAt: datetime
    status: str
    grade: Optional[float] = None
    feedback: Optional[str] = None
    gradedAt: Optional[datetime] = None

    class Config:
        from_attributes = True

# Routes
@router.get("", response_model=List[AssignmentResponse])
def get_assignments(db: Session = Depends(get_db)):
    """Get all assignments"""
    assignments = db.query(Assignment).all()
    return assignments

@router.get("/{assignment_id}", response_model=AssignmentResponse)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Get a specific assignment by ID"""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.post("", response_model=AssignmentResponse, dependencies=[Depends(permission_required("MANAGE_ASSIGNMENTS"))])
def create_assignment(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_user_from_session)
):
    """Create a new assignment (requires MANAGE_ASSIGNMENTS permission)"""
    # Check if deadline is in the past
    if assignment.deadline < datetime.now():
        raise HTTPException(
            status_code=400, 
            detail="Assignment deadline cannot be in the past"
        )
    
    # Get faculty name from user
    faculty = db.query(User).filter(User.id == user["id"]).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty user not found")
    
    # Create new assignment
    db_assignment = Assignment(
        title=assignment.title,
        courseCode=assignment.courseCode,
        courseTitle=assignment.courseTitle,
        semester=assignment.semester,
        batch=assignment.batch,
        deadline=assignment.deadline,
        description=assignment.description,
        attachments=assignment.attachments,
        submissionType=assignment.submissionType,
        status=assignment.status,
        facultyId=user["id"],
        facultyName=faculty.name
    )
    
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.put("/{assignment_id}", response_model=AssignmentResponse, dependencies=[Depends(permission_required("MANAGE_ASSIGNMENTS"))])
def update_assignment(
    assignment_id: int,
    assignment_update: AssignmentCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_user_from_session)
):
    """Update an existing assignment (requires MANAGE_ASSIGNMENTS permission)"""
    # Find the assignment
    db_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Check if the user is the faculty who created the assignment
    if db_assignment.facultyId != user["id"]:
        raise HTTPException(
            status_code=403, 
            detail="You can only update assignments that you created"
        )
    
    # Update assignment fields
    for field, value in assignment_update.dict().items():
        setattr(db_assignment, field, value)
    
    # Update timestamps
    db_assignment.updatedAt = datetime.utcnow()
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.delete("/{assignment_id}", status_code=204, dependencies=[Depends(permission_required("MANAGE_ASSIGNMENTS"))])
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_user_from_session)
):
    """Delete an assignment (requires MANAGE_ASSIGNMENTS permission)"""
    # Find the assignment
    db_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Check if the user is the faculty who created the assignment
    if db_assignment.facultyId != user["id"]:
        raise HTTPException(
            status_code=403, 
            detail="You can only delete assignments that you created"
        )
    
    # Delete the assignment
    db.delete(db_assignment)
    db.commit()
    return {"detail": "Assignment deleted successfully"}

@router.post("/submit", response_model=SubmissionResponse, dependencies=[Depends(permission_required("SUBMIT_ASSIGNMENT"))])
def submit_assignment(
    submission: SubmissionCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_user_from_session)
):
    """Submit an assignment (requires SUBMIT_ASSIGNMENT permission)"""
    # Check if assignment exists
    assignment = db.query(Assignment).filter(Assignment.id == submission.assignmentId).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Check if deadline has passed
    if assignment.deadline < datetime.now():
        # Allow submission but mark as late
        submission_status = "late"
    else:
        submission_status = "submitted"
    
    # Check if student has already submitted
    existing_submission = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.assignmentId == submission.assignmentId,
        AssignmentSubmission.studentId == user["id"]
    ).first()
    
    if existing_submission:
        # Update existing submission
        existing_submission.submissionContent = submission.submissionContent
        existing_submission.submissionType = submission.submissionType
        existing_submission.submittedAt = datetime.utcnow()
        existing_submission.status = submission_status
        db.commit()
        db.refresh(existing_submission)
        return existing_submission
    else:
        # Create new submission
        db_submission = AssignmentSubmission(
            assignmentId=submission.assignmentId,
            studentId=user["id"],
            submissionContent=submission.submissionContent,
            submissionType=submission.submissionType,
            submittedAt=datetime.utcnow(),
            status=submission_status
        )
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)
        return db_submission

@router.get("/submissions/{assignment_id}", response_model=List[SubmissionResponse], dependencies=[Depends(permission_required("MANAGE_ASSIGNMENTS"))])
def get_submissions(
    assignment_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_user_from_session)
):
    """Get all submissions for an assignment (requires MANAGE_ASSIGNMENTS permission)"""
    # Check if assignment exists and belongs to the faculty
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if assignment.facultyId != user["id"]:
        raise HTTPException(
            status_code=403, 
            detail="You can only view submissions for assignments that you created"
        )
    
    # Get all submissions for the assignment
    submissions = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.assignmentId == assignment_id
    ).all()
    
    return submissions

@router.get("/my-submissions", response_model=List[SubmissionResponse])
def get_my_submissions(
    db: Session = Depends(get_db),
    user: dict = Depends(get_user_from_session)
):
    """Get all submissions for the current user"""
    submissions = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.studentId == user["id"]
    ).all()
    
    return submissions

class GradeSubmissionRequest(BaseModel):
    grade: float = Field(..., gt=0, le=100)
    feedback: Optional[str] = None

@router.post("/grade/{submission_id}", response_model=SubmissionResponse, dependencies=[Depends(permission_required("MANAGE_ASSIGNMENTS"))])
def grade_submission(
    submission_id: int,
    grade_data: GradeSubmissionRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_user_from_session)
):
    """Grade a submission (requires MANAGE_ASSIGNMENTS permission)"""
    # Find the submission
    submission = db.query(AssignmentSubmission).filter(AssignmentSubmission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Check if the assignment belongs to the faculty
    assignment = db.query(Assignment).filter(Assignment.id == submission.assignmentId).first()
    if not assignment or assignment.facultyId != user["id"]:
        raise HTTPException(
            status_code=403, 
            detail="You can only grade submissions for assignments that you created"
        )
    
    # Update submission with grade
    submission.grade = grade_data.grade
    submission.feedback = grade_data.feedback
    submission.status = "graded"
    submission.gradedAt = datetime.utcnow()
    
    db.commit()
    db.refresh(submission)
    return submission
