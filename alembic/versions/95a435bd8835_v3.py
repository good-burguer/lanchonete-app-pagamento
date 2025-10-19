"""v3

Revision ID: 95a435bd8835
Revises: 
Create Date: 2025-09-26 20:16:53.404107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '95a435bd8835'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'cliente',
        sa.Column('cliente_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(255)),
        sa.Column('email', sa.String(255)),
        sa.Column('telefone', sa.String(11)),
        sa.Column('cpf', sa.String(11)),
    )

    op.create_table(
        'status_pedido',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('descricao', sa.String(50), nullable=False),
    )

    op.create_table(
        'pedido',
        sa.Column('pedido_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('cliente_id', sa.Integer(), sa.ForeignKey('cliente.cliente_id')),
        sa.Column('status', sa.Integer(), sa.ForeignKey('status_pedido.id'), nullable=False),
        sa.Column('data_criacao', sa.Time(), nullable=False),
        sa.Column('data_alteracao', sa.Time()),
        sa.Column('data_finalizacao', sa.Time()),
    )

    op.create_table(
        'categoria_produto',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(50), nullable=False),
    )

    op.create_table(
        'produto',
        sa.Column('produto_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('descricao', sa.String(255), nullable=False),
        sa.Column('preco', sa.Numeric(), nullable=False),
        sa.Column('categoria', sa.Integer(), sa.ForeignKey('categoria_produto.id')),
        sa.Column('imagem', sa.String(255)),
    )

    op.create_table(
        'pedido_produtos',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('pedido_id', sa.Integer(), sa.ForeignKey('pedido.pedido_id'), nullable=False),
        sa.Column('produto_id', sa.Integer(), sa.ForeignKey('produto.produto_id'), nullable=False),
    )

    op.create_table(
        'pagamento',
        sa.Column('pedido', sa.Integer(), sa.ForeignKey('pedido.pedido_id'), primary_key=True),
        sa.Column('codigo_pagamento', sa.String(255), primary_key=True),
        sa.Column('status', sa.String(100)),
    )

    op.execute(
        """
        INSERT INTO categoria_produto (nome) VALUES 
            ('Lanche'),
            ('Acompanhamento'),
            ('Bebida'),
            ('Sobremesa')
        """
    )

    op.execute(
        """
        INSERT INTO status_pedido (descricao) VALUES 
            ('Recebido'),
            ('Em preparação'),
            ('Pronto'),
            ('Finalizado')
        """
    )

def downgrade():
    op.execute("DELETE FROM status_pedido")
    op.execute("DELETE FROM categoria_produto")

    op.drop_table('pagamento')
    op.drop_table('pedido_produtos')
    op.drop_table('produto')
    op.drop_table('categoria_produto')
    op.drop_table('pedido')
    op.drop_table('status_pedido')
    op.drop_table('cliente')
