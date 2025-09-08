-- Sample dataset for Michael - The AI Business Analyst Agent
INSERT INTO customers (customer_id, name, email) VALUES
    (1001, 'Alice Johnson', 'alice@example.com'),
    (1002, 'Bob Smith', 'bob@example.com'),
    (1003, 'Carol Lee', 'carol@example.com')
ON CONFLICT (customer_id) DO NOTHING;

INSERT INTO products (product_id, product_name, description) VALUES
    (1, 'Laptop Pro', 'High-performance laptop with 16GB RAM and 512GB SSD.'),
    (2, 'Smartphone X', 'Latest smartphone with 5G support and 128GB storage.'),
    (3, 'Wireless Headphones', 'Noise-cancelling headphones with 20-hour battery life.'),
    (4, 'Gaming Console', 'Next-gen gaming console with 4K graphics.'),
    (5, 'Smart Watch', 'Fitness tracker with heart rate monitor and GPS.')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO sales (order_id, product_id, customer_id, quantity, unit_price, order_date) VALUES
    (1, 1, 1001, 2, 999.99, '2025-01-15 10:00:00'),
    (2, 2, 1002, 5, 499.99, '2025-02-01 12:35:00'),
    (3, 3, 1003, 10, 99.99, '2025-02-10 09:00:00'),
    (4, 4, 1002, 3, 399.99, '2025-03-05 15:10:00'),
    (5, 5, 1001, 7, 199.99, '2025-03-20 18:20:00'),
    (6, 1, 1003, 1, 999.99, '2025-04-01 11:00:00'),
    (7, 2, 1001, 3, 499.99, '2025-04-15 13:25:00'),
    (8, 3, 1002, 4, 99.99, '2025-05-01 08:45:00')
ON CONFLICT (order_id) DO NOTHING;
