"""add hash_token and token_created columns to users table

Revision ID: cd0f48454f4a
Revises: cbd794d4878e
Create Date: 2025-01-07 18:52:55.104418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd0f48454f4a'
down_revision: Union[str, None] = 'cbd794d4878e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
