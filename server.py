#  coding: utf-8 
import socketserver

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

def read_path(data):
    begin = data.find(bytes('/', 'utf-8'))
    end =  data.find(bytearray('HTTP/1.1', 'utf-8'))
    #print('begin = ' + str(begin) + 'end = ' + str(end))
    return begin, end
    
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #self.data = self.request.recv(1024).strip()
        self.data = self.request.recv(1024).decode('utf-8')
        print ("Got a request of: %s\n" % self.data)
        
        string_list = self.data.split(' ')
        method = string_list[0]
        path = string_list[1].split('?')[0]
        print("method = " + method)
        print ("path = " + path)

        # path = path.lstrip('/')
           
        try:            
            if(path.endswith('.css')):
                #css file
                mimetype = 'text/css'
                header = 'HTTP/1.1 200 OK\n'
            elif(path.endswith('.html')):
                #html file
                mimetype = 'text/html'
                header = 'HTTP/1.1 200 OK\n'
            elif(path.endswith('/')): 
                #directory, go to index
                mimetype = 'text/html'
                path += 'index.html'
                # header = 'HTTP/1.1 301 Permanently Moved\n'
                header = 'HTTP/1.1 200 OK\n'
            else:
                #directory, go to index
                #redirect?
                mimetype = 'text/html'
                path += '/index.html'
                header = 'HTTP/1.1 301 Permanently Moved\n'
                # header = 'HTTP/1.1 200 OK\n'
            
            header += 'Content-Type: '+str(mimetype)+'\n\n'

            print('opening ./www' + path)
            file = open('./www' + path, 'rb')
            response = file.read()
            file.close()
            
        except Exception as e:  
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = """<html>
                          <body>
                            <center>
                             <h3>Error 404: File not found</h3>
                             <p>Python HTTP Server</p>
                            </center>
                          </body>
                        </html>""".encode('utf-8')
        
        self.request.sendall(header.encode('utf-8')+response)
        #self.request.close()
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
        
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
