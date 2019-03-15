# coding: utf-8
import json
import socket
import struct
import threading


def handle_conn(conn,addr,handlers):
    print(addr,"comes")
    while True:
        length_prefix = conn.recv(4) #
        if not length_prefix:
            print(addr,"bye")
            conn.close()
            break
        length, = struct.unpack("I", length_prefix)
        body = receive(conn,length)  # 请求消息体  
        request = json.loads(body)
        in_ = request['in']
        params = request['params']
        print(in_, params)
        handler = handlers[in_]  # 查找请求处理器
        handler(conn, params)  # 处理请求
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
        conn,addr=sock.accept()
        threading._start_new_thread(handle_conn,(conn,addr,handlers))
#
def ping(conn,params):
    send_result(conn,"pong",params)


def send_result(conn,out,result):
    response = json.dumps({"out":out,"result":result})
    length_prefix = struct.pack("I",len(response))
    conn.sendall(length_prefix)
    conn.sendall(response.encode())

if __name__=="__main__":
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(("localhost",8100))
    sock.listen(1)
    handlers={
        "ping":ping
    }
    loop(sock,handlers)