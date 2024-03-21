"""quotation_product

Revision ID: e886d6e60db5
Revises: e756f75af337
Create Date: 2024-03-21 12:03:31.273830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e886d6e60db5'
down_revision: Union[str, None] = 'e756f75af337'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new column
    op.add_column('quotation_product', sa.Column('quantity', sa.Integer(), nullable=True))

    # Copy data from 'number' to 'quantity'
    connection = op.get_bind()
    connection.execute("UPDATE quotation_product SET quantity = number")

    # Drop old column
    op.drop_column('quotation_product', 'number')

def downgrade() -> None:
    # Add new column
    op.add_column('quotation_product', sa.Column('number', sa.Integer(), nullable=True))

    # Copy data from 'quantity' to 'number'
    connection = op.get_bind()
    connection.execute("UPDATE quotation_product SET number = quantity")

    # Drop old column
    op.drop_column('quotation_product', 'quantity')