# Python TCP Client 1
import socket 

# Connection details
host = socket.gethostname()
port = 6000
BUFFER_SIZE = 2048 

# Setup TCP connection
client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client1.connect((host, port))


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

# Divisor to be used for CRC
div = "1011"

# Default Code
code = "0" * (len(div) - 1)
# Note: >> len(code) = len(div)-1 <<
# eg. div='1010' code='000', div='10101' code='0000'

while True:
    # Data to be sent
    data = "XYZ"
    print 'Sending data: ' + data
    
    # bword to store the binary form of data
    bword = ''
    for letter in data:
        bword = bword + bin(ord(letter))[2:]
    print 'Binary conversion: ' + bword

    # Send binary coded data to server
    client1.send(data)
    
    # Receive CRC code from server
    recv_code = client1.recv(BUFFER_SIZE)

    # Perform Cyclic Redundancy Check
    if (crc(bword, div, recv_code) == code):
        print 'Success! Encoded Data: ' + bword + recv_code
    else:
        print 'Failure!'
    break
    
    
client1.close()
