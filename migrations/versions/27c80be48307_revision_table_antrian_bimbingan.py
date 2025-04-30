"""Revision table antrian_bimbingan

Revision ID: 27c80be48307
Revises: f2eabd09c5e1
Create Date: 2025-04-27 03:32:33.345179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '27c80be48307'
down_revision: Union[str, None] = 'f2eabd09c5e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('files')
    op.drop_table('antrian_bimbingan')
    op.create_table(
        'antrian_bimbingan',
        sa.Column('id_antrian', postgresql.UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4),
        sa.Column('mahasiswa_nim', sa.String(), sa.ForeignKey('mahasiswa.nim', ondelete="CASCADE"), nullable=False),
        sa.Column('waktu_id', sa.Integer(), sa.ForeignKey('waktu_bimbingan.id', ondelete="CASCADE"), nullable=False),
        sa.Column('dosen_inisial', sa.String(), sa.ForeignKey('dosen.alias', ondelete="CASCADE"), nullable=False),
        sa.Column('status_antrian', sa.String(), nullable=False, default="Menunggu"),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_table(
        'files',
        sa.Column('file_id', postgresql.UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4),
        sa.Column('antrian_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('antrian_bimbingan.id_antrian', ondelete="CASCADE"), nullable=False),
        sa.Column('mahasiswa_nim', sa.String(), sa.ForeignKey('mahasiswa.nim', ondelete="CASCADE"), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('file_url', sa.String(), nullable=False),
        sa.Column('is_checked', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('keterangan', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('update_at', sa.DateTime(), nullable=True, onupdate=sa.func.now())
    )

def downgrade() -> None:
    pass
