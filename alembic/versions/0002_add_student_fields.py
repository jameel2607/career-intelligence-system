"""Add experience_years and target_salary to students table

Revision ID: 0002
Revises: 0001
Create Date: 2024-11-13 11:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add new columns to students table
    op.add_column('students', sa.Column('experience_years', sa.Float(), nullable=True, default=0.0))
    op.add_column('students', sa.Column('target_salary', sa.Float(), nullable=True))
    op.add_column('students', sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=True))
    
    # Update existing records to have created_at = updated_at if they exist
    op.execute("UPDATE students SET created_at = updated_at WHERE created_at IS NULL")

def downgrade() -> None:
    # Remove added columns
    op.drop_column('students', 'target_salary')
    op.drop_column('students', 'experience_years')
    op.drop_column('students', 'created_at')
