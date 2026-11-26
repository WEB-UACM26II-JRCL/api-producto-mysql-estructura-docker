from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.product_model import create_table_if_not_exists
from routers.product_router import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Prepara la tabla de productos al iniciar la API."""
    create_table_if_not_exists()
    yield


app = FastAPI(title="API REST Productos con Docker", lifespan=lifespan)

# Para un front local de desarrollo CORS no sustituye autenticacion.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type"],
)

app.include_router(product_router)


@app.get("/")
def root():
    """Comprueba que la API se encuentra funcionando."""
    return {"message": "API de productos funcionando"}
