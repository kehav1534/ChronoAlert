#Source code by:- Keshav Maheshwari
import sys
from pynput import keyboard 
import time
import threading
import os
import win32api
import psutil
import plyer.platforms.win.notification
from plyer import notification
import json
import socketio
import socket
import sqlite3

recent = time.time()
older_time = time.time()
myapp = "ChronoAlert"
file_path = 'C:\ChronoAlert\icon'    #File path location of Shut_Down Timer Folder.

def shutdown():
    os.system('shutdown /s /f /t 0')

def restart():
    os.system("shutdown /r /f /t 0")

def sleep():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def other():
    pass

def keys():
    def on_key_release(key): #what to do on key-release
        global recent, older_time
        recent = older_time = time.time()
        return True

    with keyboard.Listener(on_release = on_key_release) as release_listener: #setting code for listening key-release
        release_listener.join()

def cursor():
    #Track the movement of the cursor.
    savedpos = win32api.GetCursorPos()
    while(True):
        global recent, older_time
        curpos = win32api.GetCursorPos()
        if savedpos != curpos:
            recent = older_time = time.time()
            savedpos = curpos  
        time.sleep(0.5)
         
#Reads the notification.json get the notification messages.
def readJson(path="notification.json", data=None):
    
    with open("C:\ChronoAlert\python_source\\"+path, "r+") as file:
        notifi_data = json.load(file)
        return notifi_data

notification_list = readJson()

def notify():
    #These are some of my reminders. You can also add your custom reminders.
    # You can make your custom reminder by adding a it into notifications.json                      
    def notifications(n):
        while True:
            try:
                time.sleep(notification_list[n]["sleep"])
                notification.notify(
                    title  = notification_list[n]["title"],
                    message = notification_list[n]["message"],
                    app_icon =  file_path+"\\"+notification_list[n]["app_icon"],
                    timeout = notification_list[n]["timeout"],
                    app_name = myapp
                )
            except Exception as e:
                pass
    #schedule        
    def rest_notification():
        while True:
            #Send Notification after 5 hours and put system to hybernation in next 15min.
            #Save your work before time runs out.
            time.sleep(18000)
            notification.notify(
                title = "Working for too long...@-@",
                message = "Take Some rest. Going to Hybernation in 15 minutes.",
                app_icon = file_path+"\\systemlockscreen_104197.ico" ,
                timeout = 10,
                app_name = myapp
            )
            time.sleep(900)
            sleep()

    #Made threads of notifications so that they keep running in parallel-like fasion.
    for mesg in range(len(notification_list)):                                       
        notify1 = threading.Thread(target= notifications, args=(mesg, ))
        notify1.start()
    notify3 = threading.Thread(target=rest_notification)
    #Start your threads to make them run, or else won't work.
    notify3.start()

#Shut-down windows operating system.
def useDB(op="*"):
    mydb = sqlite3.connect('C:/ChronoAlert/db/config.db')
    mycursor = mydb.cursor()
    k = mycursor.execute(f"Select {op} from userprofile;").fetchone()
    mydb.close()
    return k

def check_user():
    #Checks whether the user has made any movement through keyboard or mouse.
    while(True):
        global recent, older_time
        recent = time.time()
        not_moved = recent - older_time
        if(3008 > not_moved > 3000):
            notification.notify(
                title = "Are you there!?",
                message= "You haven't touched your device for a while. Shutting down your device in 10 minutes.",
                app_icon = file_path+"\com_94378.ico",
                app_name = myapp,
                timeout  =10
                )
            time.sleep(10) #To stop the repeted occurence of notification Or else it will be called 3-4times
        elif(3550> not_moved > 3540):       
            ##Notify the user 1 minute before shutting down.
            notification.notify(
                title = "Shutting Down",
                message = "You don't seem to be using the device. Shutting Down in a minute.",
                app_icon = file_path+"\com_94378.ico",
                timeout =10,
                app_name = myapp
            )
            time.sleep(10)
        elif(not_moved > 3600):     
            #Shuts Down the device after an hour.
            shutdown()
        time.sleep(1)

def sysBattery():           
    #ShutDown the system when battery is lower than 7% and 
    #if charger is not plugged-in.
    #checks battery in every 5seconds.
    notified = False
    battery = psutil.sensors_battery()
    while(True):
        if battery.percent<=7 and battery.power_plugged == False and not notified:
            notification.notify(
                title = "Charging below 7%",
                message = "Plug-in the charger. System will ShutDown at 5%",
                app_icon = file_path+"\com_94378.ico",
                timeout = 15,
                app_name = myapp
            )
            notified = True

            if psutil.sensors_battery().power_plugged == False and battery.percent<=5:shutdown()
        elif battery.percent>7 and notified:notified=not notified
                
        time.sleep(7)

ops = {
    "shutdown" : shutdown,
    "restart"  : restart,
    "sleep"    : sleep
}

def changeroom():
    while True:
        time.sleep(15)
        user = useDB("username, fnet")
        if room!=useDB("room")[0] or (username!= user[0] and user[0] is not None)or(fnet!=user[1]):
            sio.disconnect()
            
