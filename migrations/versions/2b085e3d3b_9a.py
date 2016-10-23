"""9a

Revision ID: 2b085e3d3b
Revises: 1762b6b4e46d
Create Date: 2016-10-24 02:25:51.239000

"""

# revision identifiers, used by Alembic.
revision = '2b085e3d3b'
down_revision = '1762b6b4e46d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TRoleInfo', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('TRoleInfo', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index('ix_TRoleInfo_default', 'TRoleInfo', ['default'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_TRoleInfo_default', 'TRoleInfo')
    op.drop_column('TRoleInfo', 'permissions')
    op.drop_column('TRoleInfo', 'default')
    ### end Alembic commands ###
