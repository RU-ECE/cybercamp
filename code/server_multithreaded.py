import socket
import threading
from concurrent.futures import ThreadPoolExecutor

class ThreadedServer:
    def __init__(self, host, port, num_threads):
        # Initialize the server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((host, port))
        self._server_socket.listen(5)  # Up to 5 queued connections
        self._executor = ThreadPoolExecutor(max_workers=num_threads)
        print(f'Server listening on {host}:{port} with {num_threads} threads')

    def handle_client(self, client_socket):
        try:
            # Read and print data from the client
            data = client_socket.recv(1024)
            if data:
                print(f'Received: {data.decode("utf-8")}')
        except Exception as e:
            print(f'Error: {e}')
        finally:
            # Close the client socket
            client_socket.close()

    def start(self):
        try:
            while True:
                # Accept a new connection
                client_socket, addr = self._server_socket.accept()
                print(f'Connected by {addr}')
                # Submit the connection to the thread pool
                self._executor.submit(self.handle_client, client_socket)
        except KeyboardInterrupt:
            print("Server is shutting down...")
        finally:
            self._server_socket.close()
            self._executor.shutdown(wait=True)

def main():
    host = '127.0.0.1'
    port = 9009
    num_threads = 4  # Define the number of threads in the pool

    server = ThreadedServer(host, port, num_threads)
    server.start()

if __name__ == '__main__':
    main()
