class Request:
    def __init__(self, headers, body):
        self.headers = headers
        self.body = body
    def get_headers(self):
        return self.headers
    def get_method(self):
        return self.headers['method']
    def get_path(self):
        return self.headers['path'][1:]
    def get_version(self):
        return self.headers['version']
    def get_body(self):
        return self.body