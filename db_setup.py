# db_setup.py
import duckdb

def init_db():
    conn = duckdb.connect("sales.duckdb")
    
    # Customers Table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name VARCHAR,
            region VARCHAR,
            signup_date DATE
        )
    """)
    
    # Sales Table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            transaction_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_category VARCHAR,
            amount DOUBLE,
            transaction_date DATE,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)

    # Insert Sample Data if empty
    if conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0] == 0:
        conn.execute("""
            INSERT INTO customers VALUES
            (1, 'Aarav Sharma', 'North', '2024-01-15'),
            (2, 'Priya Patel', 'West', '2024-02-20'),
            (3, 'Rohan Verma', 'South', '2024-03-10'),
            (4, 'Sneha Iyer', 'East', '2024-04-05');

            INSERT INTO sales VALUES
            (101, 1, 'Electronics', 1200.50, '2026-01-10'),
            (102, 2, 'Clothing', 350.00, '2026-01-12'),
            (103, 1, 'Electronics', 800.00, '2026-02-01'),
            (104, 3, 'Home & Kitchen', 450.75, '2026-02-15'),
            (105, 4, 'Electronics', 2100.00, '2026-03-01'),
            (106, 2, 'Electronics', 950.00, '2026-03-05'),
            (107, 3, 'Clothing', 200.00, '2026-03-10');
        """)
        print("Database initialized with sample tables & records!")
    else:
        print("Database already populated.")
        
    conn.close()

if __name__ == "__main__":
    init_db()