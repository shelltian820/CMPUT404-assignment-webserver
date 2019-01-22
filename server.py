#  coding: utf-8 
import socketserver
import os
from pathlib import Path

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

RESPONSE_404 = """<html>
                    <body>
                    <center>
                        <h3>Error 404: File not found</h3>
                        <p>Python HTTP Server</p>
                    </center>
                    </body>
                </html>""".encode('utf-8')
STATUS_404 = 'HTTP/1.1 404 Not Found\n\n'.encode('utf-8')
STATUS_301 = 'HTTP/1.1 301 Permanently Moved\n'.encode('utf-8')
STATUS_200 = 'HTTP/1.1 200 OK\n'.encode('utf-8')
    
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #self.data = self.request.recv(1024).strip()
        self.data = self.request.recv(1024).decode('utf-8')
        print ("Got a request of: %s\n" % self.data)
        
        string_list = self.data.split(' ')
        method = string_list[0]
        path = './www' + string_list[1].split('?')[0]
        print("method = " + method)
        print ("path = " + path)
        
        base_directory = os.getcwd() + "/www"
        print('base dir', base_directory)
        print('realpath', os.path.abspath(path))
        if (os.path.realpath(path).startswith(base_directory) == False):
            header = STATUS_404
            response = RESPONSE_404
            print('Access Denied!')
            self.request.sendall(header+response)
            return 

        if(path.endswith('.css')):
            #css file
            mimetype = 'text/css'
            header = STATUS_200
        elif(path.endswith('.html')):
            #html file
            mimetype = 'text/html'
            header = STATUS_200
        elif(path.endswith('/')): 
            #directory, go to index
            mimetype = 'text/html'
            path += 'index.html'
            header = STATUS_200
        else:
            #directory, go to index
            #redirect?
            mimetype = 'text/html'
            path += '/index.html'
            header = STATUS_301   

        header += ('Content-Type: '+str(mimetype)+'\n\n').encode('utf-8')


        try:            
            print('opening ' + path)
            file = open(path, 'rb')
            response = file.read()
            file.close()
            
        except Exception as e:  
            print('exception!!!')
            header = STATUS_404
            response = RESPONSE_404
        
        self.request.sendall(header+response)
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
        
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
