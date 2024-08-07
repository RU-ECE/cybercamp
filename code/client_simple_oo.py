import socket
import sys

class SocketClient:
    def __init__(self, host, port):
        # Initialize the client socket
        self.host = host
        self.port = port

    def send_message(self, message):
        try:
            self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._client_socket.connect((self.host, self.port))
            self._client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f'Error: {e}')
        finally:
            # Close the socket after sending the message
            self._client_socket.close()

def main():
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9009

    client = SocketClient(host, port)

    print("Enter your messages (end with EOF, Ctrl+D):")
    try:
        while True:
            # Read a line of input from the user
            message = input()
            if not message:
                break
            client.send_message(message)
    except EOFError:
        pass
    finally:
        print("Client is shutting down...")

if __name__ == '__main__':
    main()
