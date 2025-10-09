from datetime import datetime, timedelta
import re

def validate_aviso_adopcion(form_data, files):
    """
    Valida todos los campos del formulario de adopción en el servidor
    """
    errores = []
    
    # validador lugar entrega
    if not form_data.get('comuna'):
        errores.append("Debe seleccionar una comuna")
    
    sector = form_data.get('sector', '')
    if sector and len(sector) > 100:
        errores.append("El sector no puede tener más de 100 caracteres")
    
    # validador datos de contacto
    nombre = form_data.get('nombreContacto', '')
    if not nombre:
        errores.append("El nombre de contacto es requerido")
    elif len(nombre) < 3 or len(nombre) > 200:
        errores.append("El nombre debe tener entre 3 y 200 caracteres")
    # no deberian haber numeros en el nombre
    elif re.search(r'\d', nombre):
        errores.append("El nombre no puede contener números")
    
    email = form_data.get('email', '')
    if not email:
        errores.append("El email es requerido")
    elif len(email) > 100:
        errores.append("El email no puede tener más de 100 caracteres")
    # formato de email con regex
    elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        errores.append("El formato del email es inválido")
    
    telefono = form_data.get('fono', '')
    if telefono:
        # formato: +NNN.NNNNNNNN
        if not re.match(r'^\+\d{3}\.\d{8}$', telefono):
            errores.append("El teléfono debe tener formato +NNN.NNNNNNNN (ej: +569.12345678)")
    
    # validador metodos de contacto
    metodos_seleccionados = 0
    metodos_contacto = {
        'cb1': 'whatsapp', 
        'cb2': 'telegram', 
        'cb3': 'x', 
        'cb4': 'instagram', 
        'cb5': 'tiktok', 
        'cb6': 'otro'
    }
    
    for checkbox, metodo in metodos_contacto.items():
        if form_data.get(checkbox):
            metodos_seleccionados += 1
            identificador = form_data.get(f'contacto_{metodo}', '')
            if identificador:
                if len(identificador) < 4 or len(identificador) > 50:
                    errores.append(f"El identificador de {metodo} debe tener entre 4 y 50 caracteres")
    
    if metodos_seleccionados == 0:
        errores.append("Debe seleccionar al menos un método de contacto")
    elif metodos_seleccionados > 5:
        errores.append("No puede seleccionar más de 5 métodos de contacto")
    
    # validador informacion del animal
    tipo = form_data.get('tipo', '')
    if not tipo:
        errores.append("Debe seleccionar un tipo de animal")
    elif tipo not in ['gato', 'perro']:
        errores.append("Tipo de animal inválido")
    
    cantidad = form_data.get('cantidad', '')
    if not cantidad:
        errores.append("La cantidad es requerida")
    # solo deben ser numeros
    elif not re.match(r'^\d+$', cantidad):
        errores.append("La cantidad debe ser un número")
    elif int(cantidad) < 1:
        errores.append("La cantidad debe ser al menos 1")
    elif int(cantidad) > 100:
        errores.append("La cantidad no puede ser mayor a 100")
    
    edad = form_data.get('edad', '')
    if not edad:
        errores.append("La edad es requerida")
    # solo pueden ser números
    elif not re.match(r'^\d+$', edad):
        errores.append("La edad debe ser un número")
    elif int(edad) < 1:
        errores.append("La edad debe ser al menos 1")
    elif int(edad) > 50:
        errores.append("La edad no puede ser mayor a 50")
    
    ume = form_data.get('ume', '')
    if not ume:
        errores.append("Debe seleccionar una unidad de medida de edad")
    elif ume not in ['meses', 'años']:
        errores.append("Unidad de medida de edad inválida")
    
    fecha_entrega = form_data.get('fecha_disponible', '')
    if not fecha_entrega:
        errores.append("La fecha de entrega es requerida")
    else:
        try:
            fecha_entrega_dt = datetime.fromisoformat(fecha_entrega)
            fecha_actual = datetime.now()
            fecha_minima = fecha_actual + timedelta(hours=3)
            
            if fecha_entrega_dt < fecha_minima:
                errores.append("La fecha de entrega debe ser al menos 3 horas después de la hora actual")
        except ValueError:
            errores.append("Formato de fecha inválido")

    descripcion = form_data.get('descripcion', '')
    if descripcion and len(descripcion) > 500:
        errores.append("La descripción no puede tener más de 500 caracteres")
    
    # validador fotos
    fotos = [f for f in files if f and f.filename]
    if len(fotos) == 0:
        errores.append("Debe subir al menos una foto")
    elif len(fotos) > 5:
        errores.append("No puede subir más de 5 fotos")
    else:
        for foto in fotos:
            if foto.filename:
                # validar extensión del archivo con regex
                if not re.match(r'^.*\.(png|jpg|jpeg|gif)$', foto.filename.lower()):
                    errores.append(f"El archivo {foto.filename} no es una imagen válida (PNG, JPG, JPEG, GIF)")
    
    return errores