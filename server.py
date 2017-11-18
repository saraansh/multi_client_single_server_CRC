import socket 
from threading import Thread 
from SocketServer import ThreadingMixIn 

def crc(msg, div, code='000'):
        msg = msg + code
        msg = list(msg)
        div = list(div)
        for i in range(len(msg)-len(code)):
            if msg[i] == '1':
                for j in range(len(div)):
                    msg[i+j] = str((int(msg[i+j])+int(div[j]))%2)
        return ''.join(msg[-len(code):])


class ClientThread(Thread):

    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print "New server socket thread for " + ip + ":" + str(port) 
 
    def run(self):
        key = '11100010'
        while True : 
            data = conn.recv(1024) 
            print "Server received data: ", data
            bword = ''
            for letter in data:
                bword = bword + bin(ord(letter))[2:]
            print 'Binary converted: ' + bword
            mycode = crc(bword, key, code='0000000')
            print 'Code: ' + mycode
            conn.send(mycode)
            break

TCP_IP = '0.0.0.0' 
TCP_PORT = 6000 
BUFFER_SIZE = 1024

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    print "Waiting for TCP clients..." 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join() 
