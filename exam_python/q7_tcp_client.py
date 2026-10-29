# Q7: TCP Client - send message to server
import socket

# Create TCP socket and connect
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 12345)
client_socket.connect(server_address)

print("Connected to TCP Server. Type 'exit' to quit.")

while True:

    message = input("\nEnter message: ")

    # Send message
    client_socket.send(message.encode())

    if message.lower() == "exit":
        break

    # Receive acknowledgement
    data = client_socket.recv(1024)
    print("Server response:", data.decode())

client_socket.close()
