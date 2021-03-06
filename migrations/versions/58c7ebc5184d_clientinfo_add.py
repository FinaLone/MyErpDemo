"""ClientInfo add

Revision ID: 58c7ebc5184d
Revises: 3ae5e07a80d8
Create Date: 2016-11-21 21:09:21.480000

"""

# revision identifiers, used by Alembic.
revision = '58c7ebc5184d'
down_revision = '3ae5e07a80d8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('TClientInfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('am_id', sa.Integer(), nullable=True),
    sa.Column('flag', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('sex', sa.Integer(), nullable=True),
    sa.Column('preference', sa.String(), nullable=True),
    sa.Column('race', sa.String(), nullable=True),
    sa.Column('id_number', sa.String(), nullable=True),
    sa.Column('birthday', sa.DATE(), nullable=True),
    sa.Column('account_number', sa.Integer(), nullable=True),
    sa.Column('phone_1', sa.String(), nullable=True),
    sa.Column('phone_2', sa.String(), nullable=True),
    sa.Column('phone_3', sa.String(), nullable=True),
    sa.Column('occupation', sa.String(), nullable=True),
    sa.Column('workplace', sa.String(), nullable=True),
    sa.Column('home', sa.String(), nullable=True),
    sa.Column('hobby', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['am_id'], ['TUserInfo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TClientInfo')
    ### end Alembic commands ###
