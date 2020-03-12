# Python3.7+
import socket
from HttpContext import HttpContext
import sys
from os import fork, _exit, waitpid, WNOHANG
import signal
from StaticHandler import serve
from Response import Response
from Request import Request
HOST, PORT = '', 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(10)

static_folder = '/home/vladislav/web-server/'

#print(f'Serving HTTP on port {PORT} ...')

def parse_headers(headers_str):
    headers = {}


    splited_headers = headers_str.splitlines()
    
    headers['method'], headers['path'], headers['version'] = splited_headers[0].split()
    splited_headers.pop(0)

    for header_pair in splited_headers:
        header, value = header_pair.split(':', 1)
        headers[str(header).upper()] = str(value).strip()
    return headers

def handle_client(client_connection, client_address):

    headers = ''
    body = b''
    in_body = False
    headers_obj = {}
    while True:
        chunk = client_connection.recv(1024)

        if not chunk:
            break
        
        if not in_body:

            body_start_found = chunk.find(b'\r\n\r\n')
            
            if  body_start_found < 0:
                headers += chunk.decode('utf-8')

            elif body_start_found >= 0:
                in_body = True
                
                headers += chunk[:body_start_found].decode('utf-8')
                
                headers_obj = parse_headers(headers)
                print(headers_obj)
                if 'CONTENT-LENGTH' not in headers_obj:
                    return Request({}, '')
                
                if len(chunk) > body_start_found:
                    body += chunk[body_start_found:]
        else:
            body += chunk

        if len(body) == int(headers_obj['CONTENT-LENGTH']) + 4:
            break
    print(headers_obj)
    return Request(headers_obj, body)

activeChildren = []

def waitChild(signum, frame):
  pid, stat = waitpid(-1, WNOHANG)

signal.signal(signal.SIGCHLD, waitChild)

def server():
    while True:
        c, addr = s.accept()
        child_pid = fork()

        if child_pid == 0:
            req = handle_client(c, addr)
            print(req.get_method())
            c.send(b'so far nothing')
            c.close()
            _exit(0)
        else:
            c.close()
server()