def update(col, data):
    mydb = sqlite3.connect('C:/ChronoAlert/db/config.db')
    mycursor = mydb.cursor()
    mycursor.execute(f"UPDATE userprofile SET {col}=?;",(data, ))
    mydb.commit()

def remote():
    global IP_addres
    h_name = socket.gethostname()
    while True:
        IP_addres = socket.gethostbyname(h_name)      
        tmp = IP_addres.split(".")
        if "127.0.0" not in IP_addres:
            global sio, room, username, fnet
            room = useDB("room")[0]
            fnet=useDB("fnet")[0]
            username=useDB("username")[0]
            if username is None:username = socket.gethostname()
            if room is None:room="Unique-id unavailable"
            sio = socketio.Client()

            # Connect to the server
            @sio.event
            def connect():
                update("connectedIP", IP_addres+':5100')
                sio.emit('join_room', {"room": room, "username":username})
            # Start the client
            try:
                if fnet:
                    IP_addres = f'http://{tmp[0]}.{tmp[1]}.{tmp[2]}.{fnet}'
                    sio.connect(IP_addres+':5300')
                #Try to connect to the network server
                else:IP_addres='http://'+IP_addres;sio.connect(IP_addres+':5300')
                
                @sio.event
                def message_to_client(data):
                    if username in data["users"]:
                        ops.get(data["event"], other)()
                # Close the connection
                @sio.event
                def disconnect():
                    update("connectedIP", None)
                    1/0 #Interupt to go out of sio.wait() loop
                    
                sio.start_background_task(target=changeroom)
                sio.wait()
                
            except:
                ####Tryinng to connect
                time.sleep(5)
        else:
            ###Not Connected
            time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        notification.notify(
            title = myapp,
            message = "Application running in background.",
            app_icon = file_path+"\emoji_laughing_fill_icon_185681.ico" ,
            timeout = 10,
            app_name = myapp
        )
        #func_list contains the list of functions which are required to be threaded
        func_list = (keys, check_user, sysBattery, notify, cursor, remote)                  #add notify to the list
        for func in func_list:
                thread = threading.Thread(target=func)
                thread.start()

    else:
        def none():print("Error: Invalid operation executed. Type \help for correct syntax.")

        def SetOp(opr):
            def update(col, data):
                mydb = sqlite3.connect('C:/ChronoAlert/db/config.db')
                mycursor = mydb.cursor()
                if data not in [" ",""]:
                    if data is not None: data=data.upper()
                    try:
                        mycursor.execute(f"UPDATE userprofile SET {col}=?;", (data, ))
                        mydb.commit()
                        print(f"..{col} updated.")
                    except:none()
                else:none()
            try:   
                if opr[0] == "username":update(opr[0],opr[1])
                elif opr[0] == "room":update(opr[0],opr[1])
                elif opr[0] == "fnet" and isinstance(int(opr[1]), int) and 0<=int(opr[1])<=255:update(opr[0], opr[1])
                elif opr[0] == "delete":update(opr[1], None)
                else:none()
            except:none()

        def ShowOp(col):
            def show():
                mydb = sqlite3.connect('C:/ChronoAlert/db/config.db')
                mycursor = mydb.cursor()
                mycursor.execute(f"Select {col} from userprofile;")
                fetched = mycursor.fetchone()[0]
                if col =="connectedIP":
                    fetched+=":5100"
                print(f"..{col}\t:\t{fetched}")
            opselect={
                "username":show,
                "room":show,
                "connectedip": show
            }
            opselect.get(col, none)()

        def guide():
            print(    """
            set username [username] --- Add/Update Username displayed on WebControl.
            set room [unique code]  --- Add/Update Unique code for authorized Control.
            set fnet                --- Add/Update Fourth octanet of ipAddress.
                                        fnet value is between 0 and 255
                                            -open Command-prompt on Server Computer:
                                                -Type 'ipconfig':
                                                    -Search Ip4 Address
                                                        ex.IP4 Address:   194.43.194.45
                                                        Here, 45 is fnet.
                                                        
            show username           --- Displays username.
            show room               --- Displays unique code on which system is connected.
            show connectedIP        --- Displays server address.
                    [port: 5100]    --- port for flask server.
                                        http://address:port

            delete username         --- Removes username
            delete room             --- Removes room.
            delete fnet             --- Removes fnet.
            
            * No space in between username and room.
            * Make sure client and server connected on same network.
            * fnet is required for communication on multiple PCs.
            * fnet is essential for single device.
            
            """)

        os.system("cls")
        print("ChronoAlert Command-line Interface".center(60,"-"))
        print("Type '\help' to get help...")
        while True:

            inpt = input(">>>").lower()
            inpt = inpt.split(" ")
            while "" in inpt:
                inpt.remove("")
            try:
                if inpt[0] == "set":SetOp(inpt[1:])
                elif inpt[0] == "show":ShowOp(inpt[1])
                elif inpt[0] == "delete":SetOp(inpt[0:])
                elif inpt[0] == "\help":guide()
                else:none()
            except:
                none()