from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        priority TEXT,
                        status TEXT DEFAULT 'A Fazer'
                    )''')
    conn.commit()
    conn.close()

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, priority, status) VALUES (?, ?, ?, ?)",
                   (data["title"], data.get("description"), data.get("priority"), data.get("status", "A Fazer")))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task criada com sucesso"}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title=?, description=?, priority=?, status=? WHERE id=?",
                   (data["title"], data.get("description"), data.get("priority"), data.get("status"), task_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task atualizada com sucesso"})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task excluída com sucesso"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
