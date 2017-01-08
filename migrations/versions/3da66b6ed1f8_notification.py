"""notification

Revision ID: 3da66b6ed1f8
Revises: 3807e8cb77d7
Create Date: 2017-01-09 02:35:11.369000

"""

# revision identifiers, used by Alembic.
revision = '3da66b6ed1f8'
down_revision = '3807e8cb77d7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('publish_id', sa.Integer(), nullable=True),
    sa.Column('target_role_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('publish_datetime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['publish_id'], ['TUserInfo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_Notification_id', 'Notification', ['id'], unique=False)
    op.create_table('ReadNotification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reader_id', sa.Integer(), nullable=True),
    sa.Column('notification_id', sa.Integer(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('read_datetime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['notification_id'], ['Notification.id'], ),
    sa.ForeignKeyConstraint(['reader_id'], ['TUserInfo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ReadNotification_id', 'ReadNotification', ['id'], unique=False)
    op.add_column(u'TUserInfo', sa.Column('flag', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'TUserInfo', 'flag')
    op.drop_index('ix_ReadNotification_id', 'ReadNotification')
    op.drop_table('ReadNotification')
    op.drop_index('ix_Notification_id', 'Notification')
    op.drop_table('Notification')
    ### end Alembic commands ###
