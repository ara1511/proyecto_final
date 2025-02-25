from tareas.entity import Tarea
from tareas.dto import TareaCreateDTO, TareaUpdateDTO, DeleteTareaDTO
from config.cnx import sessionlocal 

async def get_tareas():
    try:
        db = sessionlocal()
        tareas = db.query(Tarea).all()
        return tareas
    except Exception as e:
        return f'Ocurrió un error: {e}'
    finally:
        db.close()

async def get_tarea_by_id(id: str):
    try:
        db = sessionlocal()
        tarea = db.query(Tarea).filter(Tarea.id == id).first()
        return tarea
    except Exception as e:
        return f'Ocurrió un error: {e}'
    finally:
        db.close()

async def create_tarea_service(tarea: TareaCreateDTO):
    try:
        db = sessionlocal()
        nueva_tarea = Tarea(
            usuario_id=tarea.usuario_id,
            tarea=tarea.tarea,
            fecha=tarea.fecha,
            id_estado=tarea.id_estado
        )
        db.add(nueva_tarea)
        db.commit()
        db.refresh(nueva_tarea)
        return nueva_tarea
    except Exception as e:
        db.rollback()
        return f'Ocurrió un error: {e}'
    finally:
        db.close()

async def update_tarea_service(id: str, tarea_update: TareaUpdateDTO):
    try:
        db = sessionlocal()
        tarea = db.query(Tarea).filter(Tarea.id == id).first()
        if tarea:
            tarea.usuario_id = tarea_update.usuario_id
            tarea.tarea = tarea_update.tarea
            tarea.fecha = tarea_update.fecha            
            tarea.id_estado = tarea_update.id_estado
            db.commit()
            db.refresh(tarea)
            return tarea
        return None
    except Exception as e:
        db.rollback()
        return f'Ocurrió un error: {e}'
    finally:
        db.close()

async def delete_tarea_service(id: str):
    try:
        db = sessionlocal()
        tarea = db.query(Tarea).filter(Tarea.id == id).first()
        if tarea:
            db.delete(tarea)
            db.commit()
            return tarea
        return None
    except Exception as e:
        db.rollback()
        return f'Ocurrió un error: {e}'
    finally:
        db.close()
