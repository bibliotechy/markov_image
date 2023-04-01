"""empty message

Revision ID: 5940bbe913e9
Revises: a5ae847daa02
Create Date: 2023-01-01 10:05:09.124708

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

# revision identifiers, used by Alembic.
revision = '5940bbe913e9'
down_revision = 'a5ae847daa02'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pixel2",
        sa.Column('center', sa.VARCHAR(6)),
        sa.Column('ring',   sa.VARCHAR(55)),
        sa.Column('count', sa.INTEGER)
    )
    op.create_index('pixel2_center_index', 'pixel2', ["center"])
    op.create_index('pixel2_center_ring_index', 'pixel2', ["center", "ring"])



def downgrade():
    op.drop_table("pixel2")
    #op.drop_index("pixel2_center_index")
    #op.drop_index("pixel2_center_ring_index")
