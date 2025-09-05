// --- VALIDADORES ---

// INFORMACION LUGAR DE ENTREGA //

// validador región
const validadorRegion = () => {
    const selectRegion = document.getElementById("selectRegion");
    const valorSeleccionado = selectRegion.value;
    
    if (valorSeleccionado === "" || valorSeleccionado == "--Selecciona una región--") {
        // No se ha seleccionado nada
        selectRegion.style.borderColor = "red";
        return false;
    } else {
        // Hay una región seleccionada
        selectRegion.style.borderColor = "";
        return true;
    }
}

// validador comuna
const validadorComuna = () => {
    const selectComuna = document.getElementById("selectComuna");
    const valorSeleccionado = selectComuna.value;
    
    if (valorSeleccionado === "" || valorSeleccionado == "--Selecciona una comuna--") {
        // No se ha seleccionado nada
        selectComuna.style.borderColor = "red";
        return false;
    } else {
        // Hay una comuna seleccionada
        selectComuna.style.borderColor = "";
        return true;
    }
}

// INFORMACION CONTACTO //

// validador email
const validadorMail = (mail) => {
    return (mail && mail.includes("@") && mail.length < 101);
};

// validador nombre contacto
const validadorNombre = (input) => {
    let valido = false; // definicion de variables
    let tieneNumeros = /\d/.test(input); // true si tiene numeros, false si no
    if (input && input.length > 3 && input.length < 201 && !tieneNumeros) {
      valido = true;
    }
    return valido;
};

//validador telefono de contacto
const validadorFono = (input) => {
    let regex = /^\+\d{3}\.\d{8}$/; // definicion de variables
    
    return regex.test(input);
};

const validadorMetodoContacto = () => {
    // obtener todos los checkboxes por ID
    const cb1 = document.getElementById('cb1');
    const cb2 = document.getElementById('cb2');
    const cb3 = document.getElementById('cb3');
    const cb4 = document.getElementById('cb4');
    const cb5 = document.getElementById('cb5');
    const cb6 = document.getElementById('cb6');
  
    // contar cuántos están seleccionados
    const seleccionados = [cb1, cb2, cb3, cb4, cb5, cb6].filter(cb => cb.checked).length;
  
    // validar que como máximo haya 5
    return (seleccionados <= 5);
};

//validador input metodo de contacto
const validadorInputsContacto = () => {
    let valido = true;

    for (let i = 1; i <= 6; i++) {
        const checkbox = document.getElementById(`cb${i}`);
        const inputDiv = document.getElementById(`inputCB${i}`);
        const input = inputDiv?.querySelector('input');

        if (checkbox.checked && input.type == 'text') {
            const valor = input?.value.trim();
            if (!valor || valor.length < 4 || valor.length > 50) {
                valido = false;
                input.style.borderColor = "red";
            } else {
                input.style.borderColor = "";
            }
        }
    }

    return valido;
};
  
// INFORMACION DEL ANIMAL //

// validador tipo
const validadorTipo = () => {
    const selectTipo = document.getElementById('tipo');
    const valorSeleccionado = selectTipo.value;
    
    // validar que se haya seleccionado una opción válida (no el placeholder)
    return (valorSeleccionado === 'gato' || valorSeleccionado === 'perro');
};


// validador UME
const validadorUME = () => {
    const selectUME = document.getElementById('ume');
    const valorSeleccionado = selectUME.value;
    
    // Validar que se haya seleccionado meses o años
    return (valorSeleccionado === 'meses' || valorSeleccionado === 'años');
};

// validador cantidad y edad + función auxiliar
function esEntero(input) {
    // Si ya es un número, verificar directamente
    if (typeof input == 'number') {
        return Number.isInteger(input);
    }
    
    // Si es string, intentar convertir
    if (typeof input == 'string') {
        // Verificar que el string solo contenga dígitos
        if (!/^-?\d+$/.test(input)) return false;
        
        // Convertir a número y verificar
        const numero = Number(input);
        return Number.isInteger(numero);
    }
    
    // Para cualquier otro tipo, devolver false
    return false;
}
const validadorCantidadEdad = (input) => {
    let valido = false;
    if (input && esEntero(input) && input.length >= 1){
        valido = input >= 1;
    }
    return valido;
}

