"""add tables for reality project

Revision ID: ecec92b4fb72
Revises: 09d446f53008
Create Date: 2022-06-22 18:55:24.870030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecec92b4fb72'
down_revision = '09d446f53008'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('configuration',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location_enabled', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_configuration_id'), 'configuration', ['id'], unique=False)
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pending', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contact_id'), 'contact', ['id'], unique=False)
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lng', sa.Integer(), nullable=True),
    sa.Column('lat', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_location_id'), 'location', ['id'], unique=False)
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('read', sa.Integer(), nullable=True),
    sa.Column('data', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_id'), 'notification', ['id'], unique=False)
    op.create_table('report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('problem', sa.Integer(), nullable=True),
    sa.Column('description', sa.Integer(), nullable=True),
    sa.Column('image', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_report_id'), 'report', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_report_id'), table_name='report')
    op.drop_table('report')
    op.drop_index(op.f('ix_notification_id'), table_name='notification')
    op.drop_table('notification')
    op.drop_index(op.f('ix_location_id'), table_name='location')
    op.drop_table('location')
    op.drop_index(op.f('ix_contact_id'), table_name='contact')
    op.drop_table('contact')
    op.drop_index(op.f('ix_configuration_id'), table_name='configuration')
    op.drop_table('configuration')
    # ### end Alembic commands ###
