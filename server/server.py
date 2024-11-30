# server.py
import socket
import os

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 12345)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print(f"Server is listening on {server_address}")
    
    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        try:
            print(f"Connection from {client_address}")
            command = client_socket.recv(1024).decode()
            if command.startswith("SEND"):
                filename = command[5:].strip()
                print(f"Receiving file: {filename}")
                with open(f"received_{filename}", 'wb') as f:
                    while True: 
                        data = client_socket.recv(4096)
                        if not data:
                            break
                        f.write(data)
                print(f"File received successfully")
                client_socket.sendall("File received successfully".encode())
            elif command.startswith("REQUEST"):
                filename = command[8:].strip()
                if not os.path.exists(filename):
                    client_socket.sendall("File not found".encode())
                    print(f"File {filename} not found")
                else:
                    file_size = os.path.getsize(filename)
                    client_socket.sendall(f"{file_size}".encode())
                    with open(filename, 'rb') as f:
                        while True:
                            data = f.read(4096)
                            if not data:
                                break
                            client_socket.sendall(data)
                    print(f"File {filename} sent successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            client_socket.close()

if __name__ == '__main__':
    start_server()