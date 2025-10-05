
import threading
import socket
import enum

class StatusCode(enum.Enum):
    BAD_REQUEST = 400



STANDARD_METHODS = set(["GET"])
MIN_HEADERS = 3

class ServerCommunicator(threading.Thread):
    def __init__(self, server, count, client_socket: socket, client_addr):
        super().__init__()
        self.count = count
        self.client_socket = client_socket
        self.client_addr = client_addr
        self.server = server

    def run(self):
        print(f"[ServerCommunicator] [+] Thread{self.count} Connected to {self.client_addr}")
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                request = data.decode()
                message = f"Thread{self.count}(ip_address: {self.client_addr}, request: {request})"
                self.server.log_thread_msg(message)

                request_params: list[str]= request.split(" ")
                if len(request_params) < MIN_HEADERS:
                    error_message: str = f"HTTP/1.1 {StatusCode.BAD_REQUEST.value} {StatusCode.BAD_REQUEST.name}\r\n\r\n"
                    self.client_socket.sendall(error_message.encode())
                    break

                method, pathname = request[0], request[1]
                if method not in STANDARD_METHODS or not pathname.startswith("/"):
                    error_message: str = f"HTTP/1.1 {StatusCode.BAD_REQUEST.value} {StatusCode.BAD_REQUEST.name}\r\n\r\n"
                    self.client_socket.sendall(error_message.encode())
                    break


        finally:            
            self.client_socket.close()
            message: str = "[-] Closing connection to " + str(self.client_addr)
            self.server.log_thread_msg(message)
            self.server.remove_client(self.client_addr)