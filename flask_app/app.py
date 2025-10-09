from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
from datetime import datetime
from database import db

# directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

app = Flask(__name__)
app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- rutas ---

@app.route('/')
def portada():
    avisos = db.get_avisos_recientes(5)
    # obtener fotos para cada aviso
    avisos_con_fotos = []
    for aviso in avisos:
        fotos = db.get_fotos_by_aviso_id(aviso.id)
        # usamos la primera foto como principal
        aviso.foto_principal = fotos[0] if fotos else None
        avisos_con_fotos.append(aviso)
    
    return render_template('portada.html', avisos=avisos_con_fotos)

@app.route('/formulario.html', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        from validations import validate_aviso_adopcion
        
        fotos = request.files.getlist('fotoMascota')
        errores = validate_aviso_adopcion(request.form, fotos)
        
        if errores:
            regiones = db.get_regiones()
            return render_template('formulario.html', regiones=regiones, errores=errores)
        
        # guardamos fotos
        nombres_fotos = []
        for foto in fotos:
            if foto and foto.filename:
                nombre_foto = generar_nombre_unico(foto)
                if nombre_foto:
                    foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_foto))
                    nombres_fotos.append(nombre_foto)
        
        session['form_data'] = request.form.to_dict()
        session['nombres_fotos'] = nombres_fotos
        
        return redirect(url_for('confirmacion'))
    
    regiones = db.get_regiones()
    return render_template('formulario.html', regiones=regiones)

@app.route('/api/comunas/<int:region_id>')
def api_comunas(region_id):
    comunas = db.get_comunas_by_region(region_id)
    return jsonify([{'id': c.id, 'nombre': c.nombre} for c in comunas])

@app.route('/confirmacion.html', methods=['GET', 'POST'])
def confirmacion():
    if request.method == 'POST':
        return redirect(url_for('confirmacion2'))
    
    if not session.get('form_data'):
        return redirect(url_for('formulario'))
    
    return render_template('confirmacion.html')

@app.route('/confirmacion2.html', methods=['GET', 'POST'])
def confirmacion2():
    if request.method == 'POST':
        form_data = session.get('form_data')
        nombres_fotos = session.get('nombres_fotos', [])
        
        if not form_data:
            return redirect(url_for('formulario'))
        
        # crear aviso en la base de datos
        aviso_id = db.create_aviso_adopcion(
            fecha_ingreso=datetime.now(),
            comuna_id=form_data['comuna'],
            sector=form_data.get('sector', ''),
            nombre=form_data['nombreContacto'],
            email=form_data['email'],
            celular=form_data.get('fono', ''),
            tipo=form_data['tipo'],
            cantidad=int(form_data['cantidad']),
            edad=int(form_data['edad']),
            unidad_medida='a' if form_data['ume'] == 'años' else 'm',
            fecha_entrega=datetime.fromisoformat(form_data['fecha_disponible']),
            descripcion=form_data.get('descripcion', '')
        )
        
        
        metodos_contacto = {
            'cb1': 'whatsapp', 'cb2': 'telegram', 'cb3': 'x',
            'cb4': 'instagram', 'cb5': 'tiktok', 'cb6': 'otro'
        }
        
        for checkbox, metodo in metodos_contacto.items():
            if form_data.get(checkbox):
                identificador = form_data.get(f'contacto_{metodo}', '')
                if identificador:
                    db.create_contacto_por(metodo, identificador, aviso_id)
        
        # guardar fotos en la base de datos
        for nombre_foto in nombres_fotos:
            db.create_foto(f"uploads/{nombre_foto}", nombre_foto, aviso_id)
        
        
        session.pop('form_data', None)
        session.pop('nombres_fotos', None)
        
        return render_template('confirmacion2.html')
    
    return redirect(url_for('formulario'))

@app.route('/listado.html')
def listado():
    pagina = request.args.get('pagina', 1, type=int)
    offset = (pagina - 1) * 5
    
    avisos = db.get_avisos_paginados(offset, 5)
    # obtenemos las fotos para cada aviso
    avisos_con_fotos = []
    for aviso in avisos:
        fotos = db.get_fotos_by_aviso_id(aviso.id)
        # ponemos la primera foto como foto_principal 
        aviso.foto_principal = fotos[0] if fotos else None
        avisos_con_fotos.append(aviso)
    
    total_avisos = db.get_total_avisos()
    total_paginas = (total_avisos + 4) // 5
    
    return render_template('listado.html', avisos=avisos_con_fotos, pagina=pagina, total_paginas=total_paginas)

@app.route('/aviso/<int:aviso_id>')
def aviso_detalle(aviso_id):
    aviso = db.get_aviso_by_id(aviso_id)
    if not aviso:
        return redirect(url_for('listado'))
    
    contactos = db.get_contactos_by_aviso_id(aviso_id)
    fotos = db.get_fotos_by_aviso_id(aviso_id)
    
    return render_template('aviso_detalle.html', aviso=aviso, contactos=contactos, fotos=fotos)

@app.route('/estadisticas.html')
def estadisticas():
    return render_template('estadisticas.html')

@app.route('/foto/<int:foto_id>')
def ver_foto(foto_id):
    foto = db.get_foto_by_id(foto_id)
    
    aviso = db.get_aviso_by_id(foto.aviso_id)
    return render_template('ver_foto.html', foto=foto, aviso=aviso)

# funcion para el nombre de las fotos
def generar_nombre_unico(archivo):
    # genera nombre unico usando hash
    if hasattr(archivo, 'filename') and archivo.filename:
        nombre_original = secure_filename(archivo.filename)
        
        archivo.seek(0)
        file_type = filetype.guess(archivo.read())
        archivo.seek(0)
        
        _extension = file_type.extension if file_type else 'jpg'
        _filename = hashlib.sha256(nombre_original.encode("utf-8")).hexdigest()
        
        return f"{_filename}.{_extension}"
    return None

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)