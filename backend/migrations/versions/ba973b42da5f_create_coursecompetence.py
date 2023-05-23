"""Create CourseCompetence

Revision ID: ba973b42da5f
Revises: f57b7a3742e6
Create Date: 2023-05-23 15:45:13.247009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba973b42da5f'
down_revision = 'f57b7a3742e6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_coursecompetence',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('competence_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['competence_id'], ['app_competence.id'], ),
    sa.ForeignKeyConstraint(['course_id'], ['app_course.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('course_id', 'competence_id', name='u_course_competence')
    )
    op.create_index(op.f('ix_app_coursecompetence_competence_id'), 'app_coursecompetence', ['competence_id'], unique=False)
    op.create_index(op.f('ix_app_coursecompetence_course_id'), 'app_coursecompetence', ['course_id'], unique=False)
    op.create_index(op.f('ix_app_coursecompetence_id'), 'app_coursecompetence', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_app_coursecompetence_id'), table_name='app_coursecompetence')
    op.drop_index(op.f('ix_app_coursecompetence_course_id'), table_name='app_coursecompetence')
    op.drop_index(op.f('ix_app_coursecompetence_competence_id'), table_name='app_coursecompetence')
    op.drop_table('app_coursecompetence')
    # ### end Alembic commands ###
