"""empty message

Revision ID: d85e41e9a86e
Revises: 9e45f14b1687
Create Date: 2024-06-22 23:40:39.020300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd85e41e9a86e'
down_revision = '9e45f14b1687'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('areas', sa.Column('finaliza', sa.Boolean(), nullable=True, default=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('areas', 'finaliza')
    # ### end Alembic commands ###