// validador fecha entrega
const validadorFechaEntrega = (input) => {
    // verificamos que sea válido
    if (!(input instanceof Date) || isNaN(input.getTime())) {
        return false;
    }

    let fechaActual = new Date(); // fecha actual del sistema
    let fechaMinima = new Date(fechaActual);
    fechaMinima.setHours(fechaActual.getHours() + 3);
  
    // validamos que la fecha escogida cumpla con ser en 3 horas más
    return input >= fechaMinima;
}

// validador foto
const validadorFotos = () => {
    const inputs = document.querySelectorAll('#contenedorFotos input[type="file"]');
    let cantidadFotos = 0;

    inputs.forEach(input => {
        if (input.files.length > 0) {
            cantidadFotos++;
        }
    });

    // mínimo 1 foto, máximo 5
    return (cantidadFotos >= 1 && cantidadFotos <= 5);
};

// UNIENDO TODO //

const validarForm = () => {
    console.log("Enviando..."); // imprimir en consola
  
    // obtener elementos del DOM por el ID
    let emailInput = document.getElementById("email");
    let nombreInput = document.getElementById("nombreContacto");
    let fonoInput = document.getElementById("fono");
    
    let cantidadInput = document.getElementById("cantidad");
    let edadInput = document.getElementById("edad");
    let fechaDisponibleInput = document.getElementById("fecha_disponible");

    let msg = "";

    if (!validadorRegion()) {
        msg += "Debe seleccionar una región\n";
    }

    if (!validadorComuna()) {
        msg += "Debe seleccionar una comuna\n";
    }
  
    if (!validadorMail(emailInput.value)) {
      msg += "Ingrese un email válido\n";
      emailInput.style.borderColor = "red"; // cambiar estilo con JS!!
    } else {
      emailInput.style.borderColor = "";
    }
  
    if (!validadorNombre(nombreInput.value)) {
      msg += "Nombre inválido\n";
      nombreInput.style.borderColor = "red";
    } else {
      nombreInput.style.borderColor = "";
    }
  
    if (!validadorFono(fonoInput.value)) {
      msg += "Teléfono inválido, el formato debe cumplir +NNN.NNNNNNNN\n";
      fonoInput.style.borderColor = "red";
    } else {
      fonoInput.style.borderColor = "";
    }

    if (!validadorMetodoContacto()) {
        msg += "Debe tener a lo más 5 método de contacto\n";
    }

    if (!validadorInputsContacto()) {
        msg += "Los campos de contacto (ID o URL) deben tener entre 4 y 50 caracteres.\n";
    }
    
    if (!validadorTipo()) {
        msg += "Debe elegir un tipo de animal\n";
    }

    if (!validadorUME()) {
        msg += "Debe elegir una unidad de medida de edad\n";
    }
    
    if (!validadorCantidadEdad(cantidadInput.value)) {
        msg += "Cantidad inválida\n";
        cantidadInput.style.borderColor = "red";
    } else {
        cantidadInput.style.borderColor = "";
    }

    if (!validadorCantidadEdad(edadInput.value)) {
        msg += "Edad inválida\n";
        edadInput.style.borderColor = "red";
    } else {
        edadInput.style.borderColor = "";
    }

    if (!validadorFechaEntrega(new Date(fechaDisponibleInput.value))) {
      msg += "Fecha no válida. Asegúrese de que si es el mismo día de hoy, debe ser en al menos 3 horas más la entrega\n";
      fechaDisponibleInput.style.borderColor = "red";
    } else {
        fechaDisponibleInput.style.borderColor = "";
    }

    if (!validadorFotos()) {
        msg += "Debes subir al menos una foto y no más de 5.\n";
    }
  
    if (msg != "") {
        alert(msg);
        return;
    } else {
        aparece("contenedorConfirmacion");
    }
    
  };