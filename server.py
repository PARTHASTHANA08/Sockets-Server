import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = "126.0.0.1"
port=5999
server.bind((ip_address,port))
server.listen()
nicknames=[]
list_of_clients=[]
question=[
    "What is the itallian word for Pie? \n a. Mozerrella \n b. Pastry \n c. Pizza \n d. pie",
    "Water boils at 212 degree at which unit scale? \n a. Fahrenhiet \n b.Celcius \n c.Kelvin \n d.Rankine",
]
answers =["c","a"]
print("The server has started!!")

def get_random_question_answers(conn):
    random_index = random.randit(0,len(question)-1)
    random_question = question[random_index]
    random_answers = answers[random_index]
    conn.send(random_question.encode("utf-8"))
    return random_index,random_question,random_answers
def remove_question(index):
    question.pop(index)
    answers.pop(index) 
def clientThread(conn):
    score=0
    conn.send("Welcome to this quiz game".encode("utf-8"))       
    conn.send("You will recieve a question and the answer will be either a,b,c or d".encode("utf-8"))
    conn.send("Good Luck \n \n".encode("utf-8"))
    index,question,answers = get_random_question_answers(conn)
    while True :
        try :
            message =conn.recv(2048).decode("utf-8")
            if message :
                if message.lower()==answers:
                    score =+ 1 
                    conn.send("Your score is {score}\n".encode("utf-8"))
                else :
                    conn.send("Incorrect Answer!! Better Luck next time".encode("utf-8"))
                remove_question(index)        
                index,question,answers = get_random_question_answers(conn)
            else:
                remove(conn)
        except:
            continue
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)
while True:
    conn, addr = server.accept()
    conn.send("NICKNAME".encode("utf-8"))
    nickname=conn.recv(2048).decode("utf-8")
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message = "{} joined !".format(nickname)
    print (message)
    broadcast(message,conn)
    new_thread = Thread(target= clientThread,args=(conn,nickname))
    new_thread.start()        