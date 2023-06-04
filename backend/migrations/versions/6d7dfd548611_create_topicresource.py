"""Create TopicResource

Revision ID: 6d7dfd548611
Revises: 9b69cce1bdd4
Create Date: 2023-06-03 13:15:05.704736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d7dfd548611'
down_revision = '9b69cce1bdd4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_topicresource',
    sa.Column('type', sa.Enum('text', 'image', 'video', 'embedded', name='topicresourcetype'), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('value', sa.Text(), nullable=False),
    sa.Column('prev_resource_id', sa.Integer(), nullable=True),
    sa.Column('topic_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.CheckConstraint('prev_resource_id <> id', name='check_prev_resource_id_is_not_self'),
    sa.ForeignKeyConstraint(['prev_resource_id'], ['app_topicresource.id'], ),
    sa.ForeignKeyConstraint(['topic_id'], ['app_topic.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('topic_id', 'prev_resource_id', name='u_prev_resource_per_topic')
    )
    op.create_index(op.f('ix_app_topicresource_id'), 'app_topicresource', ['id'], unique=True)
    op.create_index(op.f('ix_app_topicresource_prev_resource_id'), 'app_topicresource', ['prev_resource_id'], unique=False)
    op.create_index(op.f('ix_app_topicresource_topic_id'), 'app_topicresource', ['topic_id'], unique=False)
    op.create_index(op.f('ix_app_topicresource_type'), 'app_topicresource', ['type'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_app_topicresource_type'), table_name='app_topicresource')
    op.drop_index(op.f('ix_app_topicresource_topic_id'), table_name='app_topicresource')
    op.drop_index(op.f('ix_app_topicresource_prev_resource_id'), table_name='app_topicresource')
    op.drop_index(op.f('ix_app_topicresource_id'), table_name='app_topicresource')
    op.drop_table('app_topicresource')
    # ### end Alembic commands ###
