"""alter table admin, dosen and mahasiswa

Revision ID: 171f06cb3651
Revises: 6076b75f31cc
Create Date: 2025-04-21 22:19:16.864626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '171f06cb3651'
down_revision: Union[str, None] = '6076b75f31cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ADMIN
    op.drop_constraint('news_admin_id_fkey', 'news', type_='foreignkey')
    op.drop_constraint('admin_pkey', 'admin', type_='primary')
    op.drop_column('admin', 'account_id')
    op.add_column('admin', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('uuid_generate_v4()')))
    op.create_primary_key('admin_pkey', 'admin', ['id'])
    
    # DOSEN
    op.add_column('dosen', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('uuid_generate_v4()')))
    op.execute("UPDATE dosen SET id = uuid_generate_v4() WHERE id IS NULL;")

    # MAHASISWA
    op.add_column('mahasiswa', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=True, server_default=sa.text('uuid_generate_v4()')))
    op.execute("UPDATE mahasiswa SET id = uuid_generate_v4() WHERE id IS NULL;")


def downgrade() -> None:
    # ========== ADMIN ==========
    op.drop_constraint('admin_pkey', 'admin', type_='primary')
    op.add_column('admin', sa.Column('account_id', sa.Integer(), autoincrement=True, nullable=False))
    op.create_primary_key('admin_pkey', 'admin', ['account_id'])

    # ========== DOSEN ==========
    op.drop_constraint('dosen_pkey', 'dosen', type_='primary')
    op.drop_column('dosen', 'id')
    op.create_primary_key('dosen_pkey', 'dosen', ['alias'])

    # ========== MAHASISWA ==========
    op.drop_constraint('mahasiswa_pkey', 'mahasiswa', type_='primary')
    op.drop_constraint('uq_mahasiswa_nim', 'mahasiswa', type_='unique')
    op.drop_column('mahasiswa', 'id')
    op.create_primary_key('mahasiswa_pkey', 'mahasiswa', ['nim'])
