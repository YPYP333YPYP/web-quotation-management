"""notice init

Revision ID: 61275459cf4d
Revises: 5f1cfc3c5823
Create Date: 2024-08-16 02:09:15.215015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '61275459cf4d'
down_revision: Union[str, None] = '5f1cfc3c5823'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'notices',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, index=True),
        sa.Column('title', sa.String(length=255), nullable=False, index=True),
        sa.Column('content', sa.TEXT, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

def downgrade() -> None:
    op.drop_table('notice')