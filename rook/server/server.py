import socket

# Define host and port
HOST = "localhost"
PORT = 9999

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()
print("Server started. Listening for connections...")

while True:
    # Accept client connections
    client_socket, addr = server_socket.accept()
    print("Connected by", addr)

    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()

        if not data:
            break  # No more data, break out of the loop

        print("Received data:", data)

    # Close the connection for this client
    client_socket.close()
