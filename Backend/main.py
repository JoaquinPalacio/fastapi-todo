from fastapi import FastAPI
# conexion con mongodb
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
# rutas
from routes import router
# cors
from fastapi.middleware.cors import CORSMiddleware
# variables de entorno
import os
from dotenv import load_dotenv

# lifespan se ejecuta al iniciar el servidor
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # se cargan las variables de entorno
        load_dotenv()
        url = os.environ.get("DATABASE_URL")
        # conexion con mongodb
        app.mongodb_client = AsyncIOMotorClient(url)
        app.mongodb = app.mongodb_client.todo_db
        router.mongodb = app.mongodb
        yield
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
    finally:
        if app.mongodb_client:
            app.mongodb_client.close()

# ejecuta el servidor con el lifespan(la conexion a base de datos)
app = FastAPI(lifespan=lifespan)

# ruta de la api
app.include_router(router, prefix="/todos", tags=["todos"])

# ruta raiz (de inicio)
@app.get("/")
async def root():
    return {"message": "Bienvenido a tu gestor de tareas"}


# conexiones http de diferentes origenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambia esto a la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)