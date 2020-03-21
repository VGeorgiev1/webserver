import io
import os, sys
import importlib.util
from Response import Response

class WSGI:
    def __init__(self, port, server_name):
        self.port = port
        self.server_name = server_name
        self.app = None
    def load_application(self, path): # taken from mdatsev
        module_dir = os.path.dirname(path)
        sys.path.append(module_dir)
        os.chdir(module_dir)
        spec = importlib.util.spec_from_file_location('application', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.app = module.app
    def handle(self, request):
        if self.app is None:
            raise Exception("You must provide wsgi app for the handler! Use load_application!")
        env = self.get_environ(request)

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
        env['PATH_INFO']         = request.get_path()
        env['SERVER_NAME']       = self.server_name
        env['SERVER_PORT']       = str(self.port)  # 8888
        return env