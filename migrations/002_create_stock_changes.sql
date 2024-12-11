CREATE TABLE stock_transactions (
    id SERIAL PRIMARY KEY,
    stock VARCHAR(12),
    created_at DATE DEFAULT CURRENT_DATE,
    percent FLOAT,
    value NUMERIC
);
