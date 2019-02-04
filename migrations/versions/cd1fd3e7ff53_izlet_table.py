"""izlet table

Revision ID: cd1fd3e7ff53
Revises: f98f3f37dcb5
Create Date: 2019-01-29 19:56:25.742913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd1fd3e7ff53'
down_revision = 'f98f3f37dcb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('izlet', sa.Column('broj_putnika', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('izlet', 'broj_putnika')
    # ### end Alembic commands ###