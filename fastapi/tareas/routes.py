from fastapi import APIRouter, HTTPException, Depends
from tareas.dto import TareaDTO, TareaCreateDTO, TareaUpdateDTO
from tareas.service import *
from sqlalchemy.orm import Session
from config.cnx import sessionlocal
from estadoTareas.entity import Estado
from estadoTareas.dto import EstadoTareaUpdate


tarea_router = APIRouter()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@tarea_router.get('/', response_model=list[TareaDTO], status_code=200)
async def get_all_tareas():
    tareas = await get_tareas()
    if not tareas:
        raise HTTPException(status_code=404, detail="No se encontraron tareas")
    return tareas

@tarea_router.get('/{id}', response_model=TareaDTO, status_code=200)
async def get_tarea(id: str):
    tarea = await get_tarea_by_id(id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@tarea_router.post('/', response_model=TareaDTO, status_code=201)
async def create_tarea(tarea: TareaCreateDTO):
    nueva_tarea = await create_tarea_service(tarea)
    if not nueva_tarea:
        raise HTTPException(status_code=400, detail="No se pudo crear la tarea")
    return nueva_tarea

@tarea_router.put('/{id}', response_model=TareaDTO, status_code=200)
async def update_tarea(id: str, tarea_update: TareaUpdateDTO):
    tarea_actualizada = await update_tarea_service(id, tarea_update)
    if not tarea_actualizada:
        raise HTTPException(status_code=404, detail="Tarea no encontrada o no actualizada")
    return tarea_actualizada

@tarea_router.put('/{id}/estado/', response_model=TareaDTO, status_code=200)
async def actualizar_estado_tarea(
    id: str,
    estado_update: EstadoTareaUpdate, 
    db: Session = Depends(get_db)
):
    try:
        # Buscar la tarea
        tarea = db.query(Tarea).filter(Tarea.id == id).first()
        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada.")

        # Buscar el estado
        estado = db.query(Estado).filter(Estado.id == estado_update.id_estado).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado.")

        # Actualizar el estado de la tarea
        tarea.id_estado = estado.id
        db.commit()
        db.refresh(tarea)
        return tarea
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")


@tarea_router.delete('/{id}', response_model=TareaDTO, status_code=200)
async def delete_tarea(id: str):
    tarea_eliminada = await delete_tarea_service(id)
    if not tarea_eliminada:
        raise HTTPException(status_code=404, detail="Tarea no encontrada o no eliminada")
    return tarea_eliminada
