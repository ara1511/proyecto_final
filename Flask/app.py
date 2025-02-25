from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json
from datetime import datetime
import uuid  # Añadido para validar UUIDs

app = Flask(__name__)
app.secret_key = "clave_secreta_para_sesiones"

# URL base de la API
API_URL = "http://localhost:8000"

# Función auxiliar para validar UUIDs
def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except (ValueError, AttributeError, TypeError):
        return False

@app.route('/')
def home():
    return redirect(url_for('listar_tareas'))

# Rutas para Usuarios
@app.route('/usuarios')
def listar_usuarios():
    response = requests.get(f"{API_URL}/usuarios/")
    usuarios = response.json()
    return render_template('usuarios/index.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        nuevo_usuario = {
            "nombre": request.form.get('nombre'),
            "edad": int(request.form.get('edad')),
            "email": request.form.get('correo') 
        }
        response = requests.post(
            f"{API_URL}/usuarios/", 
            json=nuevo_usuario
        )
        
        if response.status_code == 201:
            flash('Usuario creado exitosamente.', 'success')
            return redirect(url_for('listar_usuarios'))
        else:
            flash(f'Error al crear usuario: {response.json().get("detail", "Error desconocido")}', 'danger')
    
    return render_template('usuarios/crear.html')

@app.route('/usuarios/editar/<uuid:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    # Convertir UUID a string para la API
    id_str = str(id)
    
    if request.method == 'POST':
        usuario_actualizado = {
            "nombre": request.form.get('nombre'),
            "edad": int(request.form.get('edad')),
            "email": request.form.get('correo')
        }
        
        response = requests.put(
            f"{API_URL}/usuarios/{id_str}", 
            json=usuario_actualizado
        )
        
        if response.status_code == 200:
            flash('Usuario actualizado exitosamente.', 'success')
            return redirect(url_for('listar_usuarios'))
        else:
            flash(f'Error al actualizar usuario: {response.json().get("detail", "Error desconocido")}', 'danger')
    
    # Obtener datos del usuario a editar
    response = requests.get(f"{API_URL}/usuarios/{id_str}")
    if response.status_code == 404:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('listar_usuarios'))
        
    usuario = response.json()
    
    return render_template('usuarios/editar.html', usuario=usuario)

@app.route('/usuarios/eliminar/<uuid:id>')
def eliminar_usuario(id):
    id_str = str(id)
    response = requests.delete(f"{API_URL}/usuarios/{id_str}")
    
    if response.status_code == 200:
        flash('Usuario eliminado exitosamente.', 'success')
    else:
        flash(f'Error al eliminar usuario: {response.json().get("detail", "Error desconocido")}', 'danger')
    
    return redirect(url_for('listar_usuarios'))

# Rutas para Tareas
@app.route('/tareas')
def listar_tareas():
    usuario_id = request.args.get('usuario_id')
    
    if usuario_id and is_valid_uuid(usuario_id):
        response = requests.get(f"{API_URL}/tareas/?usuario_id={usuario_id}")
    else:
        response = requests.get(f"{API_URL}/tareas/")
    
    tareas_data = response.json()
    
    # Filtrar solo los elementos que son diccionarios
    tareas = []
    for item in tareas_data:
        if isinstance(item, dict):
            tareas.append(item)
        elif isinstance(item, str):
            try:
                # Intentar convertir una posible cadena JSON a diccionario
                tarea_dict = json.loads(item)
                if isinstance(tarea_dict, dict):
                    tareas.append(tarea_dict)
            except json.JSONDecodeError:
                # Si no es un JSON válido, crear un objeto básico
                tareas.append({"tarea": item, "id_estado": None})
    
    # Obtener la lista de usuarios para el filtro
    usuarios_response = requests.get(f"{API_URL}/usuarios/")
    usuarios = usuarios_response.json()
    
    # Obtener estados para mapear IDs a nombres de estados
    estados_response = requests.get(f"{API_URL}/estados/")
    estados = {estado['id']: estado['estado'] for estado in estados_response.json()}
    
    # Preparar datos para la plantilla
    for tarea in tareas:
        # Asegurar que cada tarea tenga un estado formateado para la plantilla
        estado_id = tarea.get('id_estado')
        if estado_id and estado_id in estados:
            tarea['estado_nombre'] = estados[estado_id]
        else:
            tarea['estado_nombre'] = "Desconocido"
    
    return render_template('tareas/index.html', tareas=tareas, usuarios=usuarios, usuario_seleccionado=usuario_id)

