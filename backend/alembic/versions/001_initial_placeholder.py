"""initial placeholder revision

Revision ID: 001
Revises:
Create Date: 2026-11-26
"""
from typing import Sequence, Union

# Placeholder – generate real revision with:
# alembic revision --autogenerate -m "initial"
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Real migrations should be generated against your DB.
    pass


def downgrade() -> None:
    pass
