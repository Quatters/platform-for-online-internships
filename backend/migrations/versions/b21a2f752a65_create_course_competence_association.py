"""Create course competence association

Revision ID: b21a2f752a65
Revises: f57b7a3742e6
Create Date: 2023-06-04 18:16:41.712116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b21a2f752a65'
down_revision = 'f57b7a3742e6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_course_competence_association',
    sa.Column('course_id', sa.BigInteger(), nullable=False),
    sa.Column('post_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['app_course.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['app_competence.id'], ),
    sa.PrimaryKeyConstraint('course_id', 'post_id')
    )
    op.create_index(op.f('ix_app_course_competence_association_course_id'), 'app_course_competence_association', ['course_id'], unique=False)
    op.create_index(op.f('ix_app_course_competence_association_post_id'), 'app_course_competence_association', ['post_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_app_course_competence_association_post_id'), table_name='app_course_competence_association')
    op.drop_index(op.f('ix_app_course_competence_association_course_id'), table_name='app_course_competence_association')
    op.drop_table('app_course_competence_association')
    # ### end Alembic commands ###
