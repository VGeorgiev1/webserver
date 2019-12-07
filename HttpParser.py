class HttpParser:
    def __init__(self, raw_request):
        self.request_tokens = raw_request.splitlines()
        self.headers = dict()
    def parse(self):
        self.method, self.path, self.version = self.request_tokens[0].split()
        self.parseHeaders()
    def parseHeaders(self):
        i = 1
        while(i < len(self.request_tokens) - 1):
            header_value_pair = self.request_tokens[i].split(':', 1)
            self.headers[header_value_pair[0].upper()] = header_value_pair[1].strip()
            i+=1
    def get_headers(self):
        return self.headers
    def get_method(self):
        return self.method
    def get_path(self):
        return self.path
    def get_version(self):
        return self.version