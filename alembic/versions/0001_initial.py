from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_users_email', 'users', ['email'])

    op.create_table(
        'students',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False, unique=True),
        sa.Column('education_level', sa.String(100)),
        sa.Column('skills', sa.Text),
        sa.Column('interests', sa.Text),
        sa.Column('bio', sa.Text),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'documents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('path', sa.String(500), nullable=False),
        sa.Column('mime_type', sa.String(100)),
        sa.Column('ocr_text', sa.Text),
        sa.Column('ocr_confidence', sa.Float),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_documents_user_id', 'documents', ['user_id'])

    op.create_table(
        'reports',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('path', sa.String(500), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_reports_user_id', 'reports', ['user_id'])

    op.create_table(
        'career_scores',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('total_score', sa.Integer, nullable=False),
        sa.Column('degree_score', sa.Float),
        sa.Column('experience_score', sa.Float),
        sa.Column('skill_coverage_score', sa.Float),
        sa.Column('certificate_quality_score', sa.Float),
        sa.Column('practical_evidence_score', sa.Float),
        sa.Column('soft_skills_score', sa.Float),
        sa.Column('confidence', sa.Float),
        sa.Column('calculated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_career_scores_user_id', 'career_scores', ['user_id'])

def downgrade():
    op.drop_table('career_scores')
    op.drop_table('reports')
    op.drop_table('documents')
    op.drop_table('students')
    op.drop_table('users')
