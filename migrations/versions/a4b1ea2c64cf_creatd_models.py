"""creatd models

Revision ID: a4b1ea2c64cf
Revises: 
Create Date: 2022-09-10 22:00:29.491542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4b1ea2c64cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(), nullable=True),
    sa.Column('price', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('item_name')
    )
    op.create_table('workers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('surname', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('purchases',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('sold_item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['login'], ['workers.login'], ),
    sa.ForeignKeyConstraint(['sold_item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('purchases')
    op.drop_table('workers')
    op.drop_table('items')
    # ### end Alembic commands ###
