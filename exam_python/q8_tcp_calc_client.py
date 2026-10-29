# Q8: TCP Calculator Client - send two numbers and operator, display result
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 12345)
client_socket.connect(server_address)

print("Connected to TCP Calculator Server.")

while True:

    num1 = input("\nEnter first number: ")
    operator = input("Enter operator (+, -, *, /): ")
    num2 = input("Enter second number: ")

    # Combine as num1|operator|num2
    data = num1 + "|" + operator + "|" + num2

    # Send to server
    client_socket.send(data.encode())

    # Receive result
    result = client_socket.recv(1024)
    print("Result from server:", num1, operator, num2, "=", result.decode())

    again = input("\nDo you want to continue? (yes/no): ")

    if again.lower() == "no":
        client_socket.send("exit".encode())
        break

client_socket.close()
