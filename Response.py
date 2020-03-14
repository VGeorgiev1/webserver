class Response:
    def __init__(self, status = None, headers = dict(), version = "HTTP/1.1", body=b''):
        self.version = version
        self.status = status
        self.headers = headers
        self.body = body
    def write_body(self, data):
        self.body += data
    def set_header(self, header, value): 
        self.headers[header] = value
    def get_raw(self):
        return bytes(
            self.version + 
            ' ' +
            self.status +
            '\r\n' +
            '\r\n'.join(map(lambda h: h[0] + ': ' + h[1], self.headers.items())) +
            '\r\n\r\n') + self.body
    def set_status(self, status):
        self.status = status
