import traceback
from app.database import SessionLocal
from app.models.student import Student
from app.models.user import User
from app.services.scoring_service import compute_score

def main():
    db = SessionLocal()
    try:
        # Find demo user
        user = db.query(User).filter(User.email == "demo@example.com").first()
        if not user:
            print("Demo user not found")
            return
        # Find associated student profile
        profile = db.query(Student).filter(Student.user_id == user.id).first()
        if not profile:
            print("Demo profile not found")
            return
        print("Found demo profile, computing score...")
        try:
            result = compute_score(db, profile)
            print("Score result:", result)
        except Exception as e:
            print("Exception during compute_score:")
            traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
