#Source code by:- Keshav Maheshwari

#Backend Script
import sys
from pynput import keyboard 
import time
import threading
import os
import win32api
import psutil
from plyer import notification
import json

recent = time.time()
older_time = time.time()
myapp = "ChronoAlert"
file_path = 'C:\Program Files\ChronoAlert\icon'    #File path location of Shut_Down Timer Folder.

def keys():
    def on_key_release(key): #what to do on key-release
        global recent, older_time
        recent = time.time()
        older_time  = time.time()
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
            recent = time.time()
            older_time = time.time()
            savedpos = curpos  
        time.sleep(0.5)


#Reads the notification.json get the notification messages.
def readJson(path="notification.json", data=None):
    
    with open(path, "r+") as file:
        notifi_data = json.load(file)
        return notifi_data

notification_list = readJson()

def notify():
    #These are some of my reminders. You can also add your custom reminders.
    # You can make your custom reminder by adding a it into above list
    #                               
    def notifications(n):
        while True:
            time.sleep(notification_list[n]["sleep"])
            notification.notify(
                title  = notification_list[n]["title"],
                message = notification_list[n]["message"],
                app_icon =  file_path+"\\"+notification_list[n]["app_icon"],
                timeout = notification_list[n]["timeout"],
                app_name = myapp
            )
            
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
            os.system(r'rundll32.exe powrprof.dll,SetSuspendState Hibernate')



    #Made threads of notifications so that they keep running in parallel-like fasion.
    for mesg in range(len(notification_list)):
        notify1 = threading.Thread(target= notifications, args=(mesg, ))
        notify1.start()
    notify3 = threading.Thread(target=rest_notification)
    #Start your threads to make them run, or else won't work.
    
    notify3.start()


#Shut-down windows operating system.
def shutdown():
    os.system('shutdown -s -t 0')


def check_user():                   
    #Checks whether the user has made any movement through keyboard or mouse.
    while(True):
        global recent, older_time
        recent = time.time()
        not_moved = recent - older_time
        if(not_moved > 3000 and not_moved<3008):
            notification.notify(
                title = "Are you there!?",
                message= "You haven't touched your device for a while. Shutting down your device in 10 minutes.",
                app_icon = file_path+"\com_94378.ico",
                app_name = myapp,
                timeout  =10
                )
            time.sleep(11)
        elif(not_moved > 3540 and not_moved< 3550):       
            ##Notify the user 1 minute before shutting down.
            notification.notify(
                title = "Shutting Down",
                message = "You don't seem to be using the device. Shutting Down in a minute.",
                app_icon = file_path+"\com_94378.ico",
                timeout =10,
                app_name = myapp
            )
            time.sleep(11)
        elif(not_moved > 3600):             
            #Shuts Down the device after an hour.
            shutdown()
        time.sleep(1)

def sysBattery():           
    #ShutDown the system when battery is lower than 7% and 
    #if charger is not plugged-in.
    #checks battery in every 10seconds.
    while(True):
        battery = psutil.sensors_battery()
        if battery.percent<=7 and battery.power_plugged == False:
            notification.notify(
                title = "Charging below 7%",
                message = "Plug-in the charger. Switching-Off at 5%",
                app_icon = file_path+"\com_94378.ico",
                timeout = 15,
                app_name = myapp
            )
            break
    while(True):                                                                            #Need to Tested----------------------------<<<<<<<<<<<<<
        if psutil.sensors_battery().power_plugged == False and battery.percent<=5:
                shutdown()
        time.sleep(10)


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
        func_list = (keys, notify, check_user, sysBattery, cursor)
        for func in func_list:
                thread = threading.Thread(target=func)
                thread.start()

    else:
        os.system("C:/Users/Keshav^ Maheshwari/Desktop/ChronoAlert_/Reminder_vbs.vbs")


#

#   ^_____^
#   (* o */)/
# /{      |
#  \  _._ }
#   \/  \/
