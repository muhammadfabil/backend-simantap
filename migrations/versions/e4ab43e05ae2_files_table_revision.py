"""Files Table Revision

Revision ID: e4ab43e05ae2
Revises: 5f0b3171f765
Create Date: 2025-04-27 00:42:49.217954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4ab43e05ae2'
down_revision: Union[str, None] = '5f0b3171f765'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('files', sa.Column('update_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    pass
