import socket
serverIP = '172.17.29.11'
serverPORT = 6000

serveraddress = (serverIP, serverPORT)
bufferSize = 1024

UDPClientSocket = socket.socket(family.socket.AF_INET, tyoe = socket)