"""make name not nullable

Revision ID: 225fbb3ba271
Revises: cee0f686fe33
Create Date: 2023-11-12 17:55:54.352066

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '225fbb3ba271'
down_revision: Union[str, None] = 'cee0f686fe33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
