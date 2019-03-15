# coding: utf-8

import json
import socket
import struct
import asyncore
from io import StringIO

class RPCHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock, addr):
        asyncore.dispatcher_with_send.__init__(self,sock=sock)
        self.addr=addr
        self.handlers={
            "ping":self.ping
        }
        self.rbuf=StringIO
    
    def handle_connect(self):
        print(self.addr,"comes")
    
    def handle_close(self):
        print(self.addr,"bye")
        self.close()

    def handle_read(self):
        while True:
            content = self.recv(1024)
            if content:
                self.rbuf.write(content)
            if len(content)<1024:
                break
        self.handle_rpc()

    def handle_rpc(self): #handle received message
        while True:
            self.rbuf.seek(0)
            length_prefix = self.rbuf.read(4)
            if len(length_prefix)<4:
                break
            length,=struct.unpack("I",length_prefix)
            body=self.rbuf.read(length)
            if len(body)<length:
                break
            request=json.loads(body)
            #todo
    def ping(self,params):
        pass
    def send_result(self,out,result): #write buffer
        pass
class RPCServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host,port))
        self.listen(1)
    def handle_accept(self):
        pair=self.accept()
        if pair is not None:
            sock,addr=pair
            RPCHandler(sock,addr)

    