"""add_orden_estado

Revision ID: 53f010415f02
Revises: e6b9d3775965
Create Date: 2024-06-15 20:09:19.777158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53f010415f02'
down_revision = 'e6b9d3775965'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ordenes', sa.Column('estado', sa.String(length=50), nullable=True, comment='Estado de la orden (creada, proceso, finalizada, cancelada, entregada)'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ordenes', 'estado')
    # ### end Alembic commands ###
