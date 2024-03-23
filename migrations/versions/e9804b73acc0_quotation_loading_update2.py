"""quotation_loading_update2

Revision ID: e9804b73acc0
Revises: c804fdf65b84
Create Date: 2024-03-23 17:13:26.198180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e9804b73acc0'
down_revision: Union[str, None] = 'c804fdf65b84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_foreign_key('fk_quotation_product_product_id', 'quotation_product', 'products', ['product_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_quotation_product_product_id', 'quotation_product', type_='foreignkey')