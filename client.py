import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
running = True


try:
    client_socket.connect((HOST, PORT))
except ConnectionRefusedError:
    print("Не удалось подключиться к серверу")
    sys.exit()


def receive_messages():
    global running

    try:
        while running:
            data = client_socket.recv(1024)

            if not data:
                print("\nСервер отключился")
                break

            print(data.decode("utf-8"), end="")

    except:
        if running:
            print("\nСоединение с сервером потеряно")

    finally:
        running = False
        try:
            client_socket.close()
        except:
            pass


def send_messages():
    global running

    try:
        while running:
            message = input()

            if message.lower() == "exit":
                running = False
                break

            client_socket.sendall(message.encode("utf-8"))

    except:
        pass

    finally:
        running = False
        try:
            client_socket.close()
        except:
            pass


recv_thread = threading.Thread(target=receive_messages, daemon=True)
send_thread = threading.Thread(target=send_messages)

recv_thread.start()
send_thread.start()

send_thread.join()

print("Клиент завершил работу")