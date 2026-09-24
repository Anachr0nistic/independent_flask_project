from flask import Flask, render_template, request
import sqlite3

conn = sqlite3.connect('db/login.db', check_same_thread=False)
c = conn.cursor() # cursor

c.execute('''CREATE TABLE IF NOT EXISTS USERS(
                ID INTEGER PRIMARY KEY NOT NULL,
                USERNAME TEXT NOT NULL, 
                PASSWORD TEXT NOT NULL)''')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    username = str(request.form.get("username"))
    password = str(request.form.get("password"))
    print(username, password)
    print(c.execute('''SELECT * FROM USERS WHERE USERNAME = (?) ''', (username,)).fetchall())
    with conn:
        if username == c.execute('''SELECT * FROM USERS WHERE USERNAME = (?) ''', (username,)).fetchall():
            print("yippie")
        else:
            print("FUCK")

        #c.execute('''SELECT * FROM USERS WHERE PASSWORD = (?) ''', (password)).fetchall()
    return render_template("login.html")
@app.route("/signup", methods=["POST"])
def signup():
    signup_name = request.form.get("signup_name")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    params = (signup_name, password1)
    if password1 == password2:
        with conn:
            c.execute("INSERT INTO USERS (ID, USERNAME, PASSWORD) VALUES (NULL, ?, ?)", params)
    elif password1 != password2:
        pass #GØR MÅSKE, SÅ EN SIGN-UP FEJL BESKED POPPER OP HVIS JEG HAR TID


    return render_template("signup.html")
if __name__ == "__main__":
    app.run(debug=True, port="8082")