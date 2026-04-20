import socket
import threading
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(("127.0.0.1", 5000))
except ConnectionRefusedError:
    print("Не удалось подключиться к серверу")
    sys.exit()


def receive_messages():
    """Поток для приёма сообщений от сервера."""
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("Сервер отключился")
                break

            print(data.decode("utf-8"), end="")
    except:
        print("Соединение с сервером потеряно")
    finally:
        try:
            client_socket.close()
        except:
            pass


def send_messages():
    """Поток для отправки сообщений на сервер."""
    try:
        while True:
            message = input()
            if message.lower() == "exit":
                break

            client_socket.send(message.encode("utf-8"))
    except:
        pass
    finally:
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