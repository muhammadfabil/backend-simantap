"""Revision table Waktu_Bimbingan

Revision ID: 42b95972e594
Revises: 27c80be48307
Create Date: 2025-04-27 05:38:36.827917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42b95972e594'
down_revision: Union[str, None] = '27c80be48307'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'waktu_bimbingan',
        sa.Column('bimbingan_id', sa.String(), primary_key=True, index=True),
        sa.Column('dosen_alias', sa.String(), sa.ForeignKey('dosen.alias', ondelete="CASCADE"), nullable=False),
        sa.Column('jumlah_antrian', sa.Integer, nullable=False, server_default=sa.text('5')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('tanggal', sa.Date, nullable=False),
        sa.Column('waktu_mulai', sa.Time, nullable=False),
        sa.Column('waktu_selesai', sa.Time, nullable=False),
        sa.Column('lokasi', sa.String(), nullable=False, server_default=sa.text("'Ruang Prodi'")),
        sa.Column('keterangan', sa.Text(), nullable=True),
    )

def downgrade() -> None:
    op.drop_table('waktu_bimbingan')

    op.create_table(
        'waktu_bimbingan',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('nomor_induk', sa.String(), sa.ForeignKey('dosen.alias', ondelete="CASCADE"), nullable=False),
        sa.Column('jumlah_antrian', sa.Integer, nullable=False, default=5),
        sa.Column('tanggal', sa.Date, nullable=False),
        sa.Column('waktu_mulai', sa.Time, nullable=False),
        sa.Column('waktu_selesai', sa.Time, nullable=False),
    )