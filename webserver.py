import socket
import os

HOST = '127.0.0.1'
PORT = 8080       

def get_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return None

# Definisi/Fungsi ini memungkinkan webserver menampilkan file gambar
def get_mime_type(file_path):
    extension = os.path.splitext(file_path)[1]
    if extension == '.html':
        return 'text/html'
    elif extension == '.css':
        return 'text/css'
    elif extension == '.js':
        return 'text/javascript'
    elif extension == '.jpg' or extension == '.jpeg':
        return 'image/jpeg'
    elif extension == '.png':
        return 'image/png'
    elif extension == '.gif':
        return 'image/gif'
    else:
        return 'application/octet-stream'

# Fungsi socket
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
                response_header = 'Content-Type: {}\r\n'.format(get_mime_type(file_path))
                response_body = file_content
            else:
                response_status = 'HTTP/1.1 404 Not Found\r\n'
                response_header = ''
                # Halaman yang ditampilkan ketika file tidak ditemukan
                response_body = b'''
                    <html>
                    <head>
                        <title>404 Not Found</title>
                        <style>
                            body {
                                font-family: sans-serif;
                                text-align: center;
                                padding: 50px;
                            }
                            h1 {
                                font-size: 24px;
                                margin-bottom: 20px;
                            }
                            p {
                                font-size: 18px;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>404 Not Found</h1>
                        <p>The requested file could not be found.</p>
                    </body>
                    </html>
                '''


            response = response_status.encode('utf-8') + response_header.encode('utf-8') + b'\r\n' + response_body

            client_socket.sendall(response)