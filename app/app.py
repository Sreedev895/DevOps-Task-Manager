from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "tasks.db"))


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DevOps Task Manager</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f1f5f9;
    color: #1e293b;
}
header {
    background: linear-gradient(120deg, #0f172a, #1e40af);
    color: white;
    padding: 30px 20px;
}
.header-content, .container { max-width: 900px; margin: auto; }
header h1 { margin: 0 0 8px; font-size: 30px; }
header p { margin: 0; color: #cbd5e1; }
.container { padding: 25px 18px; }
.stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-bottom: 22px;
}
.stat {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 3px 12px #00000008;
}
.stat h2 { margin: 0; font-size: 28px; }
.stat p { color: #64748b; margin: 8px 0 0; }
.add-form {
    display: flex;
    gap: 10px;
    background: white;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 22px;
}
input[type=text] {
    flex: 1;
    min-width: 0;
    padding: 12px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 16px;
}
button {
    border: none;
    border-radius: 8px;
    padding: 11px 15px;
    cursor: pointer;
    font-weight: bold;
}
.add-btn { background: #2563eb; color: white; }
.task-list { display: grid; gap: 10px; }
.task {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    background: white;
    border-radius: 10px;
    padding: 16px;
}
.task-title { flex: 1; overflow-wrap: anywhere; }
.completed { color: #94a3b8; text-decoration: line-through; }
.actions { display: flex; gap: 8px; }
.done-btn { background: #dcfce7; color: #166534; }
.undo-btn { background: #e0e7ff; color: #3730a3; }
.delete-btn { background: #fee2e2; color: #991b1b; }
.empty {
    background: white; text-align: center; color: #64748b;
    padding: 35px; border-radius: 12px;
}
footer { text-align: center; color: #64748b; padding: 25px; font-size: 13px; }
@media(max-width:600px) {
    .stats { gap: 8px; }
    .stat { padding: 13px; }
    .stat h2 { font-size: 23px; }
    .add-form { flex-direction: column; }
    .task { align-items: flex-start; flex-direction: column; }
    .actions { width: 100%; }
    .actions form { flex: 1; }
    .actions button { width: 100%; }
}
</style>
</head>
<body>
<header>
    <div class="header-content">
        <h1>DevOps Task Manager</h1>
        <p>Organize your work. Track your progress. Get things done.</p>
    </div>
</header>

<main class="container">
    <section class="stats">
        <div class="stat"><h2>{{ total }}</h2><p>Total Tasks</p></div>
        <div class="stat"><h2>{{ pending }}</h2><p>Pending</p></div>
        <div class="stat"><h2>{{ completed }}</h2><p>Completed</p></div>
    </section>

    <form class="add-form" action="/add" method="POST">
        <input type="text" name="title" placeholder="What needs to be done?" maxlength="150" required>
        <button class="add-btn" type="submit">+ Add Task</button>
    </form>

    <section class="task-list">
    {% if tasks %}
        {% for task in tasks %}
        <article class="task">
            <div class="task-title {% if task.completed %}completed{% endif %}">
                {{ task.title }}
            </div>
            <div class="actions">
                <form action="/toggle/{{ task.id }}" method="POST">
                    <button class="{% if task.completed %}undo-btn{% else %}done-btn{% endif %}" type="submit">
                        {% if task.completed %}Undo{% else %}Complete{% endif %}
                    </button>
                </form>
                <form action="/delete/{{ task.id }}" method="POST">
                    <button class="delete-btn" type="submit">Delete</button>
                </form>
            </div>
        </article>
        {% endfor %}
    {% else %}
        <div class="empty">No tasks yet. Add your first task above!</div>
    {% endif %}
    </section>
</main>
<footer>Built with Flask · SQLite · Docker · Jenkins · AWS EC2</footer>
</body>
</html>
"""


@app.route("/")
def home():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()

    total = len(tasks)
    completed = sum(task["completed"] for task in tasks)
    pending = total - completed

    return render_template_string(
        HTML,
        tasks=tasks,
        total=total,
        pending=pending,
        completed=completed
    )


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()

    if title:
        conn = get_db()
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()

    return redirect(url_for("home"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET completed = CASE WHEN completed = 0 THEN 1 ELSE 0 END WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
