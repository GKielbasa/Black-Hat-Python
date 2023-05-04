import socket
targetHost = "0.0.0.0"
targetPort = 9998

# Create a socket object1
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM to TCP

# Connect the client2
client.connect((targetHost, targetPort))

# Send some data3
client.send(b"ABCDEF")

# Receive some data4
response = client.recv(4096)

print(response.decode())
client.close()