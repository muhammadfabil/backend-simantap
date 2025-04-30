"""Update Table Dosen and Mahasiswa

Revision ID: 1f48e8d840ad
Revises: 1b42335c38cd
Create Date: 2025-04-29 22:59:51.733721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f48e8d840ad'
down_revision: Union[str, None] = '1b42335c38cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add columns to the 'mahasiswa' table
    op.add_column('mahasiswa', sa.Column('status_mahasiswa', sa.String(), nullable=True, server_default='Aktif'))
    op.add_column('mahasiswa', sa.Column('semester_saat_ini', sa.Integer(), nullable=True))
    op.add_column('mahasiswa', sa.Column('avatar_url', sa.String(), nullable=True))

    op.alter_column(
        'dosen',
        'status_kehadiran',
        new_column_name='keterangan',
        existing_type=sa.String(),
        type_=sa.String(),
        existing_nullable=True,
    )

    op.alter_column(
        'dosen',
        'ketersediaan_bimbingan',
        new_column_name='status_kehadiran',
        existing_type=sa.Boolean(),
        type_=sa.Boolean(),
        existing_nullable=True,
        nullable=False,
        existing_server_default=sa.text('true'),
        server_default=sa.text('true'),
    )


def downgrade() -> None:
    op.drop_column('mahasiswa', 'status_mahasiswa')
    op.drop_column('mahasiswa', 'semester_saat_ini')
    op.drop_column('mahasiswa', 'avatar_url')

    op.drop_column('dosen', 'keterangan')

    # Rename 'status_kehadiran' back to 'ketersediaan_bimbingan'
    op.alter_column(
        'dosen',
        'status_kehadiran',
        new_column_name='ketersediaan_bimbingan',
        existing_type=sa.Boolean(),
        type_=sa.String(),
        existing_nullable=True,
        nullable=True,
        postgresql_using="status_kehadiran::text",  # Explicit cast back to String
    )

    # Rename 'keterangan' back to 'status_kehadiran'
    op.alter_column(
        'dosen',
        'keterangan',
        new_column_name='status_kehadiran',
        existing_type=sa.String(),
        type_=sa.String(),
        existing_nullable=True,
    )
