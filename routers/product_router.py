from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from services.product_service import add_product, list_products, remove_product

router = APIRouter(prefix="/products", tags=["products"])


class ProductIn(BaseModel):
    """DTO con los datos recibidos del cliente."""
    name: str
    price: float
    stock: int


class ProductOut(BaseModel):
    """DTO con el formato de la respuesta."""
    id: int
    name: str
    price: float
    stock: int


@router.post("/", response_model=ProductOut, status_code=201)
def create_product(product: ProductIn):
    """Recibe datos HTTP y delega al servicio."""
    try:
        new = add_product(product.model_dump())
        return ProductOut(id=new.id, name=new.name, price=new.price, stock=new.stock)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/", response_model=list[ProductOut])
def get_products():
    """Devuelve los productos consultados por el servicio."""
    return [
        ProductOut(id=p.id, name=p.name, price=p.price, stock=p.stock)
        for p in list_products()
    ]


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product_endpoint(product_id: int):
    """Solicita eliminar un producto por identificador."""
    try:
        remove_product(product_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
