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

@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/signup")
def signup():
    signup_name = request.form.get("signup_name")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    if password1 == password2:
        c.execute("INSERT INTO USERS (USERNAME, PASSWORD) VALUES (signup_name, password1)")

    return render_template("signup.html")
@app.route("/test")
def test():
    return render_template("test.html")
if __name__ == "__main__":
    app.run(debug=True, port="8081")