"""add hash_token and token_created columns to users table

Revision ID: 25dc1a6ad142
Revises: cd0f48454f4a
Create Date: 2025-01-08 16:37:53.764214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25dc1a6ad142'
down_revision: Union[str, None] = 'cd0f48454f4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
