from models.product_model import (
    Product,
    insert_product,
    get_all_products,
    delete_product,
)


def add_product(data: dict) -> Product:
    """Verifica reglas de negocio y delega el guardado."""
    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not name or not name.strip():
        raise ValueError("El nombre es obligatorio.")
    if price < 0:
        raise ValueError("El precio no puede ser negativo.")
    if stock < 0:
        raise ValueError("El stock no puede ser negativo.")

    return insert_product(name, price, stock)


def list_products() -> list[Product]:
    """Solicita al modelo los productos almacenados."""
    return get_all_products()


def remove_product(product_id: int) -> None:
    """Comprueba si el producto se elimino."""
    if not delete_product(product_id):
        raise ValueError("Producto no encontrado.")
