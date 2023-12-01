"""empty message

Revision ID: 03a3aefc1188
Revises: a981fc298f81
Create Date: 2023-11-30 19:19:57.944101

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '03a3aefc1188'
down_revision = 'a981fc298f81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('favorites',
               existing_type=sqlite.JSON(),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('favorites',
               existing_type=sa.Text(),
               type_=sqlite.JSON(),
               existing_nullable=True)

    # ### end Alembic commands ###
