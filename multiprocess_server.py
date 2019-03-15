# coding: utf-8

import os
import json
import socket
import struct
import multiprocessing
import decodeData
def handle_conn(conn,addr,handlers):
    print(addr,"comes")
    while True:
        
        data=("in","params")
        success,returnData = decodeData.decodeSelf(conn,data)
        if not success:
            print("something wrong in decoding")
            print(addr,"bye")
            break
        print(returnData)
        in_=returnData.get('in')
        params = returnData.get('params')
        handler = handlers[in_]
        handler(conn,params)

def loop(sock, handlers):
    while True:
        conn,addr = sock.accept()
        pid = os.fork() #create sub process
        if pid<0: #error
            return
        if pid>0: #parent process
            conn.close() #close parent process's socket
            return
        if pid==0:
            sock.close()
            handle_conn(conn,addr,handlers)
            break

def ping(conn,params):
    send_result(conn,"pong",params)

def send_result(conn,out,result):
    response=json.dumps({"out":out,"result":result})
    length_prefix = struct.pack("I",len(response))
    conn.sendall(length_prefix)
    conn.sendall(response.encode())

if __name__=='__main__':
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(("localhost",8100))
    sock.listen(1)
    
    handlers ={
        "ping":ping
    }
    loop(sock,handlers)

