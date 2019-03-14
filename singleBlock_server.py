# coding: utf-8
# server
import socket
import struct
import json
def handle_conn(conn,addr,handlers):
    print(addr,"comes")
    while True:
        length_prefix = conn.recv(4)
        if not length_prefix: #connection closed
            print (addr,' bye')
            conn.close()
            break # break out and handle next connection
        length, = struct.unpack("I",length_prefix) # I is integer
        body=receive(conn,length) #get body 
        # body = conn.recv(length) #get body raw method
        request = json.loads(body)
        in_=request['in']
        params = request['params']
        print( in_,params)
        handler = handlers[in_]
        handler(conn,params)

def receive(sock,n):
    res =[] 
    while n>0:
        r=sock.recv(n).decode()
        if not r: #EOF
            return res
        res.append(r)
        n-=len(r)
    return ''.join(res)

def loop(sock,handlers):
    while True:
        conn,addr = sock.accept()
        handle_conn(conn,addr,handlers)

def ping(conn,params):
    send_result(conn,"pong",params)

def send_result(conn,out,result):
    response = json.dumps({"out":out,"result":result}) #response body
    length_prefix = struct.pack("I",len(response)) #response length
    conn.sendall(length_prefix)
    conn.sendall(response.encode())

if __name__=='__main__':
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #oepn reuse addr option
    sock.bind(("localhost",8100))
    sock.listen(1)
    handlers = {
        "ping":ping
    }
    loop(sock,handlers)