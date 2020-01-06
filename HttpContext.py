from Request import Request

class HttpContext:
    def __init__(self, raw_request):
        self.request_tokens = raw_request.splitlines()
        self.headers = dict()
    def parse(self):
        self.method, self.path, self.version = self.request_tokens[0].split()
        self.parseHeaders()
        return Request(self.method, self.path, self.version, self.headers)
    def parseHeaders(self):
        i = 1
        while(i < len(self.request_tokens) - 1):
            header_value_pair = self.request_tokens[i].split(':', 1)
            self.headers[header_value_pair[0].upper()] = header_value_pair[1].strip()
            i+=1