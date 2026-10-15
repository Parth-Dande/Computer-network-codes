import socket

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address
server_address = ("localhost", 9998)

print("UDP Client started...")

while True:

    print("\n1. Uppercase to Lowercase")
    print("2. Lowercase to Uppercase")
    print("3. Reverse String")

    choice = input("Enter your choice: ")

    message = input("Enter a string: ")

    # Combine choice and message
    data = choice + "|" + message

    # Send data to server
    client_socket.sendto(data.encode(), server_address)

    # Receive response
    data, server_address = client_socket.recvfrom(1024)

    print("Server response:", data.decode())

    again = input("\nDo you want to continue? (yes/no): ")

    if again.lower() == "no":
        break

client_socket.close()

## server
import socket

# Create UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address and port
server_address = ("localhost", 9998)

# Bind socket
server_socket.bind(server_address)

print("UDP Server started...")
print("Server is waiting for client...")

while True:

    # Receive data from client
    data, client_address = server_socket.recvfrom(1024)

    message = data.decode()

    # Separate choice and message
    choice, message = message.split("|", 1)

    print("\nClient connected from:", client_address)
    print("Message received:", message)

    # Perform operation
    if choice == "1":
        result = message.lower()

    elif choice == "2":
        result = message.upper()

    elif choice == "3":
        result = message[::-1]

    else:
        result = "Invalid choice"

    # Send result back to client
    server_socket.sendto(result.encode(), client_address)

    print("Response sent:", result)
