#  coding: utf-8 
import socketserver
import os 
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

# Copyright 2022 Amanda Nguyen
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

# try: curl -v -X GET http://127.0.0.1:8080/

# Ulvi Ibrahimov, September 28, https://stackoverflow.com/questions/21214484/display-html-file-using-socketserver-in-python
def readfile(folder_path):
    f = open(folder_path, 'r')
    data= ''
    for line in f:
        data = data + line
    return data

class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        ## decode data
        decode_data = self.data.decode("utf-8").split("\r\n")
        method, path, throwaway = decode_data[0].split(" ")

        ## if method is NOT GET return 405
        if "GET" != method:
            self.request.sendall(bytearray(
                        "HTTP/1.1 405 METHOD NOT ALLOWED\r\n", 'utf-8'))
        else:
            ## if it is not .html or .css AND it doesn't end with / then redirect
            if "." not in path and "/" != path[-1]:
                self.request.sendall(bytearray(
                            f"HTTP/1.1 301 MOVED PERMANENTLY\r\nLocation: {path}/\r\n", 'utf-8'))

            ## if its not .css or already has .html
            if "." not in path:
                path += "index.html"

            if "." in path and path[-1] == "/": #for some reason base.css gets turned into base.css/
                path = path[:-1]

            # No author, September 28 https://linuxize.com/post/python-get-change-current-working-directory/#:~:text=To%20find%20the%20current%20working,chdir(path)%20
            folder_path = os.getcwd() + "/www" + path

            try: # exception handles if we get a path that doesn't exist in a folder
                
                #Sugam Mankad, September 28 https://stackoverflow.com/questions/58475164/how-to-send-css-javascirpt-files-along-with-html-using-pythons-socketio
                # drew010, September 28, https://stackoverflow.com/questions/36122461/trying-to-send-http-response-from-low-level-socket-server
                #Gord Thompson, September 28, https://stackoverflow.com/questions/44657829/css-file-blocked-mime-type-mismatch-x-content-type-options-nosniff
                if ".html" in path:
                    data = readfile(folder_path)
                    self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\ncontent-type: text/html\r\nConnection: close\r\n\r\n\r\n{data}" , 'utf-8'))
                
                # James, September 27 https://stackoverflow.com/questions/38861763/send-css-over-python-socket-server
                elif ".css" in path:
                    data = readfile(folder_path)
                    self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\ncontent-type: text/css\r\nConnection: close\r\n\r\n\r\n{data}" , 'utf-8'))
                
                else:
                    self.request.sendall(bytearray(
                            "HTTP/1.1 404 NOT FOUND\r\nConnection: close\r\n\r\n\r\n", 'utf-8'))
            except:
                self.request.sendall(bytearray(
                            "HTTP/1.1 404 NOT FOUND\r\nConnection: close\r\n\r\n\r\n", 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
