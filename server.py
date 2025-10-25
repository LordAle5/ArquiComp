import socket
import math

SOCK_BUFFER = 1024

def busca_fila(producto: str):

    try:
        with open("orders_data_large.csv", "r") as f:
            contenido = f.read()
    except FileNotFoundError:
        print("Archivo no existe")
        return ""
    tabla = contenido.split("\n")
    #########################

    lista= list()

    for idx in range(1, len(tabla)):
        fila = tabla[idx]
        if producto in fila:
            lista.append(fila)

    lista_str="\n".join(map(str, lista))
    
    return lista_str 

def promedio_ventas(producto: str):
    lista=busca_fila(producto)
    suma=0
    lista_new=lista.split("\n")
    for i in range(len(lista_new)):
        fila=lista_new[i].split(",")
        suma+=float(fila[9])
    return suma/len(lista_new) 

def mejor_canal():
    try:
        with open("orders_data_large.csv", "r") as f:
            contenido = f.read()
    except FileNotFoundError:
        print("Archivo no existe")
        return ""
    tabla = contenido.split("\n")
    num_ventas_on=0
    num_ventas_of=0
    total_ventas_on=0
    total_ventas_of=0
    for i in range(1,len(tabla)):
        fila=tabla[i].split(",")
        if "Offline" in fila:
            num_ventas_of+=1
            total_ventas_of+=float(fila[8])
        if "Online" in fila:
            num_ventas_on+=1
            total_ventas_on+=float(fila[8])
    if total_ventas_of>total_ventas_on:
        mejor="Offline"
        num=num_ventas_of
        total=total_ventas_of
    else:
        mejor="Online"
        num=num_ventas_on
        total=total_ventas_on
    return mejor, num, total

def desviacion(producto : str):

    
    lista=busca_fila(producto)
    lista_new=lista.split("\n")
    media=promedio_ventas(producto)
    n=len(lista_new)
    suma=0
    for i in range(n):
        fila=lista_new[i].split(",")
        resta=float(fila[9])-media
        r=resta*resta
        suma+= r
    desviacion= math.sqrt(suma/n)

    return desviacion 

def cant_clientes():
    suma = 0.0
    clientes = 0

    try:
        with open("orders_data_large.csv", "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        print("Archivo no existe")
        return 0

    tabla = contenido.splitlines()  # mejor que split("\n"), maneja \r\n también

    # ---- PRIMERA PASADA: sumar valores válidos ----
    for i in range(1, len(tabla)):
        fila = tabla[i].split(",")
        # si la fila está vacía o incompleta, saltar
        if len(fila) <= 8 or not fila[8].strip():
            continue
        try:
            suma += float(fila[8])
        except ValueError:
            continue

    # evitar división por cero
    if len(tabla) <= 1:
        return 0

    promedio = suma / (len(tabla) - 1)

    # ---- SEGUNDA PASADA: contar los que superan el promedio ----
    for i in range(1, len(tabla)):
        fila = tabla[i].split(",")
        if len(fila) <= 8 or not fila[8].strip():
            continue
        try:
            if float(fila[8]) > promedio:
                clientes += 1
        except ValueError:
            continue

    return clientes


def distribucion(producto : str):

    media= promedio_ventas(producto)
    lista=busca_fila(producto)
    lista_new=lista.split("\n")
    ventas=list()
    n=len(lista_new)
    
    for i in range(n):
        fila=lista_new[i].split(",")
        venta=float(fila[9])
        ventas.append(venta)
    ventas.sort()
    min=ventas[0]
    max=ventas[-1]
    n_med=int((n-1)/2)
    mediana=ventas[n_med]

    return media,min,max,mediana



if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("0.0.0.0", 5100)

    print(f"Iniciando el servidor en {server_address[0]}:{server_address[1]}")

    sock.bind(server_address)

    sock.listen(1)

    while True:
        print("Esperando conexiones...")

        conn, addr = sock.accept()

        print(f"Conexión establecida desde {addr[0]}:{addr[1]}")

        try:
            while True:
                data = conn.recv(SOCK_BUFFER)
                if data:
                    print(f"Recibido: {data.decode('utf-8')}")
                    #_----------------------------
                    cod = data.decode("utf-8")
                    if cod=="salir":
                        conn.close()
                    elif "promedio" in cod:
                        serie=cod.split(" ")
                        codigo=serie[-1]
                        prom=str(promedio_ventas(codigo))
                        envio=str("El promedio de ventas de "+codigo+ "es "+prom)
                    elif "mejor" in cod:
                        mejor,num,total=mejor_canal()
                        envio="El mejor canal de ventas es "+str(mejor)+" con "+str(num)+" y con un total de "+str(total)+" de soles"
                    elif "desviación" in cod:
                        serie=cod.split(" ")
                        codigo=serie[-1]
                        desv=str(desviacion(codigo))
                        envio="La desviación estandar de "+codigo+" es "+desv
                    elif "cantidad" in cod:
                        cantidad_cl=str(cant_clientes())
                        envio="Los clientes con ventas superiores al promedio son: "+cantidad_cl
                    elif "distribución" in cod:
                        serie=cod.split(" ")
                        codigo=serie[-1]
                        media,min,max,mediana=distribucion(codigo)
                        envio="Distribución de ventas de "+codigo+": media: "+str(media)+" mediana: "+str(mediana)+" minimo: "+str(min)+" máximo: "+str(max)

                    #fila_lista = busca_fila(cod)
                    conn.sendall(envio.encode("utf-8"))
                else:
                    print("No hay mas datos.")
                    break
        except ConnectionResetError:
            print("El cliente cerró la conexión abruptamente.")
        finally:
            print("Cerrando la conexión.")
            conn.close()
