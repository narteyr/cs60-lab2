

"""
Purpose:
Date: 05/10/2025
author: Richmond Nartey Kwalah Tettey

"""

import socket
import threading
from server_comm import ServerCommunicator

HOST = '0.0.0.0'
PORT = 9091



class MainServer():
    def __init__(self, host,port):
        self.host = host
        self.port = port
        self.count = 0
        self.client_sockets: dict[str: threading.Thread] = {}

    def start(self):
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST,PORT))

            #listen for client connections
            server_socket.listen()
            print(f"Listening for client connections at port: ${PORT}")
            try:
                while True:
                    client_socket, client_addr = server_socket.accept()
                    print(f"Connected by ${client_addr}")
                    self.count += 1
                    new_server_communicator = ServerCommunicator(self, self.count, client_socket, client_addr)
                    new_server_communicator.start()
                    self.client_sockets[client_addr] = new_server_communicator
                    #print(f"[Server] number of threads: {threading.active_count()}")
            finally:
                server_socket.close()

    def remove_client(self, client_addr):
        if client_addr in self.client_sockets:
            del self.client_sockets[client_addr]
        self.count -= 1
        
        

    def log_thread_msg(self, msg:str):
         print(f"[ServerCommunicator] {msg}")

#setup  main socket
def main():
    server = MainServer(HOST, PORT)
    server.start()

if __name__ == "__main__":
    main()