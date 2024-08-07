import socket
import sys

class SocketServer:
    def __init__(self, host, port):
        # Initialize the server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((host, port))
        self._server_socket.listen(1)
        print(f'Server listening on {host}:{port}')

    def handle_client_connection(self):
        try:
            # Accept a new connection
            conn, addr = self._server_socket.accept()
            print(f'Connected by {addr}')
            try:
                # Receive data from the client
                data = conn.recv(1024)
                if data:
                    print(f'Received: {data.decode("utf-8")}')
            finally:
                # Ensure the connection is closed
                conn.close()
        except Exception as e:
            print(f'Error: {e}')

    def close(self):
        # Close the server socket
        self._server_socket.close()

def main():
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9009

    server = SocketServer(host, port)
    
    try:
        while True:
            server.handle_client_connection()
    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        server.close()

if __name__ == '__main__':
    main()
