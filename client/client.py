import socket
import os

def send_file(filename):
    server_address = ('127.0.0.1', 12345)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    
    try:
        # Send the command and filename
        command = f"SEND {filename}"
        print(f"Sending command: {command}")
        client_socket.sendall(command.encode())

        # Send the file content
        with open(filename, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                client_socket.sendall(data)
                
        response = client_socket.recv(1024).decode()
        print(response)
        
    finally:
        client_socket.close()

def request_file(filename, save_as=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 12345)
    client_socket.connect(server_address)
    
    try:
        # Send the command and filename
        command = f"REQUEST {filename}"
        print(f"Sending command: {command}")
        client_socket.sendall(command.encode())

        response = client_socket.recv(1024).decode()
        if response == "File not found":
            print(response)
            return

        file_size = int(response)
        print(f"Receiving file: {filename} ({file_size} bytes)")

        if save_as is None:
            save_as = f"received_{filename}"

        with open(save_as, 'wb') as f:
            while file_size > 0:
                data = client_socket.recv(4096)
                f.write(data)
                file_size -= len(data)
                
        print(f"File {filename} received successfully")
        
    finally:
        client_socket.close()

if __name__ == '__main__':
    # Example usage
    send_file('example.txt')
    request_file('example.txt')