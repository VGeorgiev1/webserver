# Python3.7+
import socket
from HttpContext import HttpContext
import sys
from os import fork, _exit, waitpid, WNOHANG
import signal
from StaticHandler import serve
from Response import Response
HOST, PORT = '', 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(10)

static_folder = '/home/vladislav/web-server/'

print(f'Serving HTTP on port {PORT} ...')


def handle_client(client_connection, client_address):
    request_data = client_connection.recv(4096)
    decoded = request_data.decode('utf-8')

    if(len(decoded) == 0):
        client_connection.close()
        return

    http = HttpContext(decoded)
    
    request = http.parse()
    response = Response()

    serve(request, response)

    client_connection.send(response.get_raw())
    client_connection.close()
    return

activeChildren = []

def waitChild(signum, frame):
  pid, stat = waitpid(-1, WNOHANG)

signal.signal(signal.SIGCHLD, waitChild)

def server():
    while True:
        c, addr = s.accept()
        ##reapChildren();
        child_pid = fork()

        if child_pid == 0:
            handle_client(c, addr)
            c.close()
            _exit(0)
        else:
            c.close()
server()