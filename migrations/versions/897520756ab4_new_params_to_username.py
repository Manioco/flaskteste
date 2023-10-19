"""New params to username

Revision ID: 897520756ab4
Revises: 
Create Date: 2023-10-19 10:00:55.921149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '897520756ab4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_users_username", ['username'])
    # with op.batch_alter_table('users', schema=None, naming_convention={"uq": "uq_%(table_name)s_%(column_0_name)s"}) as batch_op:
    #     batch_op.create_unique_constraint('uq_users_username', 'users', ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###