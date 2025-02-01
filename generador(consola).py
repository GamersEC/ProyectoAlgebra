import numpy as np
import math

def generar_contrasena(longitud, usar_minusculas, usar_mayusculas, usar_numeros, usar_especiales):
    # Matriz de caracteres usando numpy
    conjuntos = [
        np.array(list("abcdefghijklmnopqrstuvwxyz")),
        np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")),
        np.array(list("0123456789")),
        np.array(list("!@#$%^&*()-_=+[]{};:,.<>/?"))
    ]

    # Vector de activación booleano
    activaciones = np.array([
        usar_minusculas,
        usar_mayusculas,
        usar_numeros,
        usar_especiales
    ], dtype=bool)

    # Filtrar conjuntos usando álgebra booleana
    conjuntos_activos = [conjuntos[i] for i in np.where(activaciones)[0]]

    if not conjuntos_activos:
        raise ValueError("Debe seleccionar al menos un tipo de carácter")

    # Vector de probabilidades (normalización L1)
    probabilidades = np.array([len(c) for c in conjuntos_activos], dtype=np.float64)
    probabilidades /= np.sum(probabilidades)

    # Generar contraseña usando selección vectorizada
    indices = np.random.choice(len(conjuntos_activos), size=longitud, p=probabilidades)
    password = [np.random.choice(conjuntos_activos[i]) for i in indices]

    # Asegurar al menos un carácter de cada conjunto
    for i, conjunto in enumerate(conjuntos_activos):
        if not any(np.isin(password, conjunto)):
            pos = np.random.randint(0, longitud)
            password[pos] = np.random.choice(conjunto)

    return ''.join(password)

def calcular_seguridad(password):
    # Vector de presencia de caracteres
    presencia = np.array([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(not c.isalnum() for c in password)
    ], dtype=int)

    # Vector de espacios posibles
    espacios = np.array([26, 26, 10, 32])

    # Cálculo de entropía usando álgebra lineal
    espacio_total = np.dot(presencia, espacios)
    if espacio_total == 0:
        return 0.0

    entropia = len(password) * math.log2(espacio_total)
    entropia += np.linalg.norm(presencia, ord=1) * 0.75  # Bonus por diversidad

    return entropia

def main():
    print("********************************")
    print("=== Generador de Contraseñas ===")
    print("********************************\n")

    # Obtener parámetros
    longitud = int(input("Ingrese la longitud de la contraseña (8-128): "))
    if not 8 <= longitud <= 128:
        print("Longitud inválida, usando valor por defecto 16")
        longitud = 16

    mayus = input("¿Incluir mayúsculas? (s/n): ").lower() == 's'
    numeros = input("¿Incluir números? (s/n): ").lower() == 's'
    especiales = input("¿Incluir caracteres especiales? (s/n): ").lower() == 's'

    try:
        password = generar_contrasena(
            longitud=longitud,
            usar_minusculas=True,  # Siempre incluir minúsculas
            usar_mayusculas=mayus,
            usar_numeros=numeros,
            usar_especiales=especiales
        )

        seguridad = calcular_seguridad(password)

        print("\nContraseña generada:", password)
        print(f"Seguridad estimada: {seguridad:.2f} bits")

    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()