from app.database import SessionLocal
from app.models.user import User
from app.utils.security import get_password_hash

def ensure_demo_user():
    db = SessionLocal()
    try:
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
            print("Demo user created.")
        else:
            print("Demo user already exists.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    ensure_demo_user()
