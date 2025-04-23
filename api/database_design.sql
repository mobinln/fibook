-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    preferred_currency_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Asset Types table
CREATE TABLE asset_types (
    asset_type_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Currencies table
CREATE TABLE currencies (
    currency_id SERIAL PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE,  -- e.g., USD, EUR
    name VARCHAR(50) NOT NULL,
    symbol VARCHAR(5) NOT NULL,        -- e.g., $, €
    is_fiat BOOLEAN DEFAULT TRUE,      -- To differentiate fiat from crypto
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Assets table
CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,
    asset_type_id INTEGER NOT NULL REFERENCES asset_types(asset_type_id),
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    currency_id INTEGER REFERENCES currencies(currency_id),  -- For assets priced in specific currencies
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, asset_type_id)  -- Same symbol can exist in different asset types
);

-- Portfolios table
CREATE TABLE portfolios (
    portfolio_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    base_currency_id INTEGER NOT NULL REFERENCES currencies(currency_id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, name)
);

-- Portfolio Holdings table (tracks current holdings)
CREATE TABLE portfolio_holdings (
    holding_id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolios(portfolio_id),
    asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
    quantity DECIMAL(28, 8) NOT NULL DEFAULT 0,
    avg_purchase_price DECIMAL(28, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(portfolio_id, asset_id)
);

-- Transactions table (for all buy, sell, convert operations)
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolios(portfolio_id),
    transaction_type VARCHAR(20) NOT NULL,  -- 'BUY', 'SELL', 'CONVERT', 'DIVIDEND', etc.
    source_asset_id INTEGER REFERENCES assets(asset_id),
    source_quantity DECIMAL(28, 8),
    source_price DECIMAL(28, 8),
    target_asset_id INTEGER REFERENCES assets(asset_id),
    target_quantity DECIMAL(28, 8),
    target_price DECIMAL(28, 8),
    fee_amount DECIMAL(28, 8) DEFAULT 0,
    fee_currency_id INTEGER REFERENCES currencies(currency_id),
    exchange_rate DECIMAL(28, 8),  -- Rate used for conversion
    transaction_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

-- Exchange Rates table (historical)
CREATE TABLE exchange_rates (
    rate_id SERIAL PRIMARY KEY,
    source_currency_id INTEGER NOT NULL REFERENCES currencies(currency_id),
    target_currency_id INTEGER NOT NULL REFERENCES currencies(currency_id),
    rate DECIMAL(28, 8) NOT NULL,
    effective_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_currency_id, target_currency_id, effective_date)
);

-- Current Exchange Rates view (for faster querying of latest rates)
CREATE VIEW current_exchange_rates AS
SELECT DISTINCT ON (source_currency_id, target_currency_id) 
    rate_id, source_currency_id, target_currency_id, rate, effective_date
FROM exchange_rates
ORDER BY source_currency_id, target_currency_id, effective_date DESC;

-- Market Data (OHLC) table
CREATE TABLE market_data (
    data_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
    date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    timeframe VARCHAR(10) NOT NULL,  -- '1m', '5m', '15m', '1h', '4h', '1d', etc.
    open_price DECIMAL(28, 8) NOT NULL,
    high_price DECIMAL(28, 8) NOT NULL,
    low_price DECIMAL(28, 8) NOT NULL,
    close_price DECIMAL(28, 8) NOT NULL,
    volume DECIMAL(28, 8),
    currency_id INTEGER NOT NULL REFERENCES currencies(currency_id),  -- Currency in which prices are denominated
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(asset_id, date_time, timeframe)
);

-- Performance Snapshots (for tracking portfolio performance over time)
CREATE TABLE performance_snapshots (
    snapshot_id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolios(portfolio_id),
    date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    total_value DECIMAL(28, 8) NOT NULL,
    currency_id INTEGER NOT NULL REFERENCES currencies(currency_id),
    daily_return DECIMAL(10, 6),  -- Percentage
    weekly_return DECIMAL(10, 6),  -- Percentage
    monthly_return DECIMAL(10, 6),  -- Percentage
    yearly_return DECIMAL(10, 6),  -- Percentage
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(portfolio_id, date_time)
);

-- Asset Performance Snapshots (for tracking individual asset performance)
CREATE TABLE asset_performance_snapshots (
    snapshot_id SERIAL PRIMARY KEY,
    holding_id INTEGER NOT NULL REFERENCES portfolio_holdings(holding_id),
    date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    market_price DECIMAL(28, 8) NOT NULL,
    total_value DECIMAL(28, 8) NOT NULL,
    currency_id INTEGER NOT NULL REFERENCES currencies(currency_id),
    unrealized_gain_loss DECIMAL(28, 8),
    percentage_gain_loss DECIMAL(10, 6),  -- Percentage
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(holding_id, date_time)
);

-- User Preferences table
CREATE TABLE user_preferences (
    preference_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    default_portfolio_id INTEGER REFERENCES portfolios(portfolio_id),
    theme VARCHAR(20) DEFAULT 'light',
    notification_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Initial Data: Asset Types
INSERT INTO asset_types (name, description) VALUES
('Cryptocurrency', 'Digital or virtual currencies'),
('Stock', 'Individual company shares'),
('ETF', 'Exchange-traded funds'),
('Bond', 'Fixed income securities'),
('Commodity', 'Physical goods like gold, silver, etc.'),
('Cash', 'Fiat currencies'),
('Real Estate', 'Property investments'),
('Other', 'Miscellaneous asset types');

-- Initial Data: Currencies
INSERT INTO currencies (code, name, symbol, is_fiat) VALUES
('USD', 'US Dollar', '$', TRUE),
('EUR', 'Euro', '€', TRUE),
('BTC', 'Bitcoin', '₿', FALSE),
('ETH', 'Ethereum', 'Ξ', FALSE),
('GBP', 'British Pound', '£', TRUE),
('JPY', 'Japanese Yen', '¥', TRUE),
('CHF', 'Swiss Franc', 'Fr', TRUE),
('CAD', 'Canadian Dollar', 'C$', TRUE),
('AUD', 'Australian Dollar', 'A$', TRUE);

-- Create indexes for performance
CREATE INDEX idx_holdings_portfolio ON portfolio_holdings(portfolio_id);
CREATE INDEX idx_transactions_portfolio ON transactions(portfolio_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_market_data_asset_date ON market_data(asset_id, date_time);
CREATE INDEX idx_exchange_rates_date ON exchange_rates(effective_date);
CREATE INDEX idx_performance_portfolio_date ON performance_snapshots(portfolio_id, date_time);