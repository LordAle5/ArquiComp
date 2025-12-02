import ctypes
import time
import csv
import os

try:
    lib_cpu = ctypes.CDLL("./operaciones1.so")
    lib_io = ctypes.CDLL("./operaciones2.so")
except OSError:
    print("ERROR")
    exit()


lib_cpu.calcular_nota_final.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_int]
lib_cpu.calcular_nota_final.restype = ctypes.c_double

lib_cpu.calcular_media.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
lib_cpu.calcular_media.restype = ctypes.c_double

for func in [lib_cpu.calcular_moda, lib_cpu.calcular_min, lib_cpu.calcular_max]:
    func.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    func.restype = ctypes.c_int

lib_io.procesar_archivo_io.restype = ctypes.c_int

print("--- CARGANDO DATOS ---")
DATOS_ALUMNOS = [] 
COLUMNAS_C = []

try:
    with open("notas_alumnos.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        
        cols_raw = {c: [] for c in header[1:]} 
        
        for row in reader:
            try:
               
                notas = [int(float(x)) for x in row[1:]]
                
                labs = notas[:-2]
                ex1, ex2 = notas[-2], notas[-1]
                
                
                arr_labs = (ctypes.c_int * len(labs))(*labs)
                DATOS_ALUMNOS.append((arr_labs, len(labs), ex1, ex2))
                
               
                for i, val in enumerate(notas):
                    nombre_col = header[i+1]
                    cols_raw[nombre_col].append(val)
            except ValueError:
                continue 

    
    for nombre, lista in cols_raw.items():
        arr = (ctypes.c_int * len(lista))(*lista)
        COLUMNAS_C.append((arr, len(lista)))
        
    print(f"Datos listos: {len(DATOS_ALUMNOS)} alumnos, {len(COLUMNAS_C)} columnas.")

except FileNotFoundError:
    print("ERROR: Falta notas_alumnos.csv")
    exit()


def tarea_cpu():
    
    for args in DATOS_ALUMNOS:
        lib_cpu.calcular_nota_final(*args)
    
    
    for arr, n in COLUMNAS_C:
        lib_cpu.calcular_media(arr, n)
        lib_cpu.calcular_moda(arr, n)
        lib_cpu.calcular_min(arr, n)
        lib_cpu.calcular_max(arr, n)

def tarea_io():
    lib_io.procesar_archivo_io()


if __name__ == "__main__":
    ITERACIONES = 10000 
    ITERACIONES_IO = 10000

    print(f"\nEJECUCIÓN SECUENCIAL")
    
    start = time.perf_counter()
    for _ in range(ITERACIONES):
        tarea_cpu()
    print(f"Tiempo CPU ({ITERACIONES} iters): {time.perf_counter()-start:.4f} s")

    start = time.perf_counter()
    for _ in range(ITERACIONES_IO):
        tarea_io()
    print(f"Tiempo I/O ({ITERACIONES_IO} iters): {time.perf_counter()-start:.4f} s")