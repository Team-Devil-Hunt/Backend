import os
import sys
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import EquipmentCategory, Equipment, EquipmentBooking, User
from database import Base

# Load environment variables
load_dotenv()

# Database connection
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Create database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Clear existing data
def clear_existing_data():
    try:
        db.execute(text("DELETE FROM equipment_bookings"))
        db.execute(text("DELETE FROM equipment"))
        db.execute(text("DELETE FROM equipment_categories"))
        db.commit()
        print("Existing equipment data cleared.")
    except Exception as e:
        db.rollback()
        print(f"Error clearing existing data: {e}")
        sys.exit(1)

# Seed equipment categories
def seed_equipment_categories():
    categories = [
        {
            "name": "Computing Hardware",
            "icon": "Cpu",
            "description": "High-performance computing resources including GPUs, servers, and specialized processors"
        },
        {
            "name": "Sensors & IoT",
            "icon": "Wifi",
            "description": "Various sensors, actuators, and Internet of Things devices for research and projects"
        },
        {
            "name": "Storage & Memory",
            "icon": "Database",
            "description": "Storage devices and memory modules for data-intensive applications"
        },
        {
            "name": "Mobile & Embedded",
            "icon": "Smartphone",
            "description": "Mobile devices and embedded systems for testing and development"
        },
        {
            "name": "Networking",
            "icon": "Layers",
            "description": "Networking equipment for communication and distributed systems research"
        }
    ]
    
    category_ids = {}
    
    for cat in categories:
        category = EquipmentCategory(
            name=cat["name"],
            icon=cat["icon"],
            description=cat["description"]
        )
        db.add(category)
        db.flush()
        category_ids[cat["name"]] = category.id
    
    db.commit()
    print(f"Added {len(categories)} equipment categories.")
    return category_ids

# Seed equipment
def seed_equipment(category_ids):
    equipment_data = [
        {
            "name": "NVIDIA RTX 4090 GPU",
            "description": "High-end graphics processing unit for AI and deep learning applications",
            "category_name": "Computing Hardware",
            "specifications": "24GB GDDR6X, 16384 CUDA cores, 2.52 GHz boost clock",
            "quantity": 4,
            "available": 2,
            "image": "/assets/equipment/gpu.jpg",
            "location": "AI Lab (Room 302)",
            "requires_approval": True
        },
        {
            "name": "Temperature & Humidity Sensor Kit",
            "description": "Precision sensors for environmental monitoring in IoT projects",
            "category_name": "Sensors & IoT",
            "specifications": "DHT22 sensors, -40 to 80°C range, ±0.5°C accuracy",
            "quantity": 20,
            "available": 15,
            "image": "/assets/equipment/temp-sensor.jpg",
            "location": "IoT Lab (Room 201)",
            "requires_approval": False
        },
        {
            "name": "High-Performance Server",
            "description": "Multi-core server for distributed computing and virtualization",
            "category_name": "Computing Hardware",
            "specifications": "AMD EPYC 7763, 64 cores, 128 threads, 256GB RAM",
            "quantity": 2,
            "available": 1,
            "image": "/assets/equipment/server.jpg",
            "location": "Server Room (Room 405)",
            "requires_approval": True
        },
        {
            "name": "Motion Capture System",
            "description": "Advanced motion tracking system for computer vision research",
            "category_name": "Sensors & IoT",
            "specifications": "12-camera setup, 120fps, sub-millimeter accuracy",
            "quantity": 1,
            "available": 1,
            "image": "/assets/equipment/motion-capture.jpg",
            "location": "Graphics Lab (Room 304)",
            "requires_approval": True
        },
        {
            "name": "SSD Storage Array",
            "description": "High-speed storage array for data-intensive applications",
            "category_name": "Storage & Memory",
            "specifications": "10TB total, NVMe SSDs, 7000MB/s read, 5000MB/s write",
            "quantity": 3,
            "available": 3,
            "image": "/assets/equipment/ssd-array.jpg",
            "location": "Data Science Lab (Room 303)",
            "requires_approval": False
        },
        {
            "name": "Raspberry Pi Kit",
            "description": "Complete Raspberry Pi development kit with accessories",
            "category_name": "Mobile & Embedded",
            "specifications": "Raspberry Pi 4B, 8GB RAM, 64GB SD, sensors, display",
            "quantity": 15,
            "available": 8,
            "image": "/assets/equipment/raspberry-pi.jpg",
            "location": "Embedded Systems Lab (Room 202)",
            "requires_approval": False
        },
        {
            "name": "Network Testing Kit",
            "description": "Professional networking equipment for protocol testing and research",
            "category_name": "Networking",
            "specifications": "Cisco switches, routers, packet analyzers, cables",
            "quantity": 5,
            "available": 4,
            "image": "/assets/equipment/network-kit.jpg",
            "location": "Networking Lab (Room 203)",
            "requires_approval": True
        },
        {
            "name": "Drone Development Kit",
            "description": "Programmable drone with sensors and development interface",
            "category_name": "Sensors & IoT",
            "specifications": "Quadcopter, 4K camera, programmable flight controller",
            "quantity": 3,
            "available": 2,
            "image": "/assets/equipment/drone.jpg",
            "location": "Robotics Lab (Room 305)",
            "requires_approval": True
        }
    ]
    
    equipment_ids = {}
    
    for eq in equipment_data:
        equipment = Equipment(
            name=eq["name"],
            description=eq["description"],
            category_id=category_ids[eq["category_name"]],
            specifications=eq["specifications"],
            quantity=eq["quantity"],
            available=eq["available"],
            image=eq["image"],
            location=eq["location"],
            requires_approval=eq["requires_approval"]
        )
        db.add(equipment)
        db.flush()
        equipment_ids[eq["name"]] = equipment.id
    
    db.commit()
    print(f"Added {len(equipment_data)} equipment items.")
    return equipment_ids

