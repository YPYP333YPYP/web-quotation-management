"""custom_product init

Revision ID: 5f1cfc3c5823
Revises: 425d363826ae
Create Date: 2024-08-09 23:32:48.673063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '5f1cfc3c5823'
down_revision: Union[str, None] = '425d363826ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'custom_products',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, index=True),
        sa.Column('name', sa.String(length=255), nullable=False, index=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=255), nullable=False, index=True),
        sa.Column('unit', sa.String(length=255), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

def downgrade() -> None:
    op.drop_table('custom_products')
