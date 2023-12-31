"""Add password_hash column to user table

Revision ID: c0de4cfb4965
Revises: 54a72074dfc5
Create Date: 2023-06-13 12:35:18.855554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0de4cfb4965'
down_revision = '54a72074dfc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_user')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=False, server_default=''))
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=100), nullable=False))
        batch_op.drop_column('user', 'password_hash')

    op.create_table('_alembic_tmp_user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=100), nullable=False),
    sa.Column('username', sa.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###
