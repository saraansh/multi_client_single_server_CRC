# Python TCP Client 1
import socket 

host = socket.gethostname() 
port = 6000
BUFFER_SIZE = 2048 
 
client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client1.connect((host, port))

def crc(msg, div, code='000'):
    msg = msg + code
    msg = list(msg)
    div = list(div)
    for i in range(len(msg)-len(code)):
        if msg[i] == '1':
            for j in range(len(div)):
                msg[i+j] = str((int(msg[i+j])+int(div[j]))%2)
    return ''.join(msg[-len(code):])

key = "11100010"

while True:
    data = "ODD"
    
    bword = ''
    for letter in data:
        bword = bword + bin(ord(letter))[2:]
    print 'Binary converted: ' + bword
    
    client1.send(data)
    mycode = client1.recv(BUFFER_SIZE)

    if (crc(bword, key, mycode) == '0000000'):
        print 'Success! ' + bword + mycode
    else:
        print 'Failure!'
    break
    
    
client1.close()
