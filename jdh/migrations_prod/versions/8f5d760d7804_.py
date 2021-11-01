"""empty message

Revision ID: 8f5d760d7804
Revises: 
Create Date: 2021-11-01 20:23:30.329147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f5d760d7804'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('equipos',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(), nullable=False),
    sa.Column('codigo', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cuentas',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('equipo_id', sa.BigInteger(), nullable=True),
    sa.Column('patrimonio', sa.Float(), nullable=True),
    sa.Column('balance', sa.Float(), nullable=True),
    sa.Column('beneficio', sa.Float(), nullable=True),
    sa.Column('mov_disponibles', sa.Integer(), nullable=True),
    sa.Column('ult_movimiento', sa.Integer(), nullable=True),
    sa.Column('no_movimientos', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['equipo_id'], ['equipos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('graficos',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('cuenta_id', sa.BigInteger(), nullable=True),
    sa.Column('simbolo', sa.String(), nullable=True),
    sa.Column('mov_disponibles', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cuenta_id'], ['cuentas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posiciones',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('grafico_id', sa.BigInteger(), nullable=True),
    sa.Column('volumen', sa.Float(), nullable=True),
    sa.Column('dia_compra', sa.String(), nullable=True),
    sa.Column('valor_compra', sa.Float(), nullable=True),
    sa.Column('comentario_compra', sa.String(), nullable=True),
    sa.Column('interes_compra', sa.Float(), nullable=True),
    sa.Column('dia_venta', sa.String(), nullable=True),
    sa.Column('valor_venta', sa.Float(), nullable=True),
    sa.Column('comentario_venta', sa.String(), nullable=True),
    sa.Column('interes_venta', sa.Float(), nullable=True),
    sa.Column('balance', sa.Float(), nullable=True),
    sa.Column('cerrado', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['grafico_id'], ['graficos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posiciones')
    op.drop_table('graficos')
    op.drop_table('cuentas')
    op.drop_table('equipos')
    # ### end Alembic commands ###