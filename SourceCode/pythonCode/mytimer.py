from pynput import keyboard 
import time
import threading
import os
import win32api
import psutil
from plyer import notification

recent = time.time()
older_time = time.time()
myapp = "Reminder"
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

def shutdown():
    #Shut-down windows operating system.
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


def notify():
    #These are some of my reminders. You can also add your custom reminders.
    # You can make your custom reminder by adding a notification function
    # And adding Thread I did in line near 122(Look by yourself.)
    # Do not forget to intialize the thread or else your function won't work.                               
    def water_notification():
        while True:
            time.sleep(3600)
            notification.notify(
                title  = "Time to Drink!!",
                message = "Drink some water to stay hydrated!",
                app_icon =  file_path+"\water_drink_bottle_icon.ico",
                timeout = 10,
                app_name = myapp
            )
            
    def exercise_notification():
        while True:
            time.sleep(5400)
            notification.notify(
                title = "Move yourself!!",
                message = "Exercise a little or go out for a nice walk. ^_^",
                app_icon =  file_path+"\walk_icon_151006.ico",
                timeout =10,
                app_name = myapp
            )
            
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
    notify1 = threading.Thread(target= water_notification)
    notify2 = threading.Thread(target=exercise_notification)
    notify3 = threading.Thread(target=rest_notification)
    #Start your threads to make them run, or else won't work.
    notify1.start()
    notify2.start()
    notify3.start()

def sysBattery():           
    #ShutDown the system when battery is lower than 7% and 
    #if charger is not plugged-in.
    #checks battery in every 10seconds.
    while(True):
        battery = psutil.sensors_battery()
        if battery.percent<=7 and battery.power_plugged == False:
            notification.notify(
                title = "Charging below 7%",
                message = "Plug-in the charger. Switching-Off in 2 minutes.",
                app_icon = file_path+"\com_94378.ico",
                timeout = 15,
                app_name = myapp
            )
            time.sleep(120)
            if psutil.sensors_battery().power_plugged == False:
                shutdown()
        time.sleep(10)

if __name__ == "__main__":
    notification.notify(
        title = "Reminder",
        message = "Application running in background.",
        app_icon = file_path+"\emoji_laughing_fill_icon_185681.ico" ,
        timeout = 10,
        app_name = myapp
    )
    t1 = threading.Thread(target=keys)
    t2 = threading.Thread(target=notify)
    t3 = threading.Thread(target =check_user)
    t4 = threading.Thread(target=sysBattery)
    t5 = threading.Thread(target=cursor)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()