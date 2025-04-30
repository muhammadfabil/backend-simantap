"""Files Table Revision

Revision ID: 5f0b3171f765
Revises: ab3297a69c20
Create Date: 2025-04-27 00:07:30.494395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
import uuid


# revision identifiers, used by Alembic.
revision: str = '5f0b3171f765'
down_revision: Union[str, None] = 'ab3297a69c20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_table('files')

    op.create_table(
        'files',
        sa.Column('file_id', pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
        sa.Column('antrian_id', sa.Integer(), sa.ForeignKey('antrian_bimbingan.id_antrian'), nullable=False),
        sa.Column('mahasiswa_nim', sa.String(), sa.ForeignKey('mahasiswa.nim'), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('file_url', sa.String(), nullable=False),
        sa.Column('is_checked', sa.Boolean(), nullable=False, default=False),
        sa.Column('keterangan', sa.Text()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, onupdate=sa.text('now()'))
    )
    pass


def downgrade():
    op.drop_table('files')
    pass
