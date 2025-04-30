"""Drop and recreate news table

Revision ID: 1b42335c38cd
Revises: 42b95972e594
Create Date: 2025-04-28 20:00:50.550309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b42335c38cd'
down_revision: Union[str, None] = '42b95972e594'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('news')
    op.create_table(
        'news',
        sa.Column('news_id', sa.UUID(as_uuid=True), primary_key=True, index=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('author_name', sa.String(255), nullable=False, default="Admin"),
        sa.Column('author_email', sa.String(255), nullable=True),
        sa.Column('picture_url', sa.String(500), nullable=True),
        sa.Column('picture_description', sa.String(255), nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('subtitle', sa.String(255), nullable=True),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('status', sa.String(50), nullable=False, default="draft"),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('update_at', sa.DateTime, onupdate=sa.func.now()),
    )

def downgrade() -> None:
    op.drop_table('news')
    op.create_table(
        'news',
        sa.Column('news_id', sa.UUID(as_uuid=True), primary_key=True, index=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('author_name', sa.String(255), nullable=False, default="Admin"),
        sa.Column('author_email', sa.String(255), nullable=True),
        sa.Column('picture_url', sa.String(500), nullable=True),
        sa.Column('picture_description', sa.String(255), nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('subtitle', sa.String(255), nullable=True),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('status', sa.String(50), nullable=False, default="draft"),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('update_at', sa.DateTime, onupdate=sa.func.now()),
    )
