#Laboratorio 2 Parte Calificada Nota 20
#Natalia Escudero 20223377

import os
import csv
import time
from typing import Union
from random import randint

inicio = time.perf_counter()

# Nombre del archivo
archivo_palabras = "palabras.txt"
archivo_stats = "stats.csv"

# Verificar si el archivo de nombres existe
if not os.path.exists(archivo_palabras):
    print("Archivo palabras.txt no encontrado")
else:
    with open(archivo_palabras, "r", encoding="utf-8") as f:
        palabras = f.read().splitlines() #obtenemos el contenido como una lista

# Seleccionar una palabra al azar
    palabra = " "
    while " " in palabra: #seguirá buscando palabras hasta que encuentre una que no sea un espacio
        num_palabra = randint(0, len(palabras) - 1)
        palabra = palabras[num_palabra]
    palabras [num_palabra] = " " #se reemplaza la palabra escogida por un espacio

#Cambiar la palabra por un espacio
    lista_actualizada = f"{'\n'.join(palabras)}" #se crea una string de cada palabra separada con enters como la original

    with open(archivo_palabras, "w", encoding="utf-8") as f:
        f.write(lista_actualizada) #se reescribe el archivo con la lista actualizada


#Juego principal:

palabra_lista = ["_"] * len(palabra)
intentos_originales = 10
intentos = intentos_originales
cant_letras = 0
letras_usadas = list()
game = 1
win = "Sí"

def actualiza_score(p_lista: list[str], intentos: int) -> str:
    score = f"{' '.join(p_lista)} - Intentos: {intentos}"
    return score


def lee_letra() -> Union[str, bool, int]:
    letra = ""
    validacion = 0

    while validacion != 1:
        letra = input("Por favor ingrese una letra o la palabra: ")
        if len(letra) == 1: #cuando se ingresa una letra como normal
            game = 1
            return letra, game
        elif letra == palabra: #se gana el juego
                print(actualiza_score(palabra, intentos))
                print(f"Felicitaciones, la palabra encontrada fue {palabra} =)")
                game = 0
                return letra, game
        elif letra != palabra: #se pierde el juego
                print(f"Lo siento perdio el juego =(")
                game = 2
                return letra, game


def busca_letra(p: str, l: str, p_lista: list[str]) -> Union[list[str], bool]: 
    """
    Busca la letra especificada dentro de la palabra para poder reemplazar el '_' en la posicion que la letra ocuparia. 
    Si hay mas de una occurrencia de la letra, se reemplaza en todas las occurrencias.
    :param p: string que contiene la palabra a analizar.
    :param l: string que contiene la letra que se buscara dentro de la palabra.
    :param p_lista: lista de strings que inicialmente tienen '_' y que seran reemplazadas con las letras en donde occuran.
    :return: p_lista actualizada con los valores y una bandera booleana indicando si hubo una ocurrencia o no.
    """
    letra_encontrada = 0

    for idx in range(len(p)):
        if l == p_lista[idx]:
            letra_encontrada = 2 #la letra ya se habia encontrado antes
            break
        elif l == p[idx]:
            p_lista[idx] = l
            letra_encontrada = 1

    return p_lista, letra_encontrada


if __name__ == '__main__': 
    while game == 1:
        print(actualiza_score(palabra_lista, intentos))
        letra_input, game = lee_letra()
        letras_usadas.append(letra_input) #va agregando las letras que se usaron en el juego
        cant_letras += 1 #se ha agregado una nueva letra
        palabra_lista, encontrada = busca_letra(palabra, letra_input, palabra_lista)
        if game == 0: #se ingreso la palabra correcta
            win = "Sí"
            break
        if game == 2: #se ingreso la palabra equivocada
            win = "No"
            break
        if encontrada == 0:
            print("Letra ingresada no es parte de la palabra =(")
            intentos -= 1
        elif encontrada == 2:
            print("¡La letra ya fue elegida anteriormente!")
        
        if intentos == 0:
            print(f"Lo siento perdio el juego =(")
            win = "No"
            game = 0

        if not "_" in palabra_lista:
            print(f"Felicitaciones, la palabra encontrada fue {palabra} =)")
            win = "Sí"
            game = 0

    #Verificando el tiempo de ejecución del script
    fin = time.perf_counter()
    duracion = fin - inicio


    #Uniendo letras usadas
    letras_usadas_str = f"{''.join(letras_usadas)}"

    #Intentos
    intentos_fallidos = intentos_originales - intentos

    # Crear el archivo CSV si no existe
    if not os.path.exists(archivo_stats):
        with open(archivo_stats, "w", encoding="utf-8") as f:   
            writer = csv.writer(f)
            writer.writerow(["Palabra", "Ganó?", "Duración", "Intentos totales", "Intentos fallidos", "Letras"])

    # Leer el archivo CSV y actualizar datos 
    filas = []
    with open(archivo_stats, "r", encoding="utf-8") as f:
        reader = csv.reader(f) #guardar contenido del csv en el iterador reader
        filas = list(reader)

    filas.append([palabra, win, duracion, cant_letras, intentos_fallidos, letras_usadas_str])

    # Escribir los datos actualizados en el CSV
    with open(archivo_stats, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(filas)
