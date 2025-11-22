"""add_scoring_metrics

Revision ID: 0004
Revises: 0003
Create Date: 2025-11-22 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to career_scores table
    op.add_column('career_scores', sa.Column('market_factor', sa.Float(), nullable=True))
    op.add_column('career_scores', sa.Column('meta_factor', sa.Float(), nullable=True))
    op.add_column('career_scores', sa.Column('role_demand', sa.Float(), nullable=True))
    op.add_column('career_scores', sa.Column('role_difficulty', sa.Float(), nullable=True))
    op.add_column('career_scores', sa.Column('salary_fit', sa.Float(), nullable=True))
    op.add_column('career_scores', sa.Column('evidence_confidence', sa.Float(), nullable=True))
    op.add_column('career_scores', sa.Column('data_completeness', sa.Float(), nullable=True))


def downgrade():
    # Remove columns
    op.drop_column('career_scores', 'data_completeness')
    op.drop_column('career_scores', 'evidence_confidence')
    op.drop_column('career_scores', 'salary_fit')
    op.drop_column('career_scores', 'role_difficulty')
    op.drop_column('career_scores', 'role_demand')
    op.drop_column('career_scores', 'meta_factor')
    op.drop_column('career_scores', 'market_factor')
