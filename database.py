import sqlite3
import hashlib
from datetime import datetime
import os

DATABASE_PATH = "marketplace.db"

def get_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with all required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('farmer', 'consumer', 'admin')),
            full_name TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    """)
    
    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            unit TEXT NOT NULL,
            quantity_available REAL NOT NULL,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (farmer_id) REFERENCES users(id)
        )
    """)
    
    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consumer_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
            delivery_address TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consumer_id) REFERENCES users(id)
        )
    """)
    
    # Order items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            farmer_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            price_per_unit REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (farmer_id) REFERENCES users(id)
        )
    """)
    
    # Reviews table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            consumer_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (consumer_id) REFERENCES users(id)
        )
    """)
    
    # Cart table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consumer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consumer_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id),
            UNIQUE(consumer_id, product_id)
        )
    """)
    
    conn.commit()
    conn.close()
    
    # Create uploads directory
    os.makedirs("static/uploads", exist_ok=True)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

# ==================== USER OPERATIONS ====================

def create_user(username, email, password, role, full_name, phone="", address=""):
    """Create a new user"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed_pw = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, email, password, role, full_name, phone, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, email, hashed_pw, role, full_name, phone, address))
        conn.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError as e:
        return False, "Username or email already exists"
    finally:
        conn.close()

def authenticate_user(username, password):
    """Authenticate user and return user data"""
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    cursor.execute("""
        SELECT * FROM users WHERE username = ? AND password = ? AND is_active = 1
    """, (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def update_user_profile(user_id, full_name, phone, address):
    """Update user profile"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET full_name = ?, phone = ?, address = ?
        WHERE id = ?
    """, (full_name, phone, address, user_id))
    conn.commit()
    conn.close()

# ==================== PRODUCT OPERATIONS ====================

def create_product(farmer_id, name, category, description, price, unit, quantity, image_path=""):
    """Create a new product"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (farmer_id, name, category, description, price, unit, quantity_available, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (farmer_id, name, category, description, price, unit, quantity, image_path))
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return product_id

def get_all_products(active_only=True):
    """Get all products"""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT p.*, u.full_name as farmer_name, u.phone as farmer_phone
        FROM products p
        JOIN users u ON p.farmer_id = u.id
    """
    if active_only:
        query += " WHERE p.is_active = 1 AND p.quantity_available > 0"
    query += " ORDER BY p.created_at DESC"
    cursor.execute(query)
    products = cursor.fetchall()
    conn.close()
    return [dict(p) for p in products]

def get_products_by_farmer(farmer_id):
    """Get all products by a specific farmer"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM products WHERE farmer_id = ? ORDER BY created_at DESC
    """, (farmer_id,))
    products = cursor.fetchall()
    conn.close()
    return [dict(p) for p in products]

def get_product_by_id(product_id):
    """Get product by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, u.full_name as farmer_name, u.phone as farmer_phone, u.address as farmer_address
        FROM products p
        JOIN users u ON p.farmer_id = u.id
        WHERE p.id = ?
    """, (product_id,))
    product = cursor.fetchone()
    conn.close()
    return dict(product) if product else None

def update_product(product_id, name, category, description, price, unit, quantity, image_path=None):
    """Update product details"""
    conn = get_connection()
    cursor = conn.cursor()
    if image_path:
        cursor.execute("""
            UPDATE products 
            SET name = ?, category = ?, description = ?, price = ?, unit = ?, 
                quantity_available = ?, image_path = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (name, category, description, price, unit, quantity, image_path, product_id))
    else:
        cursor.execute("""
            UPDATE products 
            SET name = ?, category = ?, description = ?, price = ?, unit = ?, 
                quantity_available = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (name, category, description, price, unit, quantity, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    """Soft delete product"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET is_active = 0 WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def search_products(query, category=None):
    """Search products by name or category"""
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT p.*, u.full_name as farmer_name
        FROM products p
        JOIN users u ON p.farmer_id = u.id
        WHERE p.is_active = 1 AND p.quantity_available > 0
        AND (p.name LIKE ? OR p.description LIKE ?)
    """
    params = [f"%{query}%", f"%{query}%"]
    
    if category:
        sql += " AND p.category = ?"
        params.append(category)
    
    sql += " ORDER BY p.created_at DESC"
    cursor.execute(sql, params)
    products = cursor.fetchall()
    conn.close()
    return [dict(p) for p in products]

# ==================== CART OPERATIONS ====================

def add_to_cart(consumer_id, product_id, quantity):
    """Add item to cart"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO cart (consumer_id, product_id, quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(consumer_id, product_id) 
            DO UPDATE SET quantity = quantity + ?
        """, (consumer_id, product_id, quantity, quantity))
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        conn.close()

def get_cart_items(consumer_id):
    """Get all cart items for a consumer"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, p.name, p.price, p.unit, p.quantity_available, p.image_path,
               u.full_name as farmer_name
        FROM cart c
        JOIN products p ON c.product_id = p.id
        JOIN users u ON p.farmer_id = u.id
        WHERE c.consumer_id = ? AND p.is_active = 1
        ORDER BY c.added_at DESC
    """, (consumer_id,))
    items = cursor.fetchall()
    conn.close()
    return [dict(item) for item in items]

def update_cart_quantity(consumer_id, product_id, quantity):
    """Update cart item quantity"""
    conn = get_connection()
    cursor = conn.cursor()
    if quantity <= 0:
        cursor.execute("DELETE FROM cart WHERE consumer_id = ? AND product_id = ?", 
                      (consumer_id, product_id))
    else:
        cursor.execute("""
            UPDATE cart SET quantity = ? WHERE consumer_id = ? AND product_id = ?
        """, (quantity, consumer_id, product_id))
    conn.commit()
    conn.close()

def clear_cart(consumer_id):
    """Clear all items from cart"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE consumer_id = ?", (consumer_id,))
    conn.commit()
    conn.close()

