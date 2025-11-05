from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", 
                       [("admin", "admin123"), ("Jan", "Heslo"), ("Alice", "Alice123")])
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template("welcome.html", username=user[1])
        else:
            error = "Nesprávné údaje"

    return render_template("index.html", error=error)

if __name__ == "__main__":
    app.run(debug=True)
