"""empty message

Revision ID: b1a25588085e
Revises: 50946175e3b6
Create Date: 2024-06-15 14:34:55.524075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1a25588085e'
down_revision = '50946175e3b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tipos_incidentes', sa.Column('descripcion', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tipos_incidentes', 'descripcion')
    # ### end Alembic commands ###