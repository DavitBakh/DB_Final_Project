"""add gin trigram index on metadata

Revision ID: f61630234946
Revises: 8b4a29d8f364
Create Date: 2025-12-31 20:21:27.567817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f61630234946'
down_revision: Union[str, Sequence[str], None] = '8b4a29d8f364'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute("""
        CREATE INDEX ix_automobiles_metadata_trgm
        ON automobiles
        USING gin ((meta_data::text) gin_trgm_ops)
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS ix_automobiles_meta_data_trgm")
