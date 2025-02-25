from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.cnx import sessionlocal
from estadoTareas.entity import Estado

estado_router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

# Crear un nuevo estado
@estado_router.post('/', status_code=201)
async def crear_estado(estado: str, db: Session = Depends(get_db)):
    try:
        estado_existente = db.query(Estado).filter(Estado.estado == estado).first()
        if estado_existente:
            raise HTTPException(status_code=400, detail="El estado ya existe.")
        
        nuevo_estado = Estado(estado=estado)
        db.add(nuevo_estado)
        db.commit()
        db.refresh(nuevo_estado)
        return {"mensaje": "Estado creado con éxito", "estado": nuevo_estado}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")

# Listar todos los estados
@estado_router.get('/', status_code=200)
async def listar_estados(db: Session = Depends(get_db)):
    try:
        estados = db.query(Estado).all()
        if not estados:
            raise HTTPException(status_code=404, detail="No se encontraron estados.")
        return estados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
