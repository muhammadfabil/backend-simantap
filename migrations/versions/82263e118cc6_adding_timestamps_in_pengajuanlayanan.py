"""Adding timestamps in PengajuanLayanan

Revision ID: 82263e118cc6
Revises: 1f48e8d840ad
Create Date: 2025-04-30 17:05:10.572790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82263e118cc6'
down_revision: Union[str, None] = '1f48e8d840ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'pengajuan_layanan',
        sa.Column('timestamp_diproses', sa.DateTime(), nullable=True),
    )
    op.add_column(
        'pengajuan_layanan',
        sa.Column('timestamp_selesai', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('pengajuan_layanan', 'timestamp_diproses')
    op.drop_column('pengajuan_layanan', 'timestamp_selesai')
