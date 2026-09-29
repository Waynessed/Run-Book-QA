from alembic import op
from app.db import Base

revision = "001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    Base.metadata.create_all(op.get_bind())
    op.execute("CREATE INDEX chunks_fts ON chunks USING gin(to_tsvector('english', text))")

def downgrade():
    Base.metadata.drop_all(op.get_bind())
