"""quotation_product

Revision ID: 4c4731b47610
Revises: 578bb33ae6c4
Create Date: 2024-06-27 16:07:05.394591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c4731b47610'
down_revision: Union[str, None] = '578bb33ae6c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('quotation_product',
        sa.Column('quotation_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['quotation_id'], ['quotations.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('quotation_id', 'product_id')
    )

def downgrade():
    op.drop_table('quotation_product')
