# -*- coding: utf-8 -*-
import sys
sys.path.append('.')
from config import config
from tabulate import tabulate

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
                print "[*] Module Description"
                print "[*] by [Owner Nick]"

            if(option=="exploit"):
                self.exploit()
###################################

###Exploit c0de###
    def exploit(self):
        if(len(self.targets)!=0):
            for target in self.targets:
                ###YOUR EXPLOIT CODE HERE###
                print "Atack "+target[1]+":"+target[2]
                self.testFunctions()
        else:
            print "No targets found";

####def custom user functions (calleable from exploit())####
    def testFunctions(self):
        print "Mi first functions"
#############################################################

#####Init Module#####
start = module()
#####################