@app.route('/tareas/crear', methods=['GET', 'POST'])
def crear_tarea():
    if request.method == 'POST':
        # Formato de fecha para la API
        fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d').strftime('%Y-%m-%d')
        usuario_id = request.form.get('usuario_id')
        estado_id = request.form.get('id_estado')
        
        # Validar que el usuario_id es un UUID válido
        if not is_valid_uuid(usuario_id):
            flash('ID de usuario no válido.', 'danger')
            return redirect(url_for('crear_tarea'))
        
        nueva_tarea = {
            "tarea": request.form.get('tarea'),
            "fecha": fecha,
            "usuario_id": usuario_id,  # No convertir a int si es UUID
            "id_estado": int(estado_id)  # Mantener como entero
        }
        
        response = requests.post(
            f"{API_URL}/tareas/", 
            json=nueva_tarea
        )
        
        if response.status_code == 201:
            flash('Tarea creada exitosamente.', 'success')
            return redirect(url_for('listar_tareas'))
        else:
            flash(f'Error al crear tarea: {response.json().get("detail", "Error desconocido")}', 'danger')
    
    # Obtener usuarios y estados para el formulario
    usuarios_response = requests.get(f"{API_URL}/usuarios/")
    usuarios = usuarios_response.json()
    
    estados_response = requests.get(f"{API_URL}/estados/")
    estados = estados_response.json()
    
    # Enviar la fecha actual para el formulario
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('tareas/crear.html', usuarios=usuarios, estados=estados, today_date=today_date)

@app.route('/tareas/editar/<uuid:id>', methods=['GET', 'POST'])
def editar_tarea(id):
    id_str = str(id)
    
    if request.method == 'POST':
        # Formato de fecha para la API
        fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d').strftime('%Y-%m-%d')
        usuario_id = request.form.get('usuario_id')
        estado_id = request.form.get('id_estado')
        
        # Validar que el usuario_id es un UUID válido
        if not is_valid_uuid(usuario_id):
            flash('ID de usuario no válido.', 'danger')
            return redirect(url_for('editar_tarea', id=id))
        
        tarea_actualizada = {
            "tarea": request.form.get('tarea'),
            "fecha": fecha,
            "usuario_id": usuario_id,  # No convertir a int si es UUID
            "id_estado": int(estado_id)  # Mantener como entero
        }
        
        response = requests.put(
            f"{API_URL}/tareas/{id_str}", 
            json=tarea_actualizada
        )
        
        if response.status_code == 200:
            flash('Tarea actualizada exitosamente.', 'success')
            return redirect(url_for('listar_tareas'))
        else:
            flash(f'Error al actualizar tarea: {response.json().get("detail", "Error desconocido")}', 'danger')
    
    # Obtener datos de la tarea a editar
    response = requests.get(f"{API_URL}/tareas/{id_str}")
    if response.status_code == 404:
        flash('Tarea no encontrada.', 'danger')
        return redirect(url_for('listar_tareas'))
        
    tarea = response.json()
    
    # Obtener usuarios y estados para el formulario
    usuarios_response = requests.get(f"{API_URL}/usuarios/")
    usuarios = usuarios_response.json()
    
    estados_response = requests.get(f"{API_URL}/estados/")
    estados = estados_response.json()
    
    return render_template(
        'tareas/editar.html', 
        tarea=tarea, 
        usuarios=usuarios, 
        estados=estados
    )

@app.route('/tareas/<uuid:id>/estado/<int:estado_id>', methods=['GET'])
def actualizar_estado_tarea(id, estado_id):
    id_str = str(id)
    estado_update = {
        "id_estado": estado_id
    }
    
    response = requests.put(
        f"{API_URL}/tareas/{id_str}/estado/",
        json=estado_update
    )
    
    if response.status_code == 200:
        flash('Estado de tarea actualizado exitosamente.', 'success')
    else:
        flash(f'Error al actualizar estado: {response.json().get("detail", "Error desconocido")}', 'danger')
    
    return redirect(url_for('listar_tareas'))

@app.route('/tareas/eliminar/<uuid:id>')
def eliminar_tarea(id):
    id_str = str(id)
    response = requests.delete(f"{API_URL}/tareas/{id_str}")
    
    if response.status_code == 200:
        flash('Tarea eliminada exitosamente.', 'success')
    else:
        flash(f'Error al eliminar tarea: {response.json().get("detail", "Error desconocido")}', 'danger')
    
    return redirect(url_for('listar_tareas'))

if __name__ == "__main__":
    app.run(debug=True)