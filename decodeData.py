# coding: utf-8
import socket
import struct
import json

#data structure:
#----------------+------------
# 4 bytes(length)+  data
#----------------+-----------
def decodeSelf(conn,data):

        length_prefix=conn.recv(4) ## get first 4 bytes 
        if not length_prefix:
            
            return False,None
        length,=struct.unpack("I",length_prefix)
        body=receive(conn,length)
        if not body:
            print("EOF body!!!")
        # body=conn.recv(length).decode()#get the rest data
        request=json.loads(body)
        returnData=dict()
        for i in data:
            returnData[i]=request[i]
        return True,returnData

def receive(sock,n):
    res =[] 
    while n>0:
        r=sock.recv(n).decode()
        if not r: #EOF
            return res
        res.append(r)
        n-=len(r)
    return ''.join(res)