#!/usr/bin/env python3
"""
Script to seed fee data in the database.
"""
from sqlalchemy.orm import Session
from database import get_db
from models import User, Role, FeeCategory, Fee, Transaction, FeeStatus, TransactionStatus, PaymentMethod
from datetime import datetime, timedelta
import random

def seed_fees():
    """Seed fee data in the database."""
    db = next(get_db())
    
    # Get student users by querying the role name
    student_role = db.query(Role).filter(Role.name == "STUDENT").first()
    if not student_role:
        print("Student role not found. Please seed roles first.")
        return
        
    student_users = db.query(User).filter(User.role_id == student_role.id).all()
    if not student_users:
        print("No student users found. Please seed users first.")
        return
    
    # Create fee categories
    categories = [
        {"name": "Tuition Fee", "description": "Regular tuition fee for semester"},
        {"name": "Registration Fee", "description": "Course registration fee"},
        {"name": "Library Fee", "description": "Annual library and resource access fee"},
        {"name": "Lab Fee", "description": "Laboratory usage and maintenance fee"},
        {"name": "Student Activity Fee", "description": "Fee for student clubs and activities"},
        {"name": "Examination Fee", "description": "Fee for examinations and assessments"},
        {"name": "Development Fee", "description": "University development and infrastructure fee"}
    ]
    
    db_categories = []
    for category in categories:
        db_category = FeeCategory(**category)
        db.add(db_category)
        db_categories.append(db_category)
    
    db.commit()
    
    # Refresh categories to get their IDs
    for category in db_categories:
        db.refresh(category)
    
    print(f"Created {len(db_categories)} fee categories")
    
    # Create fees for each student
    now = datetime.utcnow()
    semesters = ["2025 Summer", "2025 Spring", "2024 Fall"]
    batches = ["21", "22", "23", "24"]
    
    all_fees = []
    
    for student in student_users:
        # Assign a random batch to the student
        student_batch = random.choice(batches)
        
        # Create fees for the current semester (2025 Summer)
        current_semester = semesters[0]
        
        # Tuition Fee
        tuition_fee = Fee(
            name="Tuition Fee",
            amount=25000,
            description=f"Regular tuition fee for {current_semester} semester",
            deadline=now + timedelta(days=15),
            status=FeeStatus.PENDING,
            semester=current_semester,
            batch=student_batch,
            category_id=db_categories[0].id,
            student_id=student.id
        )
        db.add(tuition_fee)
        all_fees.append(tuition_fee)
        
        # Registration Fee (already paid)
        reg_fee = Fee(
            name="Registration Fee",
            amount=5000,
            description=f"Course registration fee for {current_semester}",
            deadline=now - timedelta(days=5),
            status=FeeStatus.PAID,
            semester=current_semester,
            batch=student_batch,
            category_id=db_categories[1].id,
            student_id=student.id,
            paid_date=now - timedelta(days=10),
            paid_amount=5000
        )
        db.add(reg_fee)
        all_fees.append(reg_fee)
        
        # Library Fee
        library_fee = Fee(
            name="Library Fee",
            amount=2000,
            description="Annual library and resource access fee",
            deadline=now + timedelta(days=20),
            status=FeeStatus.PENDING,
            semester=current_semester,
            batch=student_batch,
            category_id=db_categories[2].id,
            student_id=student.id
        )
        db.add(library_fee)
        all_fees.append(library_fee)
        
        # Lab Fee
        lab_fee = Fee(
            name="Lab Fee",
            amount=3500,
            description="Laboratory usage and maintenance fee",
            deadline=now + timedelta(days=20),
            status=FeeStatus.PENDING,
            semester=current_semester,
            batch=student_batch,
            category_id=db_categories[3].id,
            student_id=student.id
        )
        db.add(lab_fee)
        all_fees.append(lab_fee)
        
        # Student Activity Fee
        activity_fee = Fee(
            name="Student Activity Fee",
            amount=1500,
            description="Fee for student clubs and activities",
            deadline=now + timedelta(days=30),
            status=FeeStatus.PENDING,
            semester=current_semester,
            batch=student_batch,
            category_id=db_categories[4].id,
            student_id=student.id
        )
        db.add(activity_fee)
        all_fees.append(activity_fee)
        
        # Previous Semester Due (overdue)
        if random.random() < 0.3:  # 30% chance of having an overdue fee
            prev_fee = Fee(
                name="Previous Semester Due",
                amount=2500,
                description=f"Outstanding balance from {semesters[1]}",
                deadline=now - timedelta(days=10),
                status=FeeStatus.OVERDUE,
                semester=semesters[1],
                batch=student_batch,
                category_id=random.choice(db_categories).id,
                student_id=student.id
            )
            db.add(prev_fee)
            all_fees.append(prev_fee)
    
    db.commit()
    
    # Refresh fees to get their IDs
    for fee in all_fees:
        db.refresh(fee)
    
    print(f"Created {len(all_fees)} fees for {len(student_users)} students")
    
    # Create transactions for paid fees
    transactions = []
    
    for fee in all_fees:
        if fee.status == FeeStatus.PAID:
            transaction = Transaction(
                date=fee.paid_date,
                amount=fee.paid_amount,
                description=f"Payment for {fee.name}",
                payment_method=random.choice(list(PaymentMethod)),
                status=TransactionStatus.COMPLETED,
                receipt_url=f"/receipts/txn-{random.randint(10000000, 99999999)}.pdf",
                transaction_id=f"TXN-{random.randint(10000000, 99999999)}",
                fee_id=fee.id,
                student_id=fee.student_id
            )
            db.add(transaction)
            transactions.append(transaction)
    
    db.commit()
    
    print(f"Created {len(transactions)} transactions")
    print("Successfully seeded fees and transactions!")

if __name__ == "__main__":
    seed_fees()
