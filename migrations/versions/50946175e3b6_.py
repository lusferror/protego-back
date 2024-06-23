"""empty message

Revision ID: 50946175e3b6
Revises: 4be5eb508766
Create Date: 2024-06-15 14:13:32.836417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50946175e3b6'
down_revision = '4be5eb508766'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('areas', sa.Column('descripcion', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('areas', 'descripcion')
    # ### end Alembic commands ###
