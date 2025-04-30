"""create user table

Revision ID: 6076b75f31cc
Revises: 82f6ada39843
Create Date: 2025-04-21 22:11:56.125646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '6076b75f31cc'
down_revision: Union[str, None] = '82f6ada39843'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    op.drop_table("user")
    op.create_table(
        'user',
        sa.Column('user_id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('user')
    pass
