import socket
import pickle

def create(HOST,PORT):
    # Create a socket connection.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

def send(data,s):

    # Pickle the object and send it to the server
    data_string = pickle.dumps(data)
    s.send(data_string)

def send_name():
    pass
if __name__=='__main__':

    h='10.0.0.169'
    p=5002
    sock=create(h,p)

    Card={'jace':['1',2,3,4,5,6]}
    
    other={'nat':[1,2,3,4,5,'6']}
    send(Card,sock)
    #send(other,sock)

    '''
    while True:
        if sock.recv(4096)
    '''
    #sock.close()
