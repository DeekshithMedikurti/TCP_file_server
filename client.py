#!/usr/bin/env python.
import socket
import json
HOST = "localhost"
PORT = 10887

class client:
    def main(self):
        #create a socket and connect to the server
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect_ex((HOST,PORT))
        #choose the file you wanna tinker with
        fileName = input("Please enter the file name you wanna tinker with\n")
        print('what do you wanna do with this file ?')
        print('upload: Upload it to the server')
        print('download: Download it to your system')
        print('rename: Rename the file')
        print('delete: Delete the file')
        x = input("Enter the name of the operation to perform.....\nfor example type in upload and press enter\n")
        x = str(x).strip()
        if(x=="upload"):
            c.transferFile(x,fileName,s)
        elif(x=="download"):
            c.downloadFile(x,fileName,s) 
        elif(x=="rename"):
            fileName1 = input("Enter new name for the file along with the extension: ")
            c.editFile(x,fileName,fileName1,s)
        elif(x=="delete"):
            c.deleteFile(x,fileName,s)
        s.close()

    #transferring file to the server
    def transferFile(self,x,fileName,s):
        var = [x,fileName]
        with open("/Users/deekshithbucky/Downloads/"+fileName, "r") as f:
            data = f.read().replace('\n', '')
        var.append(data)
        data = json.dumps(var)
        print(data)
        s.send(data.encode('utf8'))

    #download a file from the server    
    def downloadFile(self,x,fileName,s):
        var = [x,fileName]
        s.send(json.dumps(var).encode('utf8'))
        data = s.recv(1024)
        if not data:
            print("nothing is received...")
        string = data.decode("utf8")
        print(string)
        with open("/Users/deekshithbucky/Downloads/"+fileName, "w") as f:
            f.write(string)

    #edit the file on server
    def editFile(self,x,fileName,fileName1,s):
        var = [x,fileName,fileName1]
        data = str(var)
        s.sendall(data.encode())
        print("Message received from the server: ", s.recv(1024))

    #delete the file from the server.
    def deleteFile(self,x,fileName,s):
        var = [x,fileName]
        data = str(var)
        print(data)
        s.sendall(data.encode("utf8"))
        print("Message received from the server: ", s.recv(1024))

if __name__ == "__main__":
    c = client()
    c.main()  
