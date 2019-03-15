# coding: utf-8
# client
import socket
import time
import struct
import socket
import json


def rpc(sock,in_,params):
    request = json.dumps({"in":in_,"params":params}) #serialize json
    length_prefix=struct.pack("I",len(request)) #
    sock.sendall(length_prefix)
    sock.sendall(request.encode())

    length_prefix=sock.recv(4) #length of response prefix
    length, = struct.unpack("I",length_prefix)#get first value
    body = sock.recv(length).decode()
    response = json.loads(body) #deserialize
    return response["out"],response["result"]


if __name__ == '__main__':
    
    
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("localhost",8100))
    for i in range(10):
        out,result=rpc(s,"ping","ireader %d" %i)
        print(out,result)
        time.sleep(1)
    s.close()

