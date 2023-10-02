#  coding: utf-8 


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

import socketserver
import requests


#Todo:
    #Handle paths in www (return index from dir)
    #Handle mime types for HTML + CSS
    #Serve 404 and 405 when needed
    #screenshot of root and deep
    #Handle 301 to correct paths
    #Add source code git URL
    #Add license
_debug = True

class MyWebServer (socketserver.BaseRequestHandler):
    responseSent = False

    returnCode: str = "200 OK"
    dataList = []
    path = ""
    cssPath = ""
    method = ""
    fullpath = ""

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        #check if request is empty
        
        #decode bytestring, set method and filepath vars
        self.decodeData()

        #check method, if not GET/HEADER, return 405
        isValid = self.validateMethod()

        file = self.getFile(self.path)
        print(file)

        if not isValid:
            #Return 405 error
            self.returnCode = "405 Method Not allowed"
            isValid = False


        #check filepath, try to get file
        #if valid, return 200 and file
        #if valid when / is added, return 301 file
        #if invalid, return 404

        #set mime-types for files

        #return finalized response
        if not self.responseSent:
            self.assembleResponse(self.returnCode,file)
        

        

    def decodeData(self):
        #splits up data into a list
        decodeData = self.data.decode('utf-8')
        dataList = decodeData.split('\r\n')

        self.dataList = dataList

        #assign path
        pathsplit = self.dataList[0].split(" ")
        self.path = pathsplit[1]
        #assign method
        self.method = pathsplit[0]

        if _debug:print("PATH: " + self.path)
        if _debug:print("METHOD: " + self.method)

        if _debug:print(self.dataList[1])
        
    def parsePath(self):
        #parse filepath given in request

        #get file segment
        #split path itself from segment
        #try getting INDEX file from www/ + file path
        #try again with ending /
        #if invalid, return 404
        #if with /, return 301
        #check method for 405 if not GET
        #otherwise 200

        return None
    
    def validateMethod(self):
        #check method to see if is GET/HEAD, otherwise return 405
        isValid = False

        if (self.method == "GET" or self.method == "HEAD"):
            isValid = True

        return isValid
    
    def getFile(self,path:str):
        #try to get file at file path, if fails, handle error correctly
        basepath = "www"
        filepath = basepath + path

        #check if ends with index.html, any other file ignored as it gives 404
        isFile = False

        filesplit = filepath.split("/")
        print("LAST SPLIT: "+filesplit[len(filesplit)-1])

        #check if last split has dot to indicate filename
        if "." in filesplit[len(filesplit)-1]:
            isFile = True
        
        if (not isFile and filepath[len(filepath)-1] != '/'):
            if _debug:print("301: Invalid Filepath")
            returnCode = "301 Moved Permanently"
            filepath += '/'

        if not isFile:
            self.cssPath = filepath
        else:
        
            self.cssPath = (filepath.strip(filesplit[len(filesplit)-1]))
            print("cssPath:"+self.cssPath)
        
        if not isFile:
            #add index.html to filestring if not already present
            if _debug:print("Index not given")
            filepath += "index.html"
            print("filepath: "+ filepath)
            isFile=True
        
        self.fullpath = filepath
        try:
            if _debug:print("Getting file:" + filepath)
            f = open(filepath,"r",encoding="utf-8")
        except:
            #return status 404
            print("File not found at:"+filepath)
            self.returnCode = "404 Not Found"

        else:
            
            #f.close()
            return f
        

        return None
    
    def getCSS(self,path:str):
        basepath = "www"
        print(path)

        if (path == "/"):
            try:
                if _debug:print("Getting file:" + path)
                f = open(basepath + "/base.css","r",encoding="utf-8")
            except:
                #return status 404
                print("File not found at:"+ path)

            else:
                #f.close()
                return f
        else:
            try:
                if _debug:print("Getting file:" + path)
                f = open(basepath + "deep.css","r",encoding="utf-8")
            except:
                #return status 404
                print("File not found at:"+ path)

            else:
                #f.close()
                return f


        return None


        
    
    #assemble response based on response code and file to open
    def assembleResponse(self,returnCode:str, file=None):
        if _debug:print(self.returnCode)

        #Content-Type: text/html, text/css
        #if self.path

        response = ""
        content = ""

        if ".html" in self.fullpath:
            content = "text/html"
        elif ".css" in self.fullpath:
            content = "text/css"

        #if main file is html, also return css
        #if base dir, get base.css otherwise get deep.css
        self.getCSS(self.cssPath)

        response = self.returnCode+"\r\n"+"Content-Type: "+content+"\r\n"
        if file != None:
            response += "\r\n"
            response += file.read()

        print(response)

        self.request.sendall(bytearray(response,'utf-8'))

        return None
        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    if _debug:print("Running server...")
    server.serve_forever()
