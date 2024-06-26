"""client-quotation problem solving

Revision ID: 3f455f8f535c
Revises: e41d40cba835
Create Date: 2024-06-25 19:57:38.645092

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '3f455f8f535c'
down_revision: Union[str, None] = 'e41d40cba835'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('quotations', 'client_id', existing_type=Integer, nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
