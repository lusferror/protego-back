"""empty message

Revision ID: af440ce3d155
Revises: 184a168804da
Create Date: 2024-06-15 00:49:47.932956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af440ce3d155'
down_revision = '184a168804da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lineas', sa.Column('descripcion', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lineas', 'descripcion')
    # ### end Alembic commands ###