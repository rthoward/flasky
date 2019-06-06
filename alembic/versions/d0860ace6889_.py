"""empty message

Revision ID: d0860ace6889
Revises: 0ff829745685
Create Date: 2019-06-05 21:03:37.734092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d0860ace6889"
down_revision = "0ff829745685"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("events", sa.Column("capacity", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("events", "capacity")
    # ### end Alembic commands ###
