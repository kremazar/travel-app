"""izlet table

Revision ID: f884e85e4798
Revises: 8ab4eccef997
Create Date: 2019-01-25 11:40:02.137384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f884e85e4798'
down_revision = '8ab4eccef997'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('izlet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('naziv', sa.String(length=140), nullable=True),
    sa.Column('cijena', sa.String(length=140), nullable=True),
    sa.Column('detalji', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('izlet')
    # ### end Alembic commands ###
