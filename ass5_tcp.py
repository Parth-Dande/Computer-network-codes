"""
Assignment 5: TCP Server and Client - INTERACTIVE INPUT MODE
Type your messages in the input box that appears!
Perfect for Google Colab

HOW TO USE:
1. Run this entire cell
2. Input boxes will appear - type your messages there!
"""

import socket
import threading
import time
from datetime import datetime


# ==================== TCP SERVER ====================
class TCPServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False

    def start(self):
        try:
            print("=" * 50)
            print("       TCP SERVER INITIALIZATION")
            print("=" * 50)

            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Auto port retry
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    self.server_socket.bind((self.host, self.port))
                    break
                except OSError:
                    if attempt < max_retries - 1:
                        self.port += 1
                    else:
                        raise

            print(f"\n✅ Socket bound to {self.host}:{self.port}")
            self.server_socket.listen(5)
            print(f"✅ Server listening on port {self.port}")

            self.running = True

            # Start accepting connections in thread
            accept_thread = threading.Thread(target=self.accept_connections)
            accept_thread.daemon = True
            accept_thread.start()

        except Exception as e:
            print(f"❌ Server failed: {e}")
            self.running = False

    def accept_connections(self):
        while self.running:
            try:
                self.server_socket.settimeout(1.0)
                client_socket, client_address = self.server_socket.accept()

                print(f"\n✅ Client connected from {client_address}")

                # Handle client in thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()

            except socket.timeout:
                continue
            except:
                if self.running:
                    pass

    def handle_client(self, client_socket, address):
        try:
            # Send welcome message
            welcome = "Welcome to TCP Server! Commands: TIME, DATE, HELLO, QUIT"
            client_socket.send(welcome.encode())

            while self.running:
                client_socket.settimeout(30.0)
                data = client_socket.recv(1024)

                if not data:
                    break

                message = data.decode().strip()
                print(f"\n📩 Received from client: {message}")

                response = self.process_request(message)

                if response == "DISCONNECT":
                    client_socket.send("Goodbye!".encode())
                    break

                client_socket.send(response.encode())
                print(f"📤 Sent to client: {response}")

        except:
            pass
        finally:
            client_socket.close()

    def process_request(self, request):
        cmd = request.upper()

        if "TIME" in cmd:
            return f"Server time: {datetime.now().strftime('%H:%M:%S')}"
        elif "DATE" in cmd:
            return f"Server date: {datetime.now().strftime('%Y-%m-%d')}"
        elif "HELLO" in cmd:
            return "Hello from TCP Server! 👋"
        elif "QUIT" in cmd or "EXIT" in cmd:
            return "DISCONNECT"
        else:
            return f"Echo: {request}"

    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass


# ==================== TCP CLIENT ====================
class TCPClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(5.0)

            self.client_socket.connect((self.host, self.port))

            # Receive welcome message
            welcome = self.client_socket.recv(1024).decode()
            print(f"\n✅ Connected! Server says: {welcome}\n")

            self.connected = True
            return True

        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def send(self, message):
        if not self.connected:
            print("❌ Not connected!")
            return None

        try:
            print(f"\n💬 You: {message}")
            self.client_socket.send(message.encode())

            # Receive response
            self.client_socket.settimeout(5.0)
            response = self.client_socket.recv(1024).decode()
            print(f"📨 Server: {response}\n")

            return response

        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def close(self):
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        self.connected = False


# ==================== INTERACTIVE MODE ====================
def run_interactive_tcp():
    """Run TCP with interactive input"""
    print("\n" + "*" * 60)
    print("     TCP INTERACTIVE MODE - Type Your Messages!")
    print("*" * 60)

    # Start server
    print("\n🚀 Starting server...")
    server = TCPServer('127.0.0.1', 12345)
    server.start()

    time.sleep(1)

    if not server.running:
        print("❌ Server failed to start")
        return

    print(f"\n✅ SERVER READY on port {server.port}")

    # Connect client
    print("\n🔗 Connecting client...")
    client = TCPClient('127.0.0.1', server.port)

    if not client.connect():
        server.stop()
        return

    print("=" * 60)
    print("📋 AVAILABLE COMMANDS:")
    print("  - TIME  : Get server time")
    print("  - DATE  : Get server date")
    print("  - HELLO : Get greeting")
    print("  - QUIT  : Exit")
    print("  - Or type anything else to echo it back!")
    print("=" * 60)

    # Interactive loop
    while True:
        try:
            # THIS IS WHERE YOU TYPE! 👇
            message = input("\n💬 Type your message (or 'quit' to exit): ")

            if not message.strip():
                continue

            response = client.send(message)

            if response and ("Goodbye" in response or message.upper() in ["QUIT", "EXIT"]):
                print("\n👋 Closing connection...")
                break

        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user")
            break
        except EOFError:
            # Colab specific: when input() doesn't work, switch to demo mode
            print("\n⚠️ Interactive input not available in this environment")
            print("🤖 Switching to demo mode...\n")

            demo_messages = ["HELLO", "TIME", "DATE", "Testing TCP", "QUIT"]
            for msg in demo_messages:
                client.send(msg)
                time.sleep(0.5)
            break

    # Cleanup
    client.close()
    server.stop()

    print("\n" + "*" * 60)
    print("     ✅ Session completed!")
    print("*" * 60)


# ==================== RUN IT ====================
if __name__ == "__main__":
    run_interactive_tcp()
