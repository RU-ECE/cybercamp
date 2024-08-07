import socket
import sys

def echo_server(port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = '0.0.0.0'

    # Bind to the port
    server_socket.bind((host, port))

    # Queue up to 5 requests
    server_socket.listen(5)
    print(f'Server listening on port {port}...')

    while True:
        # Establish a connection
        client_socket, addr = server_socket.accept()
        print(f'Got a connection from {addr}')

        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                print(f'Received: {data}')

                # Echo the received data back to the client
                client_socket.send(data.encode('utf-8'))

            except Exception as e:
                print(f'Error: {e}')
                break

        # Close the client connection
        client_socket.close()
        print(f'Connection from {addr} closed')

if __name__ == '__main__':
    # Get port from command line arguments or default to 9009
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9009
    echo_server(port)
