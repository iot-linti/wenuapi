"""Add alert table

Revision ID: 86b8c79ec64b
Revises: 
Create Date: 2017-09-21 16:47:06.036387

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '86b8c79ec64b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'alert',
        sa.Column('_created', sa.DateTime),
        sa.Column('_updated', sa.DateTime),
        sa.Column('_etag', sa.VarChar(40)),
        sa.Column('_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('mote_id', sa.Integer, sa.ForeignKey('mote_id')),
        sa.Column('measurement_id', sa.Integer, sa.ForeignKey('measurement_id')),
        sa.Column('time', sa.DateTime),
        sa.Column('solved', sa.Boolean),
    )


def downgrade():
    op.drop_table('alert')
