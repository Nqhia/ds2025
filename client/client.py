import socket
import os
import time

def send_file(filename):
    server_address = ('192.168.12.121', 12345)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    
    try:
        # Send the command and filename
        command = f"SEND"
        print(f"Sending command: {command}")
        client_socket.sendall(command.encode())

        response = client_socket.recv(1024)
        if response != b"OK":
            print(f"Error: {response}")
            return

        client_socket.sendall(filename.encode())

        response = client_socket.recv(1024)
        if response != b"OK":
            print(f"Error: {response}")
            return


        # Send the file size
        file_size = os.path.getsize(filename)
        print(f"Sending file: {filename} ({file_size} bytes)")
        client_socket.sendall(str(file_size).encode())

        
        # Send the file content
        with open(filename, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                client_socket.sendall(data)
                
        print("File sent successfully")
        
    finally:
        client_socket.close()

def request_file(filename, save_as=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.12.121', 12345)
    client_socket.connect(server_address)
    
    try:
        # Send the command and filename
        command = f"REQUEST"
        print(f"Requesting file: {filename}")
        client_socket.sendall(b'REQUEST')

        # Send the filename
        client_socket.sendall(filename.encode())
        
        # Receive the response from the server
        response = client_socket.recv(1024)
        if response == b'FILE_NOT_FOUND':
            print(f"Error: File {filename} not found on server")
            return False
        elif response == b'OK':
            # Receive the file size
            response = client_socket.recv(1024)
            response = client_socket.recv(1024)
            file_size = int(response.decode())  
            print(f"Receiving file: {filename} ({file_size} bytes)")
            client_socket.sendall(b'OK')
        
            # Receive the file content
            received_data = b''
            while len(received_data) < file_size:   
                data = client_socket.recv(4096)
                if not data:
                    break
                received_data += data
                # Print progress
            
            print("\nFile received successfully")
            
            # Save the received file
            save_path = save_as or f"received_{filename}"
            with open(save_path, 'wb') as f:
                f.write(received_data)
        
            print(f"File saved as {save_path}")
            return True

    except Exception as e:
        print(f"Error during file transfer: {e}")
        return False
    
    finally:
        client_socket.close()

if __name__ == '__main__':
    print("1. Send file")
    print("2. Request file")
    n = int(input("Enter your choice: "))
    if n == 1:
        filename = input("Enter the filename to send: ")
        send_file(filename)
    elif n == 2:
        filename = input("Enter the filename to request: ")
        request_file(filename)
    else:
        print("Invalid choice")