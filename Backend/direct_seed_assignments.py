from sqlalchemy.orm import Session
from database import get_db
from models import User, Role, Assignment, AssignmentSubmission
from datetime import datetime, timedelta
import random

def seed_assignments():
    db = next(get_db())
    
    # Get faculty users by querying the role name instead of assuming role_id
    faculty_role = db.query(Role).filter(Role.name == "faculty").first()
    if not faculty_role:
        print("Faculty role not found. Please seed roles first.")
        return
        
    faculty_users = db.query(User).filter(User.role_id == faculty_role.id).all()
    if not faculty_users:
        print("No faculty users found. Please seed users first.")
        return
    
    # Sample course data
    courses = [
        {"code": "CSE-301", "title": "Design and Analysis of Algorithms"},
        {"code": "CSE-303", "title": "Database Systems"},
        {"code": "CSE-307", "title": "Operating Systems"},
        {"code": "CSE-309", "title": "Web Technologies"},
        {"code": "CSE-401", "title": "Artificial Intelligence"},
        {"code": "CSE-403", "title": "Computer Graphics"},
        {"code": "CSE-405", "title": "Software Engineering"},
        {"code": "CSE-407", "title": "Computer Networks"}
    ]
    
    # Sample assignment descriptions
    descriptions = [
        "Analyze the time and space complexity of the provided algorithms and submit a detailed report.",
        "Design a comprehensive database schema for the university management system described in the requirements.",
        "Implement and train a neural network model for the given classification problem.",
        "Implement a simulation of CPU scheduling algorithms and compare their performance.",
        "Document and analyze the results of the network protocols lab experiments.",
        "Prepare a detailed project proposal including requirements analysis, design specifications, and implementation plan.",
        "Develop a responsive web application according to the provided specifications.",
        "Implement the specified 3D rendering algorithms and create visual demonstrations."
    ]
    
    # Sample attachment names
    attachment_templates = [
        {"name": "{code}_assignment.pdf", "url": "/assignments/{code}/assignment.pdf"},
        {"name": "requirements.pdf", "url": "/assignments/{code}/requirements.pdf"},
        {"name": "dataset.csv", "url": "/assignments/{code}/dataset.csv"},
        {"name": "template.docx", "url": "/assignments/{code}/template.docx"}
    ]
    
    # Create assignments
    assignments = []
    now = datetime.utcnow()
    
    for i in range(15):
        # Select a random course and faculty
        course = random.choice(courses)
        faculty = random.choice(faculty_users)
        
        # Determine status and deadline
        status_choice = random.choice(["active", "past", "draft"])
        
        if status_choice == "active":
            deadline = now + timedelta(days=random.randint(1, 14))
        elif status_choice == "past":
            deadline = now - timedelta(days=random.randint(1, 30))
        else:  # draft
            deadline = now + timedelta(days=random.randint(7, 21))
        
        # Generate attachments
        num_attachments = random.randint(0, 3)
        attachments = []
        if num_attachments > 0:
            selected_attachments = random.sample(attachment_templates, num_attachments)
            for attachment in selected_attachments:
                attachments.append({
                    "name": attachment["name"].format(code=course["code"].lower()),
                    "url": attachment["url"].format(code=course["code"].lower())
                })
        
        # Create assignment
        assignment = Assignment(
            title=f"{course['title']} Assignment {random.randint(1, 5)}",
            courseCode=course["code"],
            courseTitle=course["title"],
            semester=random.randint(1, 8),
            batch=f"{random.randint(20, 25)}",
            deadline=deadline,
            description=random.choice(descriptions),
            attachments=attachments if attachments else None,
            submissionType=random.choice(["file", "link", "text"]),
            status=status_choice,
            facultyId=faculty.id,
            facultyName=faculty.name,
            createdAt=now - timedelta(days=random.randint(1, 30)),
            updatedAt=now - timedelta(days=random.randint(0, 5))
        )
        
        db.add(assignment)
        assignments.append(assignment)
    
    db.commit()
    
    # Refresh assignments to get their IDs
    for assignment in assignments:
        db.refresh(assignment)
    
    # Get student users for submissions by querying the role name
    student_role = db.query(Role).filter(Role.name == "student").first()
    if not student_role:
        print("Student role not found. Please seed roles first.")
        return
        
    student_users = db.query(User).filter(User.role_id == student_role.id).all()
    if not student_users:
        print("No student users found. Skipping submission seeding.")
        return
    
    # Create submissions for some assignments
    for assignment in assignments:
        # Skip draft assignments and some active ones
        if assignment.status == "draft" or (assignment.status == "active" and random.random() < 0.3):
            continue
        
        # Determine how many students submitted
        num_submissions = random.randint(1, min(5, len(student_users)))
        submitting_students = random.sample(student_users, num_submissions)
        
        for student in submitting_students:
            # Determine submission time
            if assignment.status == "past" or (assignment.status == "active" and random.random() < 0.8):
                # Submission before deadline
                submission_time = min(
                    assignment.deadline - timedelta(hours=random.randint(1, 48)),
                    datetime.utcnow()
                )
                submission_status = "submitted"
            else:
                # Late submission
                submission_time = min(
                    assignment.deadline + timedelta(hours=random.randint(1, 24)),
                    datetime.utcnow()
                )
                submission_status = "late"
            
            # Create submission content based on type
            if assignment.submissionType == "file":
                content = f"/submissions/{assignment.id}/{student.id}/submission.pdf"
            elif assignment.submissionType == "link":
                content = f"https://github.com/student{student.id}/assignment{assignment.id}"
            else:  # text
                content = "This is my submission for the assignment. I have completed all the required tasks and included my analysis as requested."
            
            # Create submission
            submission = AssignmentSubmission(
                assignmentId=assignment.id,
                studentId=student.id,
                submissionContent=content,
                submissionType=assignment.submissionType,
                submittedAt=submission_time,
                status=submission_status
            )
            
            # Add grade for some past submissions
            if assignment.status == "past" and random.random() < 0.7:
                submission.grade = round(random.uniform(60, 100), 1)
                submission.feedback = random.choice([
                    "Good work! Your analysis is thorough and well-presented.",
                    "Well done. Consider exploring the alternative approaches we discussed in class.",
                    "Excellent submission. Your implementation is efficient and well-documented.",
                    "Satisfactory work, but your explanation could be more detailed.",
                    "Great job on the implementation, but there are some edge cases you didn't handle."
                ])
                submission.status = "graded"
                submission.gradedAt = submission_time + timedelta(days=random.randint(1, 5))
            
            db.add(submission)
    
    db.commit()
    print("Successfully seeded assignments and submissions!")

if __name__ == "__main__":
    seed_assignments()
