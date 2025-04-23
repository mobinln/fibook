"""initial asset types and currencies

Revision ID: 53f0b1daef03
Revises: b165f3d2e370
Create Date: 2025-03-14 21:56:11.364943

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "53f0b1daef03"
down_revision: Union[str, None] = "b165f3d2e370"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    result = conn.execute(sa.text("SELECT id FROM currencies WHERE code='USDT'"))
    rows = result.fetchall()
    if len(rows) == 0:
        op.execute(
            """INSERT INTO currencies (code, name, symbol, is_fiat) VALUES ('USDT', 'Tether', '₮', false);"""
        )

    op.execute(
        """INSERT INTO asset_types (name, description) VALUES
            ('Cryptocurrency', 'Digital or virtual currencies'),
            ('Stock', 'Individual company shares'),
            ('ETF', 'Exchange-traded funds'),
            ('Bond', 'Fixed income securities'),
            ('Commodity', 'Physical goods like gold, silver, etc.'),
            ('Cash', 'Fiat currencies'),
            ('Real Estate', 'Property investments'),
            ('Other', 'Miscellaneous asset types');"""
    )
    op.execute(
        """INSERT INTO currencies (code, name, symbol, is_fiat) VALUES
            ('USD', 'US Dollar', '$', true),
            ('IRR', 'Iran Rial', 'rial', true),
            ('IRT', 'Iran Toman', 'toman', true),
            ('XAUg', 'Gold (1g)', 'Au', false),
            ('EUR', 'Euro', '€', true),
            ('BTC', 'Bitcoin', '₿', false),
            ('ETH', 'Ethereum', 'Ξ', false);"""
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
