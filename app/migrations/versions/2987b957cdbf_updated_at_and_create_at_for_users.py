"""updated_at and create_at for users

Revision ID: 2987b957cdbf
Revises: 1c72565ce4ab
Create Date: 2023-09-26 06:33:46.346083

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2987b957cdbf"
down_revision: Union[str, None] = "1c72565ce4ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("users", sa.Column("updated_at", sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
    # ### end Alembic commands ###
