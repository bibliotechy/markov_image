"""create pixel table

Revision ID: a5ae847daa02
Revises: 
Create Date: 2020-11-29 21:05:36.377683

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY


# revision identifiers, used by Alembic.
revision = 'a5ae847daa02'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pixel",
        sa.Column('center', sa.VARCHAR(6), primary_key=True),
        sa.Column('ring',   ARRAY(sa.String, dimensions=1))
    )
    op.create_index('pixel_center_index', 'pixel', ["center"])



def downgrade():
    op.drop_table("pixel")
    op.drop_index("pixel_ring_index")
