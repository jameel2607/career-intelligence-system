import sqlite3
import os

# Database path
DB_PATH = "d:/Minds CIE/backend/career_guidance.db"

def migrate():
    print(f"Migrating database at {DB_PATH}...")
    
    if not os.path.exists(DB_PATH):
        print("Database not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # List of new columns to add
    new_columns = [
        ("market_factor", "FLOAT"),
        ("meta_factor", "FLOAT"),
        ("role_demand", "FLOAT"),
        ("role_difficulty", "FLOAT"),
        ("salary_fit", "FLOAT"),
        ("evidence_confidence", "FLOAT"),
        ("data_completeness", "FLOAT")
    ]
    
    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE career_scores ADD COLUMN {col_name} {col_type}")
            print(f"Added column {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Column {col_name} already exists")
            else:
                print(f"Error adding {col_name}: {e}")
    
    conn.commit()
    conn.close()
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()
