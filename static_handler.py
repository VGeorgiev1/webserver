from os import path

from Response import Response


class Static:
    def __init__(self):        
        pass
    def handle(self,request):
        response = Response('200 OK')
        file_path = path.join(path.dirname(path.realpath(__file__)), request.get_path())
        try:
            size = path.getsize(file_path)
            response.set_header("Content-Length", str(size))
            chunk = 200

            f = open(file_path, "r")
            while True:
                data = f.read(chunk)
                if not data:
                    break
                response.write_body(str.encode(data))
            f.close()
            return response
        except FileNotFoundError:
            print(file_path + " not found")