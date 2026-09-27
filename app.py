from flask import Flask, render_template, request, redirect, make_response
import sqlite3
import os

# Opret forbindelser og cursors rigtigt
db_login = sqlite3.connect('db/login.db', check_same_thread=False)
c = db_login.cursor()

db_video = sqlite3.connect('db/video.db', check_same_thread=False)
cc = db_video.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS USERS(
                ID INTEGER PRIMARY KEY NOT NULL,
                USERNAME TEXT NOT NULL, 
                PASSWORD TEXT NOT NULL)''')
db_login.commit()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")

@app.route("/videos", methods=["POST","GET"])
def video():
    user_id = request.cookies.get("session_user_id")
    if not user_id:
        return redirect("/login")

    table_name = f"user_videos_{user_id}"
    try:
            rows = cc.execute(f"SELECT VIDEO FROM {table_name}").fetchall()
            user_videos = []
            # laver vores tuple om til en liste
            for i in rows:
                filnavn = i[0]
                user_videos.append(filnavn)  # tilføjer filnavnet til lsitnen
                
    except sqlite3.OperationalError: # hvis ingen videoer eksisterer(altså hvis vi ikke kan append, da listen ikke eksisterer)
            user_videos = []
        
    return render_template("videos.html", videos=user_videos)

@app.route("/upload", methods=["POST","GET"])
def upload():
    if request.method == "POST":
        user_id = request.cookies.get('session_user_id')
        if not user_id:
            return redirect("/login")
        
        file = request.files.get('video_file')
        
        if file and file.filename != '':
            # gemmer filen i static/uploads
            file.save(os.path.join("static/uploads", file.filename))
            
            table_name = f"user_videos_{user_id}"
            cc.execute(f"INSERT INTO {table_name} (VIDEO) VALUES (?)", (file.filename,))
            db_video.commit() 
            
            return redirect("/videos")

    return render_template("upload.html")


@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/misc")
def misc():
    return render_template("misc.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = str(request.form.get("username"))
        password = str(request.form.get("password"))

        table = c.execute('''SELECT * FROM USERS''').fetchall()

        for i in range(len(table)):
            if table[i][1] == username and table[i][2] == password:
                print("logged in successfully")

                user_id = str(table[i][0])

                resp = make_response(redirect("/"))
                resp.set_cookie('session_user_id', user_id)

                table_name = f"user_videos_{user_id}"
        
                cc.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                    VIDEO_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    VIDEO TEXT NOT NULL)''')
                db_video.commit()

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

        for i in range(len(table)):
            if table[i][1] == signup_name:
                print("username taken")
        else:
            if password1 == password2:
                c.execute('''INSERT INTO USERS (ID, USERNAME, PASSWORD) VALUES (NULL, ?, ?)''', params)
                db_login.commit()
                return redirect("/login")
                
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True, port=8081)
