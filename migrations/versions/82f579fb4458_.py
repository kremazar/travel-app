"""empty message

Revision ID: 82f579fb4458
Revises: 455c24539b3f
Create Date: 2019-01-31 23:20:28.144135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82f579fb4458'
down_revision = '455c24539b3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tablica',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('izlet_id', sa.Integer(), nullable=True),
    sa.Column('rezervirano_mjesto', sa.String(length=140), nullable=True),
    sa.ForeignKeyConstraint(['izlet_id'], ['izlet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tablica')
    # ### end Alembic commands ###
