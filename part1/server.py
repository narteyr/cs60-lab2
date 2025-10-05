
import socket
import os

HOST = '0.0.0.0'
PORT = 9095
MIN_PARAMS = 2
ACCEPTED_METHODS = set(["GET"])

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))

    server_socket.listen()
    print(f"Listening at port: {PORT}")

    try:
        client_socket, client_addr = server_socket.accept()
        print(f"Received Connection from: {client_addr}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            request = data.decode()
            request_params = request.split(" ")
            if len(request_params) < MIN_PARAMS:
                error_message = "HTTP 400: BAD REQUEST"
                client_socket.sendall(error_message.encode())
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
                        client_socket.sendall(response.encode())
                        break


                except FileNotFoundError:
                    not_found_message = "HTTP/1.1 404 Not Found\r\n\r\n <html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
                    client_socket.sendall(not_found_message.encode())
                    break
            else:
                error_message = "HTTP 400: BAD REQUEST"
                client_socket.sendall(error_message.encode())
                break

    finally:
        client_socket.close()
        server_socket.close()
        
if __name__ == "__main__":
    main()