"""Drop antrian_bimbingan and files tables

Revision ID: ddf134a809f2
Revises: e4ab43e05ae2
Create Date: 2025-04-27 03:01:00.044370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddf134a809f2'
down_revision: Union[str, None] = 'e4ab43e05ae2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_table('files')
    op.drop_table('antrian_bimbingan')

def downgrade():
    pass
