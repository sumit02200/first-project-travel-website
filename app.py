from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey123"

# Create DB
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

def get_db():
    return sqlite3.connect("users.db")

@app.route("/")
def home():
    return redirect("/signin")

# SIGN UP
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        try:
            db = get_db()
            db.execute("INSERT INTO users(username,email,password) VALUES (?,?,?)",
                       (username,email,password))
            db.commit()
            db.close()
            return redirect("/signin")
        except:
            return "User already exists ❌"

    return render_template("signup.html")

# SIGN IN
@app.route("/signin", methods=["GET","POST"])
def signin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=?",(username,)).fetchone()
        db.close()

        if user and check_password_hash(user[3], password):
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid Login ❌"

    return render_template("signin.html")
