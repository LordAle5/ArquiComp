import ctypes
import time
import csv
from concurrent.futures import ThreadPoolExecutor


try:
    lib_cpu = ctypes.CDLL("./operaciones1.so")
    lib_io = ctypes.CDLL("./operaciones2.so")
except: exit()

lib_cpu.calcular_nota_final.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_int]
lib_cpu.calcular_nota_final.restype = ctypes.c_double
lib_cpu.calcular_media.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
lib_cpu.calcular_media.restype = ctypes.c_double
for func in [lib_cpu.calcular_moda, lib_cpu.calcular_min, lib_cpu.calcular_max]:
    func.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    func.restype = ctypes.c_int


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
                arr = (ctypes.c_int * len(labs))(*labs)
                DATOS_ALUMNOS.append((arr, len(labs), notas[-2], notas[-1]))
                for i, v in enumerate(notas): cols_raw[header[i+1]].append(v)
            except ValueError: continue
    for l in cols_raw.values():
        COLUMNAS_C.append(((ctypes.c_int * len(l))(*l), len(l)))
except: exit()


def tarea_cpu():
    for args in DATOS_ALUMNOS: lib_cpu.calcular_nota_final(*args)
    for arr, n in COLUMNAS_C:
        lib_cpu.calcular_media(arr, n)
        lib_cpu.calcular_moda(arr, n)
        lib_cpu.calcular_min(arr, n)
        lib_cpu.calcular_max(arr, n)

def tarea_io():
    lib_io.procesar_archivo_io()


WORKERS = [2, 4, 8, 16]

def correr_hilos(funcion, iters, nombre):
    print(f"\n--- {nombre} ---")
    for w in WORKERS:
        start = time.perf_counter()
        ops = iters // w
        def loop(_):
            for _ in range(ops): funcion()
        with ThreadPoolExecutor(max_workers=w) as ex:
            list(ex.map(loop, range(w)))
        print(f"Workers {w}: {time.perf_counter() - start:.4f} s")

if __name__ == "__main__":
    correr_hilos(tarea_cpu, 10000, "CPU-Bound Threading")
    correr_hilos(tarea_io, 10000, "I/O-Bound Threading")
