"""comentarios_medidas_tabla_productos

Revision ID: 160199235ee7
Revises: 0a874b7c95ad
Create Date: 2024-06-15 16:13:56.020417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '160199235ee7'
down_revision = '0a874b7c95ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('productos', 'ancho',
               existing_type=sa.INTEGER(),
               comment='Ancho en centimetros',
               existing_nullable=True)
    op.alter_column('productos', 'alto',
               existing_type=sa.INTEGER(),
               comment='Alto en centimetros',
               existing_nullable=True)
    op.alter_column('productos', 'largo',
               existing_type=sa.INTEGER(),
               comment='Largo en centimetros',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('productos', 'largo',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Largo en centimetros',
               existing_nullable=True)
    op.alter_column('productos', 'alto',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Alto en centimetros',
               existing_nullable=True)
    op.alter_column('productos', 'ancho',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Ancho en centimetros',
               existing_nullable=True)
    # ### end Alembic commands ###