# Seed equipment bookings
def seed_equipment_bookings(equipment_ids):
    # Get some users
    users = db.query(User).limit(5).all()
    if not users:
        print("No users found. Please seed users first.")
        return
    
    # Status options
    status_options = ["pending", "approved", "rejected", "completed"]
    
    # Generate bookings
    bookings = []
    now = datetime.now()
    
    for i in range(10):
        # Select random equipment and user
        equipment_name = random.choice(list(equipment_ids.keys()))
        equipment_id = equipment_ids[equipment_name]
        user = random.choice(users)
        
        # Generate random dates
        days_offset_start = random.randint(-5, 20)
        start_time = now + timedelta(days=days_offset_start, hours=random.randint(0, 23))
        end_time = start_time + timedelta(hours=random.randint(1, 8))
        created_at = start_time - timedelta(days=random.randint(1, 5))
        updated_at = created_at + timedelta(hours=random.randint(1, 24))
        
        # Determine status based on dates
        if start_time < now and end_time < now:
            status = "completed"
        elif start_time < now and end_time > now:
            status = "approved"
        else:
            status = random.choice(status_options)
        
        # Create booking
        booking = EquipmentBooking(
            equipment_id=equipment_id,
            user_id=user.id,
            user_name=user.name,
            user_role="student" if user.role_id == 2 else "faculty",
            start_time=start_time,
            end_time=end_time,
            purpose=f"Research project on {random.choice(['AI', 'ML', 'IoT', 'Computer Vision', 'Network Security', 'Data Science'])}",
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            rejection_reason=None if status != "rejected" else "Conflicting schedule with higher priority research"
        )
        bookings.append(booking)
    
    db.add_all(bookings)
    db.commit()
    print(f"Added {len(bookings)} equipment bookings.")

# Main function
def main():
    try:
        clear_existing_data()
        category_ids = seed_equipment_categories()
        equipment_ids = seed_equipment(category_ids)
        seed_equipment_bookings(equipment_ids)
        print("Equipment data seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
