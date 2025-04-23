"""initial superuser

Revision ID: b165f3d2e370
Revises:
Create Date: 2025-03-14 21:51:57.316061

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.core.security import get_password_hash

# revision identifiers, used by Alembic.
revision: str = "b165f3d2e370"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    result = conn.execute(sa.text("SELECT id FROM currencies WHERE code='USDT'"))
    rows = result.fetchall()
    if len(rows) > 0:
        op.execute(
            "INSERT INTO users (email, full_name, hashed_password, is_active, is_superuser, preferred_currency_id) "
            f"VALUES ('admin@example.com', 'Administrator', '{get_password_hash('admin')}', true, true, {rows[0][0]})"
        )
    else:
        op.execute(
            """INSERT INTO currencies (code, name, symbol, is_fiat) VALUES ('USDT', 'Tether', '₮', false);"""
        )
        result = conn.execute(sa.text("SELECT id FROM currencies WHERE code='USDT'"))
        rows = result.fetchall()
        op.execute(
            "INSERT INTO users (email, full_name, hashed_password, is_active, is_superuser, preferred_currency_id) "
            f"VALUES ('admin@example.com', 'Administrator', '{get_password_hash('admin')}', true, true, {rows[0][0]})"
        )


def downgrade() -> None:
    """Downgrade schema."""
    pass
