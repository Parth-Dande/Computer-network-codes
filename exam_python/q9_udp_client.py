# Q9: UDP Client - send lowercase string, receive uppercase string
import socket

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address
server_address = ("localhost", 9998)

print("UDP Client started...")

while True:

    message = input("\nEnter a lowercase string: ")

    # Send data to server
    client_socket.sendto(message.encode(), server_address)

    # Receive response
    data, server_address = client_socket.recvfrom(1024)

    print("Server response (Uppercase):", data.decode())

    again = input("\nDo you want to continue? (yes/no): ")

    if again.lower() == "no":
        break

client_socket.close()
