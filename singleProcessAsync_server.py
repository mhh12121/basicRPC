# coding: utf-8
# select model
import json
import socket
import struct
import asyncore
from io import BytesIO

class RPCHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock, addr):
        asyncore.dispatcher_with_send.__init__(self,sock=sock)
        self.addr=addr
        self.handlers={
            "ping":self.ping
        }
        self.rbuf=BytesIO
    
    def handle_connect(self):
        print(self.addr,"comes")
    
    def handle_close(self):
        print(self.addr,"bye")
        self.close()

    def handle_read(self):
        while True:
            content = self.recv(1024)
            if content:
                self.rbuf.write(self,content)
            if len(content)<1024:
                break
        self.handle_rpc()

    def handle_rpc(self): #handle received message
        while True:
            self.rbuf.seek(0)
            length_prefix = self.rbuf.read(self,4)
            if len(length_prefix)<4:
                break
            length,=struct.unpack("I",length_prefix)
            body=self.rbuf.read(length)
            if len(body)<length:
                break
            request=json.loads(body)
            in_=request["in"]
            params = request["params"]
            print(in_,params)
            handler = self.handlers[in_]
            handler(params)
            left=self.rbuf.getvalue()[length+4]#the whole buffer
            self.rbuf=BytesIO()#initialize buffer
            # self.rbuf=
            self.rbuf.write(left)
        self.rbuf.seek(0,2)#change stream to the end
        
    def ping(self,params):
        self.send_result("pong",params)
    def send_result(self,out,result): #write buffer
        response={"out":out,"result":result}
        body = json.dumps(response)
        length_prefix=struct.pack("I",len(body))
        self.send(length_prefix)
        self.send(body.encode())

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


if __name__=='__main__':
    RPCServer("localhost",8100)
    asyncore.loop()