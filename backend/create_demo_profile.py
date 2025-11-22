import os
from app.database import SessionLocal
from app.models.user import User
from app.models.student import Student
from app.utils.security import get_password_hash

def ensure_demo_user_and_profile():
    db = SessionLocal()
    try:
        # Ensure demo user exists
        user = db.query(User).filter(User.email == "demo@example.com").first()
        if not user:
            print("Creating demo user...")
            user = User(
                email="demo@example.com",
                name="Demo User",
                hashed_password=get_password_hash("password123")
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("Demo user created.")
        else:
            print("Demo user already exists.")
        # Ensure profile exists
        profile = db.query(Student).filter(Student.user_id == user.id).first()
        if not profile:
            print("Creating demo profile...")
            profile = Student(
                user_id=user.id,
                education_level="Bachelor",
                skills="Python, React, SQL, Git",
                interests="Web Development, AI",
                bio="Worked on several web projects and contributed to open source.",
                experience_years=2.5,
                target_salary=70000,
                name="Demo User",
                contact_email="demo@example.com",
                career_direction="job"
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
            print("Demo profile created.")
        else:
            print("Demo profile already exists.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    ensure_demo_user_and_profile()
