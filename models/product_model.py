from db import get_connection


class Product:
    """Representa un producto recuperado de MySQL."""

    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock


def create_table_if_not_exists():
    """Crea la tabla si todavia no existe."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price FLOAT NOT NULL,
                stock INT NOT NULL
            )
        """)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def insert_product(name: str, price: float, stock: int) -> Product:
    """Inserta y devuelve el nuevo producto."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
            (name, price, stock),
        )
        conn.commit()
        return Product(cursor.lastrowid, name, price, stock)
    finally:
        cursor.close()
        conn.close()


def get_all_products() -> list[Product]:
    """Consulta todos los productos."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, name, price, stock FROM products")
        return [Product(**row) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()


def delete_product(product_id: int) -> bool:
    """Elimina el producto y devuelve si existia."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()
