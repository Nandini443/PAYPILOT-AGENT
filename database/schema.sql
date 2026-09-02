-- PayPilot Agent Database Schema
-- SQLite 3 compatible with indexes for fast analytical aggregations

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    rating REAL NOT NULL,
    review_count INTEGER NOT NULL,
    stock INTEGER NOT NULL,
    brand TEXT NOT NULL,
    features TEXT NOT NULL,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);
CREATE INDEX IF NOT EXISTS idx_products_rating ON products(rating);

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    age_group TEXT NOT NULL,
    location TEXT NOT NULL,
    customer_segment TEXT NOT NULL,
    previous_orders INTEGER NOT NULL DEFAULT 0,
    average_order_value REAL NOT NULL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_customers_segment ON customers(customer_segment);
CREATE INDEX IF NOT EXISTS idx_customers_location ON customers(location);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    amount REAL NOT NULL,
    order_status TEXT NOT NULL, -- PENDING, COMPLETED, CANCELLED, ABANDONED
    checkout_status TEXT NOT NULL, -- INITIATED, COMPLETED, ABANDONED
    payment_status TEXT NOT NULL, -- PENDING, SUCCESS, FAILED, REFUNDED
    items_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(order_status);
CREATE INDEX IF NOT EXISTS idx_orders_checkout_status ON orders(checkout_status);
CREATE INDEX IF NOT EXISTS idx_orders_payment_status ON orders(payment_status);
CREATE INDEX IF NOT EXISTS idx_orders_timestamp ON orders(timestamp);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    product_id TEXT,
    timestamp TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_method TEXT NOT NULL, -- UPI, Card, Net Banking, Wallet
    payment_status TEXT NOT NULL, -- INITIATED, PROCESSING, SUCCESS, FAILED
    failure_reason TEXT, -- TIMEOUT, BANK_DECLINED, INSUFFICIENT_FUNDS, NETWORK_ERROR, INVALID_REQUEST, NONE
    processing_time REAL NOT NULL, -- in seconds
    device_type TEXT NOT NULL, -- Mobile, Desktop, Tablet
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE INDEX IF NOT EXISTS idx_tx_order ON transactions(order_id);
CREATE INDEX IF NOT EXISTS idx_tx_status ON transactions(payment_status);
CREATE INDEX IF NOT EXISTS idx_tx_method ON transactions(payment_method);
CREATE INDEX IF NOT EXISTS idx_tx_failure ON transactions(failure_reason);
CREATE INDEX IF NOT EXISTS idx_tx_timestamp ON transactions(timestamp);
