# Q8: TCP Calculator Server - receive two numbers and operator, send result
import socket

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind and listen
server_address = ("127.0.0.1", 12345)
server_socket.bind(server_address)
server_socket.listen(1)

print("TCP Calculator Server started...")
print("Server is waiting for client on port 12345...")

client_socket, client_address = server_socket.accept()
print("Client connected from:", client_address)

while True:

    data = client_socket.recv(1024)

    if not data:
        break

    message = data.decode()

    if message.lower() == "exit":
        print("Client disconnected.")
        break

    # Separate num1|operator|num2
    num1, operator, num2 = message.split("|")
    num1 = float(num1)
    num2 = float(num2)

    print("\nReceived:", num1, operator, num2)

    # Perform operation
    if operator == "+":
        result = num1 + num2

    elif operator == "-":
        result = num1 - num2

    elif operator == "*" or operator == "x":
        result = num1 * num2

    elif operator == "/":
        if num2 == 0:
            result = "Error: Division by zero"
        else:
            result = num1 / num2

    else:
        result = "Invalid operator"

    # Send result back to client
    client_socket.send(str(result).encode())
    print("Result sent:", result)

client_socket.close()
server_socket.close()
