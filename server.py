#!/usr/bin/env python.
import socket
import threading
import os, os.path
import errno

class server(object):
    #initialize server
    def __init__(self, host, port,lock):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.bind((self.host, self.port))
        self.lock = lock

    def listen(self):
        while True:
            self.sock.listen(5)
            conn,addr = self.sock.accept()
            print('connected by the user: ', conn)
            threading.Thread(target=self.listenToClient, args=(conn, addr)).start()


    def listenToClient(self,conn,addr):
        var = []
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                var = eval(data.decode('utf8'))
                print(var)
                x = str(var[0]).strip()
                print('coming after reading choice')
                print('choice: ',x)
                if x=="upload":
                    threading.Thread(target=self.receiveFile, args=(var,conn,self.lock)).start()
                if x=="download":
                    threading.Thread(target=self.sendFile, args=(var,conn,self.lock)).start()
                if x=="rename":
                    threading.Thread(target=self.renameFile, args=(var,conn,self.lock)).start()
                if x=="delete":
                    threading.Thread(target=self.deleteFile, args=(var,conn,self.lock)).start()
            except:
                conn.close()

    #receive a file.
    def receiveFile(self,var,conn,lock):
        with lock:
            pathh = "Users/user/"
            print("receiving file....")
            if not os.path.exists(pathh):
                self.mkdir_p(pathh)
            with open(pathh+var[1],"w") as f:
                f.write(str(var[2]))
            print('writing data '+var[2]+' to the file ')

    #send a file.
    def sendFile(self,var,conn,lock):
        with lock:
            with open("Users/user/"+var[1], "r") as f:
                data = f.read()
            conn.sendall(data.encode('utf8'))

    #rename a file on the Server.
    def renameFile(self,var,conn,lock):
        print('Renaming the file on Server....')
        with lock:
            if os.path.exists("Users/user/"+var[1]):
                print("coming here....")
                os.rename("Users/user/"+var[1],"Users/user/"+var[2])
                conn.send("file renamed successfully...".encode("utf8"))
            
    #delete a file from the Server.
    def deleteFile(self,var,conn,lock):
        print('Deleting the file you want.....')
        fileName = var[1]
        if os.path.exists("Users/user/"+fileName):
            os.remove("Users/user/"+fileName)
            conn.send("file deleted successfully.....")
        else:
            print('looks like the file is already deleted.')

    #create directory in the server
    def mkdir_p(self,pathh):
        try:
            os.makedirs(pathh,mode=0o777)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(pathh):
                pass
            else:
                raise

if __name__ == "__main__":
    lock = threading.Lock()
    server("localhost",10887,lock).listen()