"""empty message

Revision ID: 9df4f79f02ab
Revises: 
Create Date: 2020-04-05 19:02:59.741497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9df4f79f02ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pet', 'posted_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pet', 'posted_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
