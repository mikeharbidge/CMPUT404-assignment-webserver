
import socket

BYTES_TO_READ = 4096

def get(hostname, port):
    request = b"GET / HTTP/1.1\nHost: " + hostname.encode('utf-8') + b"\n\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname,port))
        s.send(request)
        s.shutdown(socket.SHUT_WR)

        result = s.recv(BYTES_TO_READ)
        while(len(result)>0):
            print(result)
            result = s.recv(BYTES_TO_READ)


#get("www.google.com",80)
get("localhost",8080)
