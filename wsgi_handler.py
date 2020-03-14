import io
import os, sys

from Response import Response

class WSGI:
    def __init__(self, port, server_name, app):
        self.app = app
        self.port = port
        self.server_name = server_name
    def handle(self, request):
        env = self.get_environ(request)

        print(request.get_headers())

        for (key, value) in request.get_headers().items():
            env['HTTP_' + key.replace('-', '_').upper()] = value
        result = self.app(env, self.start_response)

        for data in result:
            if data:
                self.response.write_body(data)

        return self.response

    def start_response(self, status, response_headers, exc_info=None):
        self.response = Response(status, dict(response_headers))
        return self.response.write_body

    def get_environ(self, request):
        env = {}
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = io.BytesIO(request.get_body())
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = request.get_method()    # GET
        env['PATH_INFO']         = request.get_path()      # /hello
        env['SERVER_NAME']       = self.server_name
        env['SERVER_PORT']       = str(self.port)  # 8888
        return env