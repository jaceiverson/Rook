import pygame
import socket
import threading

# Define server host and port
HOST = "localhost"
PORT = 9999

# Initialize pygame
pygame.init()
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Card Game")

# Create YES and NO buttons
button_yes = pygame.Rect(50, 50, 100, 50)
button_no = pygame.Rect(250, 50, 100, 50)


def handle_connection():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("Connected to server")

    while True:
        # Receive data from the server
        data = client_socket.recv(1024).decode()
        if not data:
            break  # No more data, break out of the loop

        print("Received data:", data)

    # Close the connection
    client_socket.close()


# Create multiple client connections
num_clients = 3  # Specify the number of client connections you want
threads = []
for _ in range(num_clients):
    thread = threading.Thread(target=handle_connection)
    thread.start()
    threads.append(thread)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill((255, 255, 255))

    # Draw buttons
    pygame.draw.rect(screen, (0, 255, 0), button_yes)
    pygame.draw.rect(screen, (255, 0, 0), button_no)

    # Update the display
    pygame.display.flip()

# Wait for all threads to complete
for thread in threads:
    thread.join()
