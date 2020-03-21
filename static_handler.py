from os import path

from Response import Response


class Static:
    def __init__(self):        
        pass
    def handle(self,request):
        response = Response()

        file_path = path.join(path.dirname(path.realpath(__file__)), request.get_path())
        
        if not path.isfile(file_path):
            response.set_status("404 Not Found")
            return response

        chunk = 200
        f = open(file_path, "r")

        while True:
            data = f.read(chunk)
            if not data:
                break
            response.write_body(str.encode(data))

        size = path.getsize(file_path)
        f.close()

        response.set_header("Content-Length", str(size))
        response.set_status("200 OK")
        return response