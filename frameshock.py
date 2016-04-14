import os

from tabulate import tabulate
import shodan;

from Injector.creator import creator
from config import config


class init(config, creator):


    def shodanSearch(self):
        print "Search target with Shodan:"
        print "(0 to return)"
        search = raw_input("Search word: ");
        if(search!="0"):
            api = shodan.Shodan(self.config.getApiKey())
            try:
                # Search Shodan
                resultsFirts = api.search(search)
                pages = resultsFirts['total']/100;
                print 'Results found: %s' % resultsFirts['total']
                print "Pages: %s" % pages
                addPages = raw_input("Input number of page to insert: ")
                self.error = False

                for page in range(1,int(addPages)+1):
                    try:
                        print "Adding Page: %s" % page
                        results = api.search(search,page)
                        # Show the results
                        for result in results['matches']:
                            sql = "Insert into results (ip,port,search) values('%s','%s','%s')" % (result['ip_str'],result['port'],search);
                            #print sql;
                            self.cur.execute(sql)
                            self.con.commit()
                    except:
                        self.error = True
                        pass
                if(self.error):
                    print "Error processing pages, check if your SHODAN KEY is a full key"
                print "Done target scanning"
                #raw_input("Press any key for Main menu")
                self.startModules();

            except shodan.APIError, e:
                    print 'Error: %s. Try again changing search value!' %e
        else:

            print "No target founds!"
            #raw_input("Press any key for Main menu")
            self.startModules();

    def manualTarget(self):
        ip = raw_input("Target ip/host: ");
        port = raw_input("Target port: ");
        description = raw_input("Description: ");
        sql = "Insert into results (ip,port,search) values('%s','%s','%s')" % (ip,port,description);
        #print sql;
        self.cur.execute(sql)
        self.con.commit()
        print "Done"
        #raw_input("Press any key for Main menu")

    def selectedModule(self,option):
        print "Load Module: " + self.modules[option].replace('_', ' ').replace(".py",'');
        try:
            cmd ="python ./Modules/"+self.modules[option]
            os.system(cmd)
            #execfile("./Modules/"+self.modules[option]);
        except:
            pass




    def showTargets(self):
        print "Targets: "
        targets = self.cur.execute("Select * from results").fetchall();
        if(len(targets)==0):
            print "No targets found"
            #raw_input("Press any key for Main menu")
        else:
            #print "|---------IP---------||----PORT----||---------Description---------|"
            #for target in targets:
            #    print target[1];
            print tabulate(targets, ["id", "IP", "PORT", "Description"], tablefmt="grid")
            #raw_input("Press any key for Main menu")

    def delTargets(self):
        option = raw_input("Description (Empty for all // 0 for cancel // 1 for module Description): ")
        if(option==""):
            print "Deleting..."
            self.cur.execute("DELETE FROM results")
        else:
            if(option!="0"):
                if(option=="1"):
                    description = raw_input("Set Module Description: ")
                    print "Deleting..."
                    sql = "DELETE FROM results where search='"+str(description)+"'";
                    self.cur.execute(sql);
                else:
                    print "No targets deleted";
            else:
                print "No targets deleted";

        self.con.commit();
        print "Done"
        #raw_input("Press any key for Main menu")

    def readModules(self):
        os.system("rm -rf ./Modules/*.pyc")
        ls = os.listdir("./Modules");
        ls.sort()
        ls.remove("__init__.py");
        return ls;

    def setHandler(self):
        print "**********Select Payload**********"
        print "1 /bin/sh Generic Reverse TCP"
        print "2 /bin/bash Generic Reverse TCP"
        print "3 Linux   Python  Reverse TCP"
        print "4 Win**   Python  Reverse TCP"
        print "5 Meterpy Reverse TCP (Python Meterpreter)"

        option = int(raw_input("Payload: "))
        if(option!=""):
            if(option==1):
                self.creator.setHandler("sh")
            if(option==2):
                self.creator.setHandler("bash")
            if(option==3):
                self.creator.setHandler("linux")
            if(option==4):
                self.creator.setHandler("windows")
            if(option==5):
                self.creator.setHandler("meterpy")
        else:
            print "No handler Selected"
        self.startModules()

    def writeConf(self):
        host = raw_input("IP/Host: ")
        lport = raw_input("LPORT: ")
        webPort = raw_input("Web Port: ")
        apachePath = raw_input("Apache Path: ")
        APIKey  = raw_input("Shodan API Key: ")
        if(host==""):
            host="www.example.org"
        if(lport==""):
            lport="5557"
        if(apachePath==""):
            apachePath="/var/www"
        if(webPort==""):
            webPort="80"
        if(APIKey==""):
            APIKey="xxxxxxxxxxxxxxxxxxxxxx"

        f = open(self.config.getPath()+"/config.py","w");

        model = open(self.config.getPath()+"/handler/config/config.model","r").read();

        model = model.replace(">>>HOST<<<",host)
        model = model.replace(">>>LPORT<<<",lport)
        model = model.replace(">>>APACHE<<<",apachePath)
        model = model.replace(">>>WEB<<<",webPort)
        model = model.replace(">>>APIKEY<<<",APIKey)

        #print model;

        f.write(model)

        f.close()


    def __init__(self):
        self.config = config()
        self.creator = creator()
        self.cur = self.config.getCursor();
        self.con = self.config.getCon();
        self.error = False;
        print "*******************************"
        print "Welcome to ShellShock Framework"
        print "*******************************"
        self.modules = self.readModules();
        self.startModules();

    def showModules(self):
        for module in self.modules:
                    print module.replace('_', ' ').replace(".py",'')

    def showHelp(self):
            print "***********HELP***********"
            print "show modules       --> show modules"
            print "use {moduleNumber} --> select a module"
            print "set payload        --> Create Payload"
            print "start handler      --> Start Handler"
            print "set target         --> Shodan Manual target"
            print "use shodan         --> Search with Shodan"
            print "show targets       --> Show targets"
            print "delete targets     --> Delete targets"
            print "config             --> Configuration"
            print "about              --> About"
            print "exit               --> Exit"

    def startModules(self):

        while True:

            option = raw_input("Main Menu > ").lower();


            if(option!=""):


                if(option.find("use")>-1):
                    if(option.find("shodan")>-1):
                        self.shodanSearch()
                    else:
                        option = option.split(" ")
                        option = int(option[1])-1;
                        self.selectedModule(option);
                if(option=="help"):
                    self.showHelp()
                if(option=="show modules"):
                    self.showModules()
                if(option=="set payload"):
                    self.setHandler()
                if(option=="start handler"):
                    self.creator.startHandler()
                if(option=="set target"):
                    self.manualTarget()
                if(option=="show targets"):
                    self.showTargets()
                if(option=="delete targets"):
                    self.delTargets()
                if(option=="config"):
                    self.writeConf()
                if(option=="about"):
                    print "Frameshock is powered by hdbreaker (Alejandro Parodi)"
                if(option=="exit"):
                    exit()

if os.geteuid() != 0:
    exit("You need to have root privileges")
else:
    Main = init()



        #Enviar a ejecutar el modulo
        #print self.modules[option-1];


