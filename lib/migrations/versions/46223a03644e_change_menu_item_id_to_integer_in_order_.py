"""Change menu_item_id to Integer in order_details

Revision ID: 46223a03644e
Revises: 3d350dab02ba
Create Date: 2024-05-27 16:49:17.749037

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46223a03644e'
down_revision: Union[str, None] = '3d350dab02ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Change menu_item_id column from String to Integer
    with op.batch_alter_table('order_details') as batch_op:
        batch_op.alter_column('menu_item_id',
                              existing_type=sa.String(),
                              type_=sa.Integer(),
                              existing_nullable=False)


def downgrade() -> None:
    # Revert menu_item_id column from Integer to String
    with op.batch_alter_table('order_details') as batch_op:
        batch_op.alter_column('menu_item_id',
                              existing_type=sa.Integer(),
                              type_=sa.String(),
                              existing_nullable=False)
