"""init migration

Revision ID: 27782269e586
Revises:
Create Date: 2023-08-24 20:07:33.020595

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '27782269e586'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String(100), unique=True, index=True),
        sa.Column('password', sa.String(100)),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('user_type', sa.Enum('CLIENT', 'ADMIN', 'MODERATOR', name='user_type_enum'), default='CLIENT'),
    )


def downgrade() -> None:
    op.drop_table('user')
