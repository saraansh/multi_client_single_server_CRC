# Python TCP Server
import socket 
from threading import Thread 
from SocketServer import ThreadingMixIn 

# Function to calculate CRC
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
        print 'New server socket thread for ' + ip + ':' + str(port) 
 
    def run(self):
        # Divisor to be used for CRC
        div = "1011"

        # Default Code
        code = "0" * (len(div) - 1)
        # Note: >> len(code) = len(div)-1 <<
        # eg. div='1010' code='000', div='10101' code='0000'

        while True :
            # Receive data sent from client
            data = conn.recv(1024) 
            print 'Server received data: ', data
            # bword to store the binary form of data
            bword = ''
            for letter in data:
                bword = bword + bin(ord(letter))[2:]
            print 'Binary conversion: ' + bword
            # Generate CRC code
            gen_code = crc(bword, div, code)
            print 'Code generated: ' + gen_code + '\n'
            # Send code to client
            conn.send(gen_code)
            break

TCP_IP = '0.0.0.0' 
TCP_PORT = 6000 
BUFFER_SIZE = 1024

# Setup TCP connection
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    print 'Waiting for TCP clients...\n' 
    (conn, (ip,port)) = tcpServer.accept()
    # Start a new thread for each client connection
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join() 
