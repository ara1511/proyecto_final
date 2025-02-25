from usuarios.entity import Usuario
from usuarios.dto import UsuarioCreateDTO, UsuarioUpdateDTO, DeleteUsuarioDTO
from config.cnx import sessionlocal

async def get_usuarios():
    try:
        db = sessionlocal()
        usuarios = db.query(Usuario).all()
        return usuarios
    except Exception as e:
        return f'Ocurrió un error: {e}'
    finally:
        db.close()

async def get_usuario_by_id(id: str):
    try:
        db = sessionlocal()
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        return usuario
    except Exception as e:
        return f'Ocurrió un error: {e}'
    finally:
        db.close()

async def create_usuario_service(usuario: UsuarioCreateDTO):
    try:
        db = sessionlocal()
        nuevo_usuario = Usuario(
            nombre=usuario.nombre,
            edad=usuario.edad,
            correo=usuario.correo
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    except Exception as e:
        db.rollback()
        return f'Ocurrió un error: {e}'
    finally:
        db.close()

async def update_usuario_service(id: str, usuario_update: UsuarioUpdateDTO):
    try:
        db = sessionlocal()
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if usuario:
            usuario.nombre = usuario_update.nombre
            usuario.edad = usuario_update.edad
            usuario.correo = usuario_update.correo
            
            db.commit()
            db.refresh(usuario)
            return usuario
        return None
    except Exception as e:
        db.rollback()
        return f'Ocurrió un error: {e}'
    finally:
        db.close()

async def delete_usuario_service(id: str):
    try:
        db = sessionlocal()
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if usuario:
            db.delete(usuario)
            db.commit()
            return usuario
        return None
    except Exception as e:
        db.rollback()
        return f'Ocurrió un error: {e}'
    finally:
        db.close()