# ==================== ORDER OPERATIONS ====================

def create_order(consumer_id, cart_items, delivery_address, phone):
    """Create order from cart items"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Calculate total
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        
        # Create order
        cursor.execute("""
            INSERT INTO orders (consumer_id, total_amount, delivery_address, phone)
            VALUES (?, ?, ?, ?)
        """, (consumer_id, total, delivery_address, phone))
        order_id = cursor.lastrowid
        
        # Create order items and update product quantities
        for item in cart_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, farmer_id, quantity, price_per_unit, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (order_id, item['product_id'], item['farmer_id'], item['quantity'], 
                  item['price'], item['price'] * item['quantity']))
            
            # Update product quantity
            cursor.execute("""
                UPDATE products SET quantity_available = quantity_available - ?
                WHERE id = ?
            """, (item['quantity'], item['product_id']))
        
        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        return None
    finally:
        conn.close()

def get_orders_by_consumer(consumer_id):
    """Get all orders for a consumer"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM orders WHERE consumer_id = ? ORDER BY created_at DESC
    """, (consumer_id,))
    orders = cursor.fetchall()
    conn.close()
    return [dict(order) for order in orders]

def get_orders_by_farmer(farmer_id):
    """Get all orders containing farmer's products"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT o.*, u.full_name as consumer_name, u.phone as consumer_phone
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN users u ON o.consumer_id = u.id
        WHERE oi.farmer_id = ?
        ORDER BY o.created_at DESC
    """, (farmer_id,))
    orders = cursor.fetchall()
    conn.close()
    return [dict(order) for order in orders]

def get_order_items(order_id):
    """Get all items in an order"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT oi.*, p.name as product_name, p.unit, u.full_name as farmer_name
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN users u ON oi.farmer_id = u.id
        WHERE oi.order_id = ?
    """, (order_id,))
    items = cursor.fetchall()
    conn.close()
    return [dict(item) for item in items]

def update_order_status(order_id, status):
    """Update order status"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, order_id))
    conn.commit()
    conn.close()

# ==================== REVIEW OPERATIONS ====================

def add_review(product_id, consumer_id, rating, comment):
    """Add a product review"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO reviews (product_id, consumer_id, rating, comment)
            VALUES (?, ?, ?, ?)
        """, (product_id, consumer_id, rating, comment))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_product_reviews(product_id):
    """Get all reviews for a product"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, u.full_name as consumer_name
        FROM reviews r
        JOIN users u ON r.consumer_id = u.id
        WHERE r.product_id = ?
        ORDER BY r.created_at DESC
    """, (product_id,))
    reviews = cursor.fetchall()
    conn.close()
    return [dict(review) for review in reviews]

def get_product_rating(product_id):
    """Get average rating for a product"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(rating) as avg_rating, COUNT(*) as review_count
        FROM reviews WHERE product_id = ?
    """, (product_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'avg_rating': round(result['avg_rating'], 1) if result['avg_rating'] else 0,
            'review_count': result['review_count']
        }
    return {'avg_rating': 0, 'review_count': 0}

# ==================== ANALYTICS ====================

def get_farmer_stats(farmer_id):
    """Get statistics for a farmer"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total products
    cursor.execute("SELECT COUNT(*) as count FROM products WHERE farmer_id = ? AND is_active = 1", (farmer_id,))
    total_products = cursor.fetchone()['count']
    
    # Total orders
    cursor.execute("SELECT COUNT(DISTINCT order_id) as count FROM order_items WHERE farmer_id = ?", (farmer_id,))
    total_orders = cursor.fetchone()['count']
    
    # Total revenue
    cursor.execute("SELECT SUM(subtotal) as revenue FROM order_items WHERE farmer_id = ?", (farmer_id,))
    total_revenue = cursor.fetchone()['revenue'] or 0
    
    conn.close()
    return {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': round(total_revenue, 2)
    }

# Initialize database on import
init_database()
