import sys
import socket

if len(sys.argv) < 3:
    print("Usage: python3 client.py [server ip] [server port]")
    sys.exit(-1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def get_response():
    data = b''
    chunk = client_socket.recv(1024)
    while chunk:
        data += chunk
        chunk = client_socket.recv(1024)
    print(f"Received from server: {data.decode()}")

def send_message(message):
    client_socket.sendall(message.encode())
try:
    message = "GET /english_words.txt"
    send_message(message)
    get_response()

finally:
    client_socket.close()
