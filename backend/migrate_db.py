"""
Direct SQL migration script for journey system and enhanced profile fields
Run this if Alembic migration fails
"""
import sqlite3
import os

# Get database path
db_path = os.path.join(os.path.dirname(__file__), '..', 'career.db')

print(f"Connecting to database: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("\n=== Starting Migration ===\n")
    
    # Add journey tracking fields to students table
    print("1. Adding journey tracking fields to students table...")
    try:
        cursor.execute("ALTER TABLE students ADD COLUMN journey_stage INTEGER DEFAULT 1")
        print("   ✓ Added journey_stage")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("   ⚠ journey_stage already exists")
        else:
            raise
    
    try:
        cursor.execute("ALTER TABLE students ADD COLUMN completion_percentage REAL DEFAULT 0.0")
        print("   ✓ Added completion_percentage")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("   ⚠ completion_percentage already exists")
        else:
            raise
    
    # Add enhanced profile fields to students table
    print("\n2. Adding enhanced profile fields to students table...")
    enhanced_fields = [
        ("career_direction", "VARCHAR(50)"),
        ("name", "VARCHAR(200)"),
        ("contact_email", "VARCHAR(200)"),
        ("contact_phone", "VARCHAR(50)"),
        ("language_fluency", "TEXT"),  # JSON stored as TEXT in SQLite
        ("medium_of_instruction_10", "VARCHAR(50)"),
        ("medium_of_instruction_12", "VARCHAR(50)"),
        ("gpa_percentile", "REAL"),
        ("linkedin_url", "VARCHAR(500)"),
        ("github_url", "VARCHAR(500)")
    ]
    
    for field_name, field_type in enhanced_fields:
        try:
            cursor.execute(f"ALTER TABLE students ADD COLUMN {field_name} {field_type}")
            print(f"   ✓ Added {field_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"   ⚠ {field_name} already exists")
            else:
                raise
    
    # Add verification fields to documents table
    print("\n3. Adding verification fields to documents table...")
    verification_fields = [
        ("verification_status", "VARCHAR(20) DEFAULT 'needs_action'"),
        ("provider", "VARCHAR(100)"),
        ("extracted_skills", "TEXT"),  # JSON stored as TEXT in SQLite
        ("manual_edits", "TEXT")  # JSON stored as TEXT in SQLite
    ]
    
    for field_name, field_type in verification_fields:
        try:
            cursor.execute(f"ALTER TABLE documents ADD COLUMN {field_name} {field_type}")
            print(f"   ✓ Added {field_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"   ⚠ {field_name} already exists")
            else:
                raise
    
    # Create courses table
    print("\n4. Creating courses table...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                category VARCHAR(50) NOT NULL,
                description TEXT,
                duration_hours INTEGER,
                score_impact REAL,
                target_component VARCHAR(50),
                difficulty VARCHAR(20),
                url VARCHAR(500),
                provider VARCHAR(100),
                is_active INTEGER DEFAULT 1
            )
        """)
        print("   ✓ Created courses table")
    except sqlite3.OperationalError as e:
        print(f"   ⚠ courses table: {e}")
    
    # Create user_courses table
    print("\n5. Creating user_courses table...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                status VARCHAR(20) DEFAULT 'not_started',
                progress_percentage REAL DEFAULT 0.0,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (course_id) REFERENCES courses(id)
            )
        """)
        print("   ✓ Created user_courses table")
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_user_courses_user_id ON user_courses(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_user_courses_course_id ON user_courses(course_id)")
        print("   ✓ Created indexes for user_courses")
    except sqlite3.OperationalError as e:
        print(f"   ⚠ user_courses table: {e}")
    
    # Create user_progress table
    print("\n6. Creating user_progress table...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                score INTEGER,
                actions_completed INTEGER DEFAULT 0,
                courses_completed INTEGER DEFAULT 0,
                documents_uploaded INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        print("   ✓ Created user_progress table")
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_user_progress_user_id ON user_progress(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_user_progress_date ON user_progress(date)")
        print("   ✓ Created indexes for user_progress")
    except sqlite3.OperationalError as e:
        print(f"   ⚠ user_progress table: {e}")
    
    # Commit all changes
    conn.commit()
    print("\n=== Migration Completed Successfully! ===\n")
    
    # Verify tables exist
    print("Verifying tables...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    print(f"Total tables: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
    
except Exception as e:
    print(f"\n❌ Error during migration: {e}")
    conn.rollback()
    raise
finally:
    conn.close()
    print("\nDatabase connection closed.")
