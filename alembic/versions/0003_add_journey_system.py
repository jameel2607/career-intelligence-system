"""Add journey system and enhanced profile fields

Revision ID: 0003
Revises: 0002
Create Date: 2025-11-22

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade():
    # Add journey tracking fields to students table
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('journey_stage', sa.Integer(), nullable=True, server_default='1'))
        batch_op.add_column(sa.Column('completion_percentage', sa.Float(), nullable=True, server_default='0.0'))
        
        # Add enhanced profile fields
        batch_op.add_column(sa.Column('career_direction', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('name', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('contact_email', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('contact_phone', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('language_fluency', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('medium_of_instruction_10', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('medium_of_instruction_12', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('gpa_percentile', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('linkedin_url', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('github_url', sa.String(length=500), nullable=True))
    
    # Add verification fields to documents table
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verification_status', sa.String(length=20), nullable=True, server_default='needs_action'))
        batch_op.add_column(sa.Column('provider', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('extracted_skills', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('manual_edits', sa.JSON(), nullable=True))
    
    # Create courses table
    op.create_table('courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('duration_hours', sa.Integer(), nullable=True),
        sa.Column('score_impact', sa.Float(), nullable=True),
        sa.Column('target_component', sa.String(length=50), nullable=True),
        sa.Column('difficulty', sa.String(length=20), nullable=True),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('provider', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Integer(), nullable=True, server_default='1'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)
    
    # Create user_courses table
    op.create_table('user_courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='not_started'),
        sa.Column('progress_percentage', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_courses_id'), 'user_courses', ['id'], unique=False)
    op.create_index(op.f('ix_user_courses_user_id'), 'user_courses', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_courses_course_id'), 'user_courses', ['course_id'], unique=False)
    
    # Create user_progress table
    op.create_table('user_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('actions_completed', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('courses_completed', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('documents_uploaded', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_progress_id'), 'user_progress', ['id'], unique=False)
    op.create_index(op.f('ix_user_progress_user_id'), 'user_progress', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_progress_date'), 'user_progress', ['date'], unique=False)


def downgrade():
    # Drop new tables
    op.drop_index(op.f('ix_user_progress_date'), table_name='user_progress')
    op.drop_index(op.f('ix_user_progress_user_id'), table_name='user_progress')
    op.drop_index(op.f('ix_user_progress_id'), table_name='user_progress')
    op.drop_table('user_progress')
    
    op.drop_index(op.f('ix_user_courses_course_id'), table_name='user_courses')
    op.drop_index(op.f('ix_user_courses_user_id'), table_name='user_courses')
    op.drop_index(op.f('ix_user_courses_id'), table_name='user_courses')
    op.drop_table('user_courses')
    
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_table('courses')
    
    # Remove columns from documents table
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.drop_column('manual_edits')
        batch_op.drop_column('extracted_skills')
        batch_op.drop_column('provider')
        batch_op.drop_column('verification_status')
    
    # Remove columns from students table
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.drop_column('github_url')
        batch_op.drop_column('linkedin_url')
        batch_op.drop_column('gpa_percentile')
        batch_op.drop_column('medium_of_instruction_12')
        batch_op.drop_column('medium_of_instruction_10')
        batch_op.drop_column('language_fluency')
        batch_op.drop_column('contact_phone')
        batch_op.drop_column('contact_email')
        batch_op.drop_column('name')
        batch_op.drop_column('career_direction')
        batch_op.drop_column('completion_percentage')
        batch_op.drop_column('journey_stage')
