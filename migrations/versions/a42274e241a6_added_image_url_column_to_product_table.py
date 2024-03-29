"""Added image_url column to product table

Revision ID: a42274e241a6
Revises: 7d2721816e66
Create Date: 2024-03-02 08:34:59.107019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a42274e241a6'
down_revision = '7d2721816e66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('image_url', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'image_url')
    # ### end Alembic commands ###
