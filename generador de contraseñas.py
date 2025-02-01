import numpy as np

def generar_contrasena(longitud):
    caracteres = np.array(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:,.<>/?"))

    # Convertir caracteres a valores numéricos usando su código ASCII
    valores_numericos = np.vectorize(ord)(caracteres)

    # Crear un vector aleatorio de índices
    indices = np.random.randint(0, len(caracteres), longitud)

    # Seleccionar caracteres usando los índices aleatorios
    contrasena_vector = valores_numericos[indices]

    # Transformación lineal (ejemplo: suma de un escalar y módulo para mantener rango válido)
    contrasena_transformada = (contrasena_vector + 3) % 126  # Evita caracteres no imprimibles

    # Convertir de nuevo a caracteres
    contrasena = "".join(np.vectorize(chr)(contrasena_transformada))

    return contrasena

def calcular_seguridad(longitud):
    caracteres_unicos = 94  # Considerando 94 caracteres imprimibles ASCII
    entropia = longitud * np.log2(caracteres_unicos)
    return entropia

# Solicitar al usuario la longitud de la contraseña
try:
    longitud_contrasena = int(input("Ingrese la longitud de la contraseña (máximo 128): "))
    if longitud_contrasena <= 0:
        print("La longitud debe ser un número positivo.")
    elif longitud_contrasena > 128:
        print("Error: La longitud máxima permitida es 128.")
    else:
        contrasena = generar_contrasena(longitud_contrasena)
        seguridad = calcular_seguridad(longitud_contrasena)
        print("Contraseña generada:", contrasena)
        print(f"Nivel criptográfico estimado: {seguridad:.2f} bits")
except ValueError:
    print("Error: Ingrese un número válido.")
