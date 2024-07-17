import socket
import threading
import os
import sys
import gzip
import io

def parse_request(request):
    request_parts = request.split(b'\r\n\r\n', 1)
    headers_part = request_parts[0].decode()
    body = request_parts[1] if len(request_parts) > 1 else b''
    
    lines = headers_part.split('\r\n')
    request_line = lines[0]
    method, path, _ = request_line.split(' ')
    
    headers = {}
    for line in lines[1:]:
        if line:
            key, value = line.split(': ', 1)
            headers[key.lower()] = value
    
    return method, path, headers, body


def client_accepts_gzip(accept_encoding):
    if not accept_encoding:
        return False
    encodings = [enc.strip().lower() for enc in accept_encoding.split(',')]
    return 'gzip' in encodings


def gzip_compress(data):
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode='w') as f:
        f.write(data.encode())
    return out.getvalue()


def handle_client(client_socket, directory):
    request = client_socket.recv(1024)
    
    method, path, headers, body = parse_request(request)
    
    # Check if client supports gzip
    accepts_gzip = client_accepts_gzip(headers.get('accept-encoding', ''))
    
    if method == 'GET':
        if path == '/':
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith('/echo/'):
            echo_string = path[6:]  # Remove '/echo/' from the beginning
            if accepts_gzip:
                compressed_content = gzip_compress(echo_string)
                content_length = len(compressed_content)
                response_headers = [
                    "HTTP/1.1 200 OK",
                    "Content-Type: text/plain",
                    f"Content-Length: {content_length}",
                    "Content-Encoding: gzip"
                ]
                response = ("\r\n".join(response_headers) + "\r\n\r\n").encode() + compressed_content
            else:
                content_length = len(echo_string)
                response_headers = [
                    "HTTP/1.1 200 OK",
                    "Content-Type: text/plain",
                    f"Content-Length: {content_length}"
                ]
                response = ("\r\n".join(response_headers) + "\r\n\r\n" + echo_string).encode()
        elif path == '/user-agent':
            user_agent = headers.get('user-agent', '')
            if accepts_gzip:
                compressed_content = gzip_compress(user_agent)
                content_length = len(compressed_content)
                response_headers = [
                    "HTTP/1.1 200 OK",
                    "Content-Type: text/plain",
                    f"Content-Length: {content_length}",
                    "Content-Encoding: gzip"
                ]
                response = ("\r\n".join(response_headers) + "\r\n\r\n").encode() + compressed_content
            else:
                content_length = len(user_agent)
                response_headers = [
                    "HTTP/1.1 200 OK",
                    "Content-Type: text/plain",
                    f"Content-Length: {content_length}"
                ]
                response = ("\r\n".join(response_headers) + "\r\n\r\n" + user_agent).encode()
        elif path.startswith('/files/') and directory:
            filename = path[7:]  # Remove '/files/' from the beginning
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    content = file.read()
                if accepts_gzip:
                    compressed_content = gzip.compress(content)
                    content_length = len(compressed_content)
                    response_headers = [
                        "HTTP/1.1 200 OK",
                        "Content-Type: application/octet-stream",
                        f"Content-Length: {content_length}",
                        "Content-Encoding: gzip"
                    ]
                    response = ("\r\n".join(response_headers) + "\r\n\r\n").encode() + compressed_content
                else:
                    content_length = len(content)
                    response_headers = [
                        "HTTP/1.1 200 OK",
                        "Content-Type: application/octet-stream",
                        f"Content-Length: {content_length}"
                    ]
                    response = ("\r\n".join(response_headers) + "\r\n\r\n").encode() + content
            else:
                response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    elif method == 'POST':
        if path.startswith('/files/') and directory:
            filename = path[7:]  # Remove '/files/' from the beginning
            file_path = os.path.join(directory, filename)
            with open(file_path, 'wb') as file:
                file.write(body)
            response = b"HTTP/1.1 201 Created\r\n\r\n"
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    else:
        response = b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"
    
    client_socket.sendall(response)
    client_socket.close()


def main():
    directory = None
    if len(sys.argv) >= 3 and sys.argv[1] == "--directory":
        directory = sys.argv[2]
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, directory))
        client_thread.start()


if __name__ == "__main__":
    main()
