import socket

HOST = '127.0.0.1'
PORT = 8080       

def get_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return None

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print('Server is running at http://{}:{}/'.format(HOST, PORT))

    while True:
        client_socket, client_address = server_socket.accept()

        with client_socket:
            print('Connected to the client ', client_address)

            request = client_socket.recv(1024).decode('utf-8')

            request_lines = request.split('\r\n')
            request_method, request_path, request_protocol = request_lines[0].split()

            file_path = request_path.lstrip('/')
            file_content = get_file(file_path)

            # HTTP response
            if file_content is not None:
                response_status = 'HTTP/1.1 200 OK\r\n'
                response_header = 'Content-Type: text/html\r\n'
                response_body = file_content.decode('utf-8')
            else:
                response_status = 'HTTP/1.1 404 Not Found\r\n'
                response_header = ''
                response_body = '<h1>404 Not Found</h1><p>The requested file could not be found.</p>'

            response = response_status + response_header + '\r\n'.join(request_lines[1:]) + '\r\n\r\n' + response_body

            client_socket.sendall(response.encode('utf-8'))