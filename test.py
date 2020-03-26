import os
stream = os.popen('ab -n 100 -c 10 localhost:8888/hello')
output = stream.read()
print(output)

