-- Schema for Michael - The AI Business Analyst Agent
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    customer_id INT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_id INT UNIQUE NOT NULL,
    product_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    order_id INT UNIQUE NOT NULL,
    product_id INT NOT NULL,
    customer_id INT,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (product_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    generated_sql TEXT,
    answer_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
