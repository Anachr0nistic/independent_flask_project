from flask import Flask, render_template, request, redirect, make_response
import sqlite3

c = sqlite3.connect('db/login.db', check_same_thread=False).cursor() # cursor
cc = sqlite3.connect('db/video.db', check_same_thread=False).cursor()

c.execute('''CREATE TABLE IF NOT EXISTS USERS(
                ID INTEGER PRIMARY KEY NOT NULL,
                USERNAME TEXT NOT NULL, 
                PASSWORD TEXT NOT NULL)''')

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")

@app.route("/videos")
def video():
    return render_template("partials/videos.html")

@app.route("/upload")
def upload():
    return render_template("/partials/upload.html")


@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/misc")
def misc():
    return render_template("misc.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        logged_in = False
        username = str(request.form.get("username"))
        password = str(request.form.get("password"))

        table = c.execute('''SELECT * FROM USERS''').fetchall()

        for i in range(len(table)):
            if table[i][1] == username and table[i][2] == password:
                print("logged in successfully")

                user_id = str(table[i][0])

                resp = make_response(redirect("/"))
                resp.set_cookie(username, user_id)

                table_name = f"user_videos_{user_id}"
        
                cc.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                    VIDEO_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    VIDEO TEXT NOT NULL)''')

                return resp
            
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        signup_name = str(request.form.get("signup_name"))
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        params = (signup_name, password1)

        table = c.execute('''SELECT * FROM USERS''').fetchall()
        print(len(table))

        for i in range(len(table)):
            print(table[i][1])
            if table[i][1] == signup_name:
                print("username taken")
                break
        else:
            if password1 == password2:
                 with sqlite3.connect('db/login.db', check_same_thread=False):
                    c.execute('''INSERT INTO USERS (ID, USERNAME, PASSWORD) VALUES (NULL, ?, ?)''', params)
                    return redirect("/login")
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True, port="8081")