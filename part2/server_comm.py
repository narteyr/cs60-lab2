
import threading
import socket
import enum
import os

class StatusCode(enum.Enum):
    BAD_REQUEST = 400



ACCEPTED_METHODS = set(["GET"])
MIN_PARAMS = 2

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
                request_params = request.split(" ")
                if len(request_params) < MIN_PARAMS:
                    error_message = "HTTP 400: BAD REQUEST"
                    self.client_socket.sendall(error_message.encode())
                    break
                print(request_params)
                method, pathname = request_params[0], request_params[1]

                if method in ACCEPTED_METHODS and pathname.startswith("/"):
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    requested_path = pathname.lstrip("/")
                    file_path = os.path.join(base_dir, requested_path)
                    file_path = os.path.normpath(file_path)

                    try :
                        with open(file_path, 'r') as file:
                            html_content = file.read()
                            response = (
                            "HTTP/1.1 200 OK\r\n"
                            "\r\n"
                            f"{html_content}"
                            )
                            self.client_socket.sendall(response.encode())
                            break


                    except FileNotFoundError:
                        not_found_message = "HTTP/1.1 404 Not Found\r\n\r\n <html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
                        self.client_socket.sendall(not_found_message.encode())
                        break
                else:
                    error_message = "HTTP 400: BAD REQUEST"
                    self.client_socket.sendall(error_message.encode())
                    break

                request = data.decode()
                message = f"Thread{self.count}(ip_address: {self.client_addr}, request: {request})"
                self.server.log_thread_msg(message)

                request_params: list[str]= request.split(" ")
                if len(request_params) < MIN_HEADERS:
                    error_message: str = f"HTTP/1.1 {StatusCode.BAD_REQUEST.value} {StatusCode.BAD_REQUEST.name}\r\n\r\n"
                    self.client_socket.sendall(error_message.encode())
                    break


        finally:
            self.client_socket.close()
            message: str = "[-] Closing connection to " + str(self.client_addr)
            self.server.log_thread_msg(message)
            self.server.remove_client(self.client_addr)
