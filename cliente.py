###Clienteeeeeeeeeeeeeeeee

import socket
import datetime

SOCK_BUFFER = 1024

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("0.0.0.0", 5100)
    log_file = "historial_consultas.txt"

    try:
        print(f"Conectando al servidor en {server_address[0]}:{server_address[1]}")
        sock.connect(server_address)

        with open(log_file, "a", encoding="utf-8") as f:
            f.write("\n===== Nueva sesión =====\n")
            f.write(f"Inicio: {datetime.datetime.now()}\n\n")

            while True:
                producto = input("Consulta (o 'salir' para terminar): ")

                if not producto:
                    continue

                sock.sendall(producto.encode("utf-8"))
                f.write(f">>> Consulta: {producto}\n")

                if producto.lower() == "salir":
                    print("Cerrando conexión...")
                    f.write(">>> Sesión finalizada por el usuario.\n")
                    break

                data = sock.recv(SOCK_BUFFER)
                if not data:
                    print("Conexión perdida con el servidor.")
                    f.write(">>> Conexión perdida con el servidor.\n")
                    break

                respuesta = data.decode("utf-8")
                print("Respuesta:", respuesta)
                f.write(f"<<< Respuesta: {respuesta}\n\n")

            f.write(f"Fin: {datetime.datetime.now()}\n")
            f.write("=========================\n")

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor.")
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
    except Exception as e:
        print("Error:", e)
    finally:
        sock.close()
        print("Cliente cerrado.")



