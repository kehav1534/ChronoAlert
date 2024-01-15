from flask import Flask, render_template, request, redirect, url_for, jsonify
import os, random, string
import sqlite3
from flask_socketio import SocketIO
from time import sleep
#Get the IP4 address of the connnected network
import socket
h_name = socket.gethostname()
IP_addres = socket.gethostbyname(h_name)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='http://'+IP_addres+':5300')

app.config["SECRET_KEY"] = os.urandom(16)  # Set a secret key for security
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True  # Require HTTPS for the session cookie
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent client-side JavaScript access to the session cookie

sessions = {}
# A dictionary to store user credentials (username: password)
user_credentials = {}

def generate_random_string(length = 4): #Call function to add code in database during signup.
    exist = True
    val = ""
    while exist:
        alphabet = string.ascii_letters
        for n in range(2):
            val += (''.join(random.choice(alphabet) for i in range(length))+ "-"+ str(random.randint(1001, 9999))).upper()
            if n==0:val+="-"
        mycursor = sqlite3.connect('C:/ChronoRemote/File/db/users.db').cursor()
        mycursor.execute("SELECT room FROM userprofile WHERE room = ?;", (val, ))        #change table/column or create new table to store
        data = mycursor.fetchone()
        if data:
            pass
        else:
            return val


def login(email, password, typ=True):
    mycursor = sqlite3.connect('C:/ChronoRemote/File/db/users.db').cursor()
    mycursor.execute('SELECT * from userprofile where email =?;', (email,) )
    data = mycursor.fetchone()
    if not typ and data:
        return True
    if data is None or not typ:
        return False
    user_credentials = {data[0] : data[2]}
    data = None
    if email in user_credentials and user_credentials[email] == password:
        return True
    return False

@app.route("/", methods=["GET", "POST"])
def index():
    if "email" in sessions:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if login(email, password):
            sessions["email"] = email
            return redirect('/dashboard')
        else:
            return render_template("login.html", message = 'Invalid User or password', email=email, password=password)

    return render_template("login.html")

@app.route('/CheckUsername', methods=['POST'])
def Check_Username():
    email:str = request.json['email']
    mycursor = sqlite3.connect('C:/ChronoRemote/File/db/users.db').cursor()
    data = mycursor.fetchall()
    for tpl in data:
        if tpl[0]==email:
            return jsonify({'exists': True})
    return jsonify({'exists': False})

@app.route('/Signup')
def Signup():
    return render_template('signup.html')

@app.route('/SignupData', methods=['POST'])
def SignupData():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        if not login(email=email, password=password, typ=False):
            room = generate_random_string()
            mydb = sqlite3.connect('C:/ChronoRemote/File/db/users.db')
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO userprofile values( ?, ? , ? , ? );", (email, username, password, room))
            mydb.commit()
            if login(email, password):
                sessions["email"] = email
                return redirect(url_for("dashboard"))
        else:
            return render_template('signup.html', email=email, username=username, message="Email already exist.")

@app.route("/dashboard")
def dashboard():
    if "email" in sessions:
        mycursor = sqlite3.connect('C:/ChronoRemote/File/db/users.db').cursor()
        mycursor.execute(f'SELECT username, room from userprofile where email =?;', (sessions['email'],) )
        data = mycursor.fetchone()
        checkcursor = sqlite3.connect('C:/ChronoRemote/File/db/connected.db').cursor()
        checkcursor.execute("SELECT username FROM connected WHERE room = ?;", (data[1], ))
        users = checkcursor.fetchall()
        chkbox= ""
        for user in users:
            if user[0]!="WebApp":
                chkbox+= f'<input type="checkbox" name="connecteduser" value="{user[0]}" class="other-checkbox"></label> {user[0]}</label><br><hr>'
        return render_template("newHomepage.html", email=sessions['email'], username=data[0], room = data[1], ip=IP_addres, chkbox=chkbox, count=len(users))
    return redirect(url_for("index"))

@app.route("/logout", methods=['POST'])
def logout():
    sessions.clear()
    return redirect(url_for("index"))
    

if __name__ == "__main__":
    while True:
        IP_addres = socket.gethostbyname(h_name)
        if IP_addres != "127.0.0.0":
            app.run(host=IP_addres, port=5100, debug=True)
        else:
            sleep(5)