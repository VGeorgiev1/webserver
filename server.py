import socket
from HttpContext import HttpContext
import sys
from os import fork, _exit, waitpid, WNOHANG
import signal
from Response import Response
from Request import Request
from wsgi_handler import WSGI
from static_handler import Static
from logger import Logger

import errno
HOST, PORT = '', 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(10)


static_folder = '/home/vladislav/web-server/'

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
                headers += chunk[:body_start_found].decode('utf-8')
                
                headers_obj = parse_headers(headers)

                if len(chunk) > body_start_found + 4:
                    in_body = True
                    body += chunk[body_start_found:]

                    if 'CONTENT-LENGTH' not in headers_obj:
                        return Request({}, '')
                else:
                    break
        else:
            body += chunk

        if in_body and len(body) == int(headers_obj['CONTENT-LENGTH']) + 4:
            break

    return Request(headers_obj, body, )

activeChildren = []

def waitChild(signum, frame):
  pid, stat = waitpid(-1, WNOHANG)

signal.signal(signal.SIGCHLD, waitChild)

logger = Logger()

def server(handler):
    while True:
        try:
            c, addr = s.accept()

            child_pid = fork()

            if child_pid == 0:
                req = handle_client(c, addr)
                res = {}
                try:
                    res = handler.handle(req)
                    logger.access_log(req, res, addr[0])
                except Exception as ex:
                    logger.error_log(req, ex, addr[0])
                    res = Response("500 Internal Server Error")
                finally:
                    c.send(res.get_raw())
                    _exit(0)
            else:
                c.close()
        except socket.error as err:
            print(err)

if __name__ == '__main__':
    wsgi = WSGI(PORT, 'localhost')
    wsgi.load_application("./simple_flask_app.py")
    #static = Static()
    print('Server: Serving HTTP on port %s ...\n' % (PORT))
    server(wsgi)