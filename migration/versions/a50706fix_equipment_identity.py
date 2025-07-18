"""
Alembic migration to ensure auto-increment (identity) on equipment, equipment_categories, and equipment_bookings id columns.
"""
revision = 'a50706fixequipid'
down_revision = 'a50706addmanageequip'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    # For PostgreSQL 10+: set GENERATED BY DEFAULT AS IDENTITY
    op.execute("ALTER TABLE equipment ALTER COLUMN id DROP DEFAULT;")
    op.execute("ALTER TABLE equipment ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY;")
    op.execute("ALTER TABLE equipment_categories ALTER COLUMN id DROP DEFAULT;")
    op.execute("ALTER TABLE equipment_categories ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY;")
    op.execute("ALTER TABLE equipment_bookings ALTER COLUMN id DROP DEFAULT;")
    op.execute("ALTER TABLE equipment_bookings ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY;")

def downgrade():
    # Optionally revert to plain integer (not recommended)
    op.execute("ALTER TABLE equipment ALTER COLUMN id DROP IDENTITY IF EXISTS;")
    op.execute("ALTER TABLE equipment_categories ALTER COLUMN id DROP IDENTITY IF EXISTS;")
    op.execute("ALTER TABLE equipment_bookings ALTER COLUMN id DROP IDENTITY IF EXISTS;")
