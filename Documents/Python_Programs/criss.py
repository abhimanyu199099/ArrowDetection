for i in range (0,100):
    import socket

    serverIP = '172.17.29.11'
    serverPORT = 6000

    serveraddress = (serverIP, serverPORT)
    bufferSize = 1024

    UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

    message = "luke, i am your father <insert vaders voice + breathing> *slow star wars theme*"

    bytestosend = str.encode (message)

    UDPClientSocket.sendto (bytestosend,serveraddress)
