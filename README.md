# Simple HTTP Server with Compression Support

## Overview

This project implements a basic HTTP server in Python that supports GET and POST requests, file serving, and gzip compression. The server is designed to handle concurrent connections and respond to various endpoints with appropriate HTTP responses.

## Features

- Concurrent connection handling using threading
- Support for GET and POST methods
- Custom endpoints:
  - `/` - Root endpoint
  - `/echo/{string}` - Echoes the provided string
  - `/user-agent` - Returns the User-Agent of the client
  - `/files/{filename}` - Serves files from a specified directory
- gzip compression support
- Content-Type and Content-Length headers
- Optional directory specification for file serving

## Requirements

- Python 3.6+
- No external libraries required (uses only built-in Python modules)

## Usage

To start the server:

```bash
python server.py [--directory <path_to_directory>]
```
The ```--directory``` flag is optional. If provided, it specifies the directory from which the server will serve files for the ```/files/{filename}``` endpoint.

## Endpoints
1. Root Endpoint (```/```)
- Method: GET
- Response: 200 OK

2. Echo Endpoint (```/echo/{string}```)
- Method: GET
- Response: 200 OK
- Body: The string provided in the URL
- Supports gzip compression if the client accepts it

3. User-Agent Endpoint (```/user-agent```)
- Method: GET
- Response: 200 OK
- Body: The User-Agent string from the request headers
- Supports gzip compression if the client accepts it

4. Files Endpoint (```/files/{filename}```)
- Methods: GET, POST
- GET Response:
    - 200 OK if file exists
    - 404 Not Found if file doesn't exist
- POST Response: 201 Created
- Supports serving and uploading files
- Supports gzip compression for GET requests if the client accepts it

## Compression Support
The server supports gzip compression for responses. It checks the ```Accept-Encoding``` header in the request and compresses the response if the client accepts gzip encoding. The server adds appropriate ```Content-Encoding``` and ```Content-Length``` headers for compressed responses.

## Error Handling
+ 404 Not Found for non-existent endpoints or files
+ 405 Method Not Allowed for unsupported HTTP methods

## Concurrency
The server uses Python's threading module to handle multiple client connections concurrently. Each client connection is processed in a separate thread.
Code Structure
+ ```parse_request()```: Parses the incoming HTTP request
+ ```client_accepts_gzip()```: Checks if the client accepts gzip encoding
+ ```gzip_compress()```: Compresses data using gzip
+ ```handle_client()```: Main function to process client requests
+ ```main()```: Sets up the server socket and accepts client connections

## Future Improvements
+ Add support for more HTTP methods (PUT, DELETE, etc.)
+ Implement better error handling and logging
+ Add support for HTTPS
+ Implement request routing for easier endpoint management
+ Add configuration file support for server settings
+ Implement rate limiting and other security features

## Contributing
Contributions to improve the server are welcome.

## Acknowledgments
This project was developed as part of a coding challenge from CodeCrafters to implement a basic HTTP server with specific features and requirements.
