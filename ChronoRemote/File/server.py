import socketio
import eventlet
import socket
from time import sleep
import sqlite3

mydb = sqlite3.connect("C:/ChronoRemote/File/db/connected.db")
mycursor = mydb.cursor()
mycursor.execute("DELETE FROM connected;")
mydb.commit()
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    #connected
    pass

@sio.event
def disconnect(sid):
    #disconnected
    mydb = sqlite3.connect('C:/ChronoRemote/File/db/connected.db')
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM connected WHERE sid = ?;", (sid, ))
    mydb.commit()

@sio.event
def join_room(sid, user):
    mydb = sqlite3.connect('C:/ChronoRemote/File/db/connected.db')
    mycursor = mydb.cursor()
    try:
        mycursor.execute("INSERT INTO connected values( ? , ? , ?);", (user["room"], sid, user["username"]))
        mydb.commit()
        sio.enter_room(sid, user['room'])
    except:
        pass
      # Place client in the specified room

@sio.event
def message_from_client(sid, data):
    # Emitting an event to all clients in the specified room
    sio.emit('message_to_client', data=data, room=data["room"])

if __name__ == '__main__':
    # Create an eventlet WSGI server (or you can use gevent, asyncio, etc.)
    h_name = socket.gethostname()
    while True:
        IP_addres = socket.gethostbyname(h_name)
        if "127.0.0" not in IP_addres:
            eventlet.wsgi.server(eventlet.listen((IP_addres, 5300)), app)     
        else:
            sleep(5)