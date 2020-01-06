from os import path

def serve(request, response):
    response.set_status('200 OK')
    file_path = path.join(path.dirname(path.realpath(__file__)), request.get_path())
    try:
        size = path.getsize(file_path)
        response.set_header("Content-Length", str(size))
        response.set_header("Content-Type", "text/html")
        chunk = 200

        f = open(file_path, "r")
        while True:
            data = f.read(chunk)
            if not data:
                break
            response.write_body(str.encode(data))
        f.close()
    except FileNotFoundError:
        print(file_path + " not found")