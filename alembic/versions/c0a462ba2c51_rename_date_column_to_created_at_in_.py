"""Rename date column to created_at in file_items table

Revision ID: c0a462ba2c51
Revises: 6788ff57a723
Create Date: 2024-02-11 06:25:48.165228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0a462ba2c51'
down_revision: Union[str, None] = '6788ff57a723'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_chat_messages_id', table_name='chat_messages')
    op.drop_index('ix_chat_sessions_id', table_name='chat_sessions')
    op.add_column('file_items', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
    op.drop_index('ix_file_items_id', table_name='file_items')
    op.drop_column('file_items', 'date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file_items', sa.Column('date', sa.DATETIME(), nullable=True))
    op.create_index('ix_file_items_id', 'file_items', ['id'], unique=False)
    op.drop_column('file_items', 'created_at')
    op.create_index('ix_chat_sessions_id', 'chat_sessions', ['id'], unique=False)
    op.create_index('ix_chat_messages_id', 'chat_messages', ['id'], unique=False)
    # ### end Alembic commands ###