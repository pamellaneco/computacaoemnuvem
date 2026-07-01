import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            descricao TEXT NOT NULL,
            concluida BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        descricao = request.form["descricao"]
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO tarefas (descricao) VALUES (%s)", (descricao,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, descricao, concluida FROM tarefas ORDER BY id")
    tarefas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", tarefas=tarefas)

@app.route("/concluir/<int:id>")
def concluir(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE tarefas SET concluida = TRUE WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

with app.app_context():
    try:
        init_db()
    except Exception:
        pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)