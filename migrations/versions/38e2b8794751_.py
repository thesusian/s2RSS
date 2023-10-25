"""empty message

Revision ID: 38e2b8794751
Revises: 0d25979a0c81
Create Date: 2023-10-25 19:27:27.278917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38e2b8794751'
down_revision = '0d25979a0c81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feed', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pattern', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feed', schema=None) as batch_op:
        batch_op.drop_column('pattern')

    # ### end Alembic commands ###