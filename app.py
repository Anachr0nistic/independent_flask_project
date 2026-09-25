from flask import Flask, render_template, request, redirect
import sqlite3

conn = sqlite3.connect('db/login.db', check_same_thread=False)
c = conn.cursor() # cursor

c.execute('''CREATE TABLE IF NOT EXISTS USERS(
                ID INTEGER PRIMARY KEY NOT NULL,
                USERNAME TEXT NOT NULL, 
                PASSWORD TEXT NOT NULL)''')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        logged_in = False
        username = str(request.form.get("username"))
        password = str(request.form.get("password"))
        print(username, password)
        table = c.execute('''SELECT * FROM USERS''').fetchall()
        #print(c.execute('''SELECT * FROM USERS''').fetchall())
        print(table, len(table))
        for i in range(len(table)):
            if table[i][1] == username and table[i][2] == password:
                print("logged in successfully")
                return redirect("/")
    return render_template("login.html")
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        signup_name = request.form.get("signup_name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        params = (signup_name, password1)
        table = c.execute('''SELECT * FROM USERS''').fetchall()
        print(len(table))
        for i in range(len(table)):
            if table[i][1] == signup_name:
                break
            else:
                if password1 == password2:
                    with conn:
                        c.execute('''INSERT INTO USERS (ID, USERNAME, PASSWORD) VALUES (NULL, ?, ?)''', params)
                        break
    return render_template("signup.html")
if __name__ == "__main__":
    app.run(debug=True, port="8081")