# api-producto-mysql-estructura-docker

API REST para dar de alta, consultar y eliminar productos usando FastAPI y MySQL. Todo corre con Docker Compose para levantar la API y la base de datos sin tener que instalar MySQL en local.

## Estructura del proyecto

El código está dividido por capas para no mezclar las rutas HTTP con las validaciones ni con el SQL:

- `main.py`: inicializa FastAPI, configura CORS, registra el router y crea la tabla `products` al arrancar (`lifespan`).
- `routers/product_router.py`: define las rutas, valida entradas y salidas con Pydantic (`ProductIn` y `ProductOut`) y convierte los errores del servicio en códigos HTTP.
- `services/product_service.py`: revisa las reglas de negocio (que el nombre no venga vacío y que precio y stock no sean negativos).
- `models/product_model.py`: ejecuta las consultas SQL directas contra MySQL (sin ORM).
- `db.py`: abre la conexión usando variables de entorno y hace algunos reintentos por si MySQL todavía está iniciando.

## Requisitos

- Docker y Docker Compose instalados.
- Puerto `8000` disponible en el equipo.

## Variables de entorno

Antes de arrancar el proyecto, crea tu archivo `.env` a partir del archivo de ejemplo:

```bash
cp .env.example .env
```

El `.env` está en `.gitignore` para no subir credenciales al repositorio. Los datos de `.env.example` son solo para desarrollo local.

## Comandos de Docker Compose

Construir la imagen y levantar los servicios en segundo plano:

```bash
docker compose up --build -d
```

Ver el estado de los contenedores (el servicio `mysql-productos` debe aparecer como `healthy`):

```bash
docker compose ps
```

Consultar los logs de la API o de la base de datos:

```bash
docker compose logs -f api
docker compose logs -f mysql-productos
```

Detener y eliminar los contenedores conservando los datos:

```bash
docker compose down
```

## Endpoints

Con los contenedores corriendo, Swagger queda disponible en `http://localhost:8000/docs`.

| Método | Ruta | Descripción | Códigos |
| --- | --- | --- | --- |
| GET | `/` | Comprueba que la API responde | 200 |
| POST | `/products/` | Crea un producto nuevo | 201, 400 |
| GET | `/products/` | Lista los productos guardados | 200 |
| DELETE | `/products/{product_id}` | Elimina un producto por su ID | 204, 404 |

## Persistencia (volumen)

MySQL guarda sus datos en el volumen `db_data` montado en `/var/lib/mysql`. Por eso, aunque se ejecute `docker compose down` y después `docker compose up -d`, los registros siguen ahí.

Nota: si se corre `docker compose down -v`, también se elimina el volumen y se borran los datos guardados.

## Ejemplos de solicitudes

Crear un producto:

```bash
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Teclado", "price": 250, "stock": 5}'
```

Consultar productos:

```bash
curl http://localhost:8000/products/
```

Eliminar un producto por ID:

```bash
curl -X DELETE http://localhost:8000/products/1
```
