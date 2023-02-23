"""empty message

Revision ID: 0e1fde61787e
Revises: c221d5ab5b6a
Create Date: 2023-02-15 10:04:32.162646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e1fde61787e'
down_revision = 'c221d5ab5b6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('department', schema=None) as batch_op:
        batch_op.drop_column('faculty')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('department', schema=None) as batch_op:
        batch_op.add_column(sa.Column('faculty', sa.VARCHAR(length=50), nullable=True))

    # ### end Alembic commands ###