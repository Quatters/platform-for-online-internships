"""Add unique constraints for courses and topics

Revision ID: 0c180df3107f
Revises: 1102c863e0f2
Create Date: 2023-05-14 15:26:33.496397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c180df3107f'
down_revision = '1102c863e0f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('u_prev_topic_for_course', 'app_topic', ['course_id', 'prev_topic_id'])
    op.create_unique_constraint('u_user_course', 'app_usercourse', ['user_id', 'course_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('u_user_course', 'app_usercourse', type_='unique')
    op.drop_constraint('u_prev_topic_for_course', 'app_topic', type_='unique')
    # ### end Alembic commands ###