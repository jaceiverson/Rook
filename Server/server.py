import pickle
'''
SERVER SIDE
https://stackoverflow.com/questions/42415207/send-receive-data-with-python-socket#42415879
'''
import socket
import os
from _thread import *

ServerSideSocket = socket.socket()
host = '10.0.0.169'
port = 5002
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
    connection.send(str.encode('Welcome to Rook'))
    while True:
        data = connection.recv(2048)
        response = 'Server message: ' + str(pickle.loads(data))
        if not data:
            break
        connection.sendall(str.encode(response))
    connection.close()

def get_name(connection):
    connection.sendall(str.encode('Please Enter Your Name: '))
    name= connection.recv(2048)
    return name

def create_player(sock_con,addr):
    pass

def connect_sockets(players=4):
    connections=0
    while connections<players:
        Client, address = ServerSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        create_player()
        start_new_thread(multi_threaded_client, (Client, ))
        connections += 1
        print('Thread Number: ' + str(connections))

connect_sockets(2)
ServerSideSocket.close()
'''
OLD WAY
players={}
HOST = '10.0.0.169'
PORT = 5002
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print('Listening')
conn, addr = s.accept()

print('Connected by', addr)
print(conn)


data = conn.recv(4096)
data_variable = pickle.loads(data)
conn.close()
print(data_variable)
# Access the information by doing data_variable.process_id or data_variable.task_id etc..,
print('Data received from client')
'''
