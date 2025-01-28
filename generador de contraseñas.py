import numpy as np
import random
import string
import math
from sympy import Matrix

matriz_descifrado_global = None

def generar_contraseña(longitud, incluir_especiales, incluir_numeros, incluir_mayusculas):
    caracteres = string.ascii_lowercase
    if incluir_especiales:
        caracteres += string.punctuation
    if incluir_numeros:
        caracteres += string.digits
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def calcular_bits_encriptacion(caracteres_posibles, longitud):
    return math.log2(len(caracteres_posibles)) * longitud

def generar_matriz_invertible(n):
    while True:
        matriz = np.random.randint(0, 256, (n, n))
        sympy_mat = Matrix(matriz)
        det = sympy_mat.det()
        det_mod = det % 256
        if math.gcd(det_mod, 256) == 1:
            try:
                sympy_mat.inv_mod(256)
                return matriz
            except ValueError:
                continue

def cifrar_contraseña(numeros, matriz_cifrado):
    vector = np.array(numeros)
    cifrado = np.dot(matriz_cifrado, vector) % 256
    return list(cifrado.astype(int))

def descifrar_contraseña(numeros_cifrados, matriz_cifrado):
    try:
        n = len(numeros_cifrados)
        if matriz_cifrado.shape[0] != n:
            print("Error: La longitud no coincide con el tamaño de la matriz.")
            return []
        matriz_mod = Matrix(matriz_cifrado)
        matriz_inv = np.array(matriz_mod.inv_mod(256).tolist(), dtype=int)
        vector = np.array(numeros_cifrados)
        descifrado = np.dot(matriz_inv, vector) % 256
        return list(descifrado.astype(int))
    except Exception as e:
        print(f"Error de descifrado: {str(e)}")
        return []

def menu_generar_contraseña():
    print("\n--- Generador de Contraseñas ---")
    longitud = int(input("Ingrese la longitud de la contraseña (12): ") or 12)
    incluir_especiales = input("¿Incluir caracteres especiales? (s/n): ").lower() == 's'
    incluir_numeros = input("¿Incluir números? (s/n): ").lower() == 's'
    incluir_mayusculas = input("¿Incluir letras mayúsculas? (s/n): ").lower() == 's'

    contraseña = generar_contraseña(longitud, incluir_especiales, incluir_numeros, incluir_mayusculas)
    print("\nContraseña generada:", contraseña)
    caracteres_posibles = string.ascii_lowercase + \
                        (string.punctuation if incluir_especiales else "") + \
                        (string.digits if incluir_numeros else "") + \
                        (string.ascii_uppercase if incluir_mayusculas else "")
    print("Nivel de encriptación: {:.2f} bits".format(calcular_bits_encriptacion(caracteres_posibles, longitud)))

def menu_cifrar_descifrar():
    global matriz_descifrado_global
    print("\n--- Cifrado y Descifrado ---")
    opcion = input("1. Cifrar contraseña\n2. Descifrar contraseña\nSeleccione una opción: ")

    if opcion == "1":
        contraseña_input = input("Ingrese la contraseña a cifrar: ")
        numeros = [ord(c) for c in contraseña_input]
        n = len(numeros)
        matriz_cifrado = generar_matriz_invertible(n)
        matriz_descifrado_global = matriz_cifrado
        cifrada = cifrar_contraseña(numeros, matriz_cifrado)
        print(f"Contraseña cifrada: {cifrada}")
        print("Guarde esta matriz para descifrar:\n", matriz_cifrado.tolist())

    elif opcion == "2":
        if matriz_descifrado_global is None:
            print("Primero debe cifrar una contraseña para generar la matriz.")
            return
        cifrada_input = input("Ingrese los números cifrados (separados por espacios): ")
        try:
            numeros_cifrados = list(map(int, cifrada_input.split()))
        except ValueError:
            print("Entrada no válida. Ingrese números separados por espacios.")
            return
        descifrada = descifrar_contraseña(numeros_cifrados, matriz_descifrado_global)
        if descifrada:
            contraseña_descifrada = ''.join([chr(n) for n in descifrada])
            print(f"Contraseña descifrada: {contraseña_descifrada}")
        else:
            print("No se pudo descifrar la contraseña.")

def main():
    while True:
        print("\n--- Menú Principal ---")
        opcion = input("1. Generar contraseña\n2. Cifrar/Descifrar contraseña\n3. Salir\nSeleccione una opción: ")
        if opcion == "1":
            menu_generar_contraseña()
        elif opcion == "2":
            menu_cifrar_descifrar()
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()