class Request:
    def __init__(self, method, path, version, headers):
        self.method = method
        self.headers = headers
        self.path = path
        self.version = version
    def get_headers(self):
        return self.headers
    def get_method(self):
        return self.method
    def get_path(self):
        return self.path[1:]
    def get_version(self):
        return self.version