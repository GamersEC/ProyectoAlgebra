import secrets
import numpy as np

def generar_matriz_invertible(modulo):
    """Genera una matriz 2x2 invertible módulo 'modulo' usando secrets"""
    intentos = 0
    while True:
        a = secrets.randbelow(modulo)
        b = secrets.randbelow(modulo)
        c = secrets.randbelow(modulo)
        d = secrets.randbelow(modulo)

        # Calcular determinante
        det = (a * d - b * c) % modulo

        if np.gcd(det, modulo) == 1:
            return np.array([[a, b], [c, d]])

        # Intentos limitados para evitar ciclos infinitos
        intentos += 1
        if intentos > 100:
            raise Exception("No se pudo generar una matriz invertible después de 100 intentos.")

def aplicar_transformacion(vector, modulo):
    """Aplica transformación lineal usando matrices invertibles"""
    if len(vector) % 2 != 0:
        vector.append(secrets.randbelow(modulo))  # Padding seguro

    matriz = np.array(vector).reshape(2, -1)
    M = generar_matriz_invertible(modulo)

    # Transformación lineal
    transformada = (M @ matriz) % modulo

    return transformada.ravel()

def generar_contrasena(longitud):
    """Genera una contraseña utilizando transformación lineal"""
    caracteres = list("abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#$%^&*()-_=+[]{};:,.<>/?")

    contrasena = [secrets.choice(caracteres) for _ in range(longitud)]
    valores = [caracteres.index(c) for c in contrasena]

    valores_transformados = aplicar_transformacion(valores, 76)
    contrasena_final = [caracteres[v % 76] for v in valores_transformados[:longitud]]

    return ''.join(contrasena_final)

def calcular_seguridad(longitud):
    """Calcula la entropía de la contraseña en bits"""
    return longitud * np.log2(76)

try:
    longitud = int(input("Ingrese la longitud de la contraseña (máximo 128): "))
    if longitud <= 0:
        print("La longitud debe ser positiva.")
    elif longitud > 128:
        print("Error: Longitud máxima es 128.")
    else:
        print("Contraseña generada:", generar_contrasena(longitud))
        print(f"Nivel criptográfico: {calcular_seguridad(longitud):.2f} bits")
except ValueError:
    print("Error: Ingrese un número válido.")