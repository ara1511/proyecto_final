from fastapi import FastAPI
from default.defaultmodel import Base
from config.cnx import engine

# Ruotes
from default.routes import default
from usuarios.routes import usuario_router
from tareas.routes import tarea_router
from estadoTareas.routes import estado_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API Rest FastAPI",
    description="Ejemplo de API Rest con FASTAPI",
    version="0.0.1",
        contact={
        "name": "Soporte Técnico",
        "email": "soporte@miempresa.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Origins admited
origins = ["*"]

# Add Middleware CORS (Cross-Origin Resource Sharing )
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruotes Apps
app.include_router(default, prefix='', tags=['App Routes Default'])
app.include_router(usuario_router, prefix='/usuarios', tags=['usuario Endpoints'])
app.include_router(tarea_router, prefix='/tareas', tags=['tarea Endpoints'])
app.include_router(estado_router, prefix='/estados', tags=['estado Endpoints'])

Base.metadata.create_all(bind=engine)