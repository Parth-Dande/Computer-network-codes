# Q7: TCP Server - receive message from client and display it
import socket

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind and listen
server_address = ("127.0.0.1", 12345)
server_socket.bind(server_address)
server_socket.listen(1)

print("TCP Server started...")
print("Server is waiting for client on port 12345...")

# Accept connection
client_socket, client_address = server_socket.accept()
print("Client connected from:", client_address)

while True:

    # Receive message
    data = client_socket.recv(1024)

    if not data:
        break

    message = data.decode()

    if message.lower() == "exit":
        print("Client disconnected.")
        break

    print("Message received:", message)

    # Send acknowledgement
    client_socket.send(("Server received: " + message).encode())

client_socket.close()
server_socket.close()
