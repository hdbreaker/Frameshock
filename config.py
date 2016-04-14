import sqlite3
import os
class config():

    path = os.path.dirname(os.path.realpath(__file__))
    con = sqlite3.connect(path+"/db/"+"frameshock.db");
    host="192.168.0.107";
    LPORT=9669;
    WebPort=80
    Apache="/var/www"
    #Shodan API KEY
    #wAVHCCkorRhFNwGOE6JO9OXVkacdBxlH
    APIKey="wAVHCCkorRhFNwGOE6JO9OXVkacdBxlH";
    #filter for db
    filter = "";

    def __init__(self):
        pass

    def getApiKey(self):
        return self.APIKey;

    def getCursor(self):
        return self.con.cursor();

    def getCon(self):
        return self.con;

    def getHost(self):
        return self.host;

    def getPort(self):
        return self.LPORT;

    def getPath(self):
        return self.path

    def getApachePath(self):
        return self.Apache

    def getWebPort(self):
        return self.WebPort

    def getUrlInjector(self):
        url=""
        if(os.path.isfile(self.getApachePath()+"/Injector/injector.py")==True):
            url = self.host+":"+str(self.WebPort)+"/Injector/injector.py"
        if(os.path.isfile(self.getApachePath()+"/Injector/injector.sh")==True):
            url = self.host+":"+str(self.WebPort)+"/Injector/injector.sh"
        if(os.path.isfile(self.getApachePath()+"/Injector/injector.bash")==True):
            url = self.host+":"+str(self.WebPort)+"/Injector/injector.bash"
        return url

    def getInjectorName(self):
        file=""
        if(os.path.isfile(self.getApachePath()+"/Injector/injector.py")==True):
            file = "injector.py"
        if(os.path.isfile(self.getApachePath()+"/Injector/injector.sh")==True):
            file = "injector.sh"
        if(os.path.isfile(self.getApachePath()+"/Injector/injector.bash")==True):
            file = "injector.bash"
        return file

    def getTargets(self):
        cur = self.getCursor();
        self.filter=raw_input("Filter Descriptor: (Empty for all)")
        targets=[]

        if(self.filter!=""):
            sql = "Select * from results where search='%s'" % (self.filter)
            targets = cur.execute(sql).fetchall();
        else:
            targets = cur.execute("Select * from results").fetchall();
        return targets

