"""cascade delete on changelog

Revision ID: 1aca885a577d
Revises: 2c45f8ce631b
Create Date: 2022-10-20 23:24:33.981343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aca885a577d'
down_revision = '2c45f8ce631b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('spatial_ref_sys')
    op.drop_constraint('changelog_location_id_fkey', 'changelog', type_='foreignkey')
    op.create_foreign_key(None, 'changelog', 'location', ['location_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'changelog', type_='foreignkey')
    op.create_foreign_key('changelog_location_id_fkey', 'changelog', 'location', ['location_id'], ['id'])
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('(srid > 0) AND (srid <= 998999)', name='spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )
    # ### end Alembic commands ###
