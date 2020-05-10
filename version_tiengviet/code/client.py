# https://realpython.com/python-sockets/
import socket

HOST, PORT = "127.0.0.1", 12345
ctrl_cyc="1234567"
data = ""
data += str(ctrl_cyc)

    # Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(b'Hello, world')
    data = sock.recv(1024)
    print(data)

finally:
    sock.close()