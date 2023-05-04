import socket
targetHost = "127.0.0.1"
targetPort = 9997

#create socket object1
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #SOCK_DGRAM to UDP

#send some data2
client.sendto(b"AAABBBCCC", (targetHost, targetPort))

#recive some data3

data, addr = client.recvfrom(4096)
print(data.decode())
client.close()