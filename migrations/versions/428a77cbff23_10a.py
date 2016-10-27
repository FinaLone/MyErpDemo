"""10a

Revision ID: 428a77cbff23
Revises: 2db411cf1ba2
Create Date: 2016-10-26 01:08:15.186000

"""

# revision identifiers, used by Alembic.
revision = '428a77cbff23'
down_revision = '2db411cf1ba2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TUserInfo', sa.Column('about_me', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('TUserInfo', 'about_me')
    ### end Alembic commands ###