from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models_quicklinks import Base, QuickLink
from config import settings

# Create database connection
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@localhost:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_quicklinks():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if quick_links table exists and has data
        existing_links = db.query(QuickLink).count()
        
        if existing_links == 0:
            print("Adding sample quick links...")
            # Add sample quick links
            quick_links = [
                QuickLink(
                    title="Academic Programs",
                    description="Explore our undergraduate and graduate programs",
                    href="/programs",
                    icon="GraduationCap",
                    category="Academic",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                QuickLink(
                    title="Faculty Directory",
                    description="Meet our distinguished faculty members",
                    href="/faculty",
                    icon="Users",
                    category="People",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                QuickLink(
                    title="Course Catalog",
                    description="Browse available courses and descriptions",
                    href="/courses",
                    icon="BookOpen",
                    category="Academic",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                QuickLink(
                    title="Admissions",
                    description="Apply to join our department",
                    href="/admissions",
                    icon="FileText",
                    category="Admissions",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                QuickLink(
                    title="Class Schedule",
                    description="View current semester schedules",
                    href="/schedule",
                    icon="Calendar",
                    category="Academic",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                QuickLink(
                    title="Research Projects",
                    description="Discover ongoing research initiatives",
                    href="/projects",
                    icon="Award",
                    category="Research",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                QuickLink(
                    title="Contact Us",
                    description="Get in touch with our department",
                    href="/contact",
                    icon="Phone",
                    category="Contact",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                QuickLink(
                    title="Student Portal",
                    description="Access grades, assignments, and more",
                    href="/login",
                    icon="ExternalLink",
                    category="Student",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
            ]
            
            db.add_all(quick_links)
            db.commit()
            print(f"Added {len(quick_links)} sample quick links")
        else:
            print(f"Found {existing_links} existing quick links, skipping sample data creation")
            
    except Exception as e:
        print(f"Error setting up quick links: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_quicklinks()
