from flask import Flask, render_template
import sqlite3

conn = sqlite3.connect('db/login.db')
c = conn.cursor() # cursor

c.execute('''CREATE TABLE IF NOT EXISTS users(
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
if __name__ == "__main__":
    app.run(debug=True, port="8081")