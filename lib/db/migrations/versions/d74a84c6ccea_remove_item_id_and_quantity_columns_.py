"""Remove item_id and quantity columns from orders table

Revision ID: d74a84c6ccea
Revises: 5500f4b8ddef
Create Date: 2024-05-26 23:45:49.758263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd74a84c6ccea'
down_revision: Union[str, None] = '5500f4b8ddef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("orders") as batch_op:
        batch_op.drop_column('item_id')
        batch_op.drop_column('quantity')


def downgrade() -> None:
    with op.batch_alter_table("orders") as batch_op:
        batch_op.add_column(sa.Column('item_id', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_orders_item_id', 'item_id', 'menu_items', ['id'])
