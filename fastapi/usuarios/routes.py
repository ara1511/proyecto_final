from fastapi import APIRouter, HTTPException
from usuarios.dto import UsuarioDTO, UsuarioCreateDTO, UsuarioUpdateDTO
from usuarios.service import *

usuario_router = APIRouter()

@usuario_router.get('/', response_model=list[UsuarioDTO], status_code=200)
async def get_all_usuarios():
    usuarios = await get_usuarios()
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    return usuarios

@usuario_router.get('/{id}', response_model=UsuarioDTO, status_code=200)
async def get_usuario(id: str):
    usuario = await get_usuario_by_id(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@usuario_router.post('/', response_model=UsuarioDTO, status_code=201)
async def create_usuario(usuario: UsuarioCreateDTO):
    nuevo_usuario = await create_usuario_service(usuario)
    if not nuevo_usuario:
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
    return nuevo_usuario

@usuario_router.put('/{id}', response_model=UsuarioDTO, status_code=200)
async def update_usuario(id: str, usuario_update: UsuarioUpdateDTO):
    usuario_actualizado = await update_usuario_service(id, usuario_update)
    if not usuario_actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no actualizado")
    return usuario_actualizado

@usuario_router.delete('/{id}', response_model=UsuarioDTO, status_code=200)
async def delete_usuario(id: str):
    usuario_eliminado = await delete_usuario_service(id)
    if not usuario_eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no eliminado")
    return usuario_eliminado
