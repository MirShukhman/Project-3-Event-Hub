"""empty message

Revision ID: f895e5cd3a5f
Revises: 2e7b5f9b333a
Create Date: 2024-02-25 13:39:19.513971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f895e5cd3a5f'
down_revision = '2e7b5f9b333a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('EventCategories',
    sa.Column('CategoryID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('EventCategory', sa.String(length=50), nullable=False),
    sa.Column('Description', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('CategoryID'),
    sa.UniqueConstraint('EventCategory')
    )
    op.create_table('Users',
    sa.Column('UserID', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('Username', sa.String(length=50), nullable=False),
    sa.Column('PasswordHash', sa.String(length=80), nullable=False),
    sa.Column('Email', sa.String(length=50), nullable=False),
    sa.Column('FullName', sa.String(length=100), nullable=False),
    sa.Column('ProfileDescription', sa.String(length=300), nullable=True),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('IsActive', sa.Boolean(), nullable=True),
    sa.Column('IsMasterUser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('UserID'),
    sa.UniqueConstraint('Email'),
    sa.UniqueConstraint('Username')
    )
    op.create_table('Events',
    sa.Column('EventID', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('Title', sa.String(length=100), nullable=False),
    sa.Column('Description', sa.String(length=1000), nullable=True),
    sa.Column('Location', sa.String(length=300), nullable=False),
    sa.Column('EventDateTime', sa.DateTime(), nullable=False),
    sa.Column('EventImage', sa.LargeBinary(), nullable=True),
    sa.Column('OrganizerID', sa.BigInteger(), nullable=False),
    sa.Column('CategoryID', sa.Integer(), nullable=False),
    sa.Column('IsPrivate', sa.Boolean(), nullable=False),
    sa.Column('IsCanceled', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['CategoryID'], ['EventCategories.CategoryID'], ),
    sa.ForeignKeyConstraint(['OrganizerID'], ['Users.UserID'], ),
    sa.PrimaryKeyConstraint('EventID')
    )
    op.create_table('EventImages',
    sa.Column('ImageID', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('EventID', sa.BigInteger(), nullable=False),
    sa.Column('Image', sa.LargeBinary(), nullable=False),
    sa.Column('UserID', sa.BigInteger(), nullable=False),
    sa.Column('SubmittionDateTime', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['EventID'], ['Events.EventID'], ),
    sa.ForeignKeyConstraint(['UserID'], ['Users.UserID'], ),
    sa.PrimaryKeyConstraint('ImageID')
    )
    op.create_table('Registrations',
    sa.Column('RegistrationID', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('EventID', sa.BigInteger(), nullable=False),
    sa.Column('UserID', sa.BigInteger(), nullable=False),
    sa.Column('RegistrationDateTime', sa.DateTime(), nullable=False),
    sa.Column('Status', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['EventID'], ['Events.EventID'], ),
    sa.ForeignKeyConstraint(['UserID'], ['Users.UserID'], ),
    sa.PrimaryKeyConstraint('RegistrationID')
    )
    op.create_table('Feedback',
    sa.Column('FeedbackID', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('RegistrationID', sa.BigInteger(), nullable=False),
    sa.Column('Raiting', sa.Integer(), nullable=True),
    sa.Column('Comment', sa.String(length=1000), nullable=True),
    sa.Column('SubmittionDateTime', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['RegistrationID'], ['Registrations.RegistrationID'], ),
    sa.PrimaryKeyConstraint('FeedbackID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Feedback')
    op.drop_table('Registrations')
    op.drop_table('EventImages')
    op.drop_table('Events')
    op.drop_table('Users')
    op.drop_table('EventCategories')
    # ### end Alembic commands ###
