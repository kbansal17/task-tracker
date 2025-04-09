from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secretkey"

# In-memory user store
users = {"admin": "admin123"}
tasks = {}  # { username: [ {title, desc, time, done}, ... ] }

# 15 Suggestions
suggestions = [
    "Go for a walk", "Drink water", "Meditate", "Read a book", "Call a friend",
    "Organize your desk", "Stretch", "Review goals", "Eat fruits", "Journal your day",
    "Practice breathing", "Learn a new word", "Limit screen time", "Compliment someone", "Clean your inbox"
]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        if uname in users and users[uname] == pword:
            session['username'] = uname
            if uname not in tasks:
                tasks[uname] = []
            return redirect('/index')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/')
    user_tasks = tasks[session['username']]
    return render_template('index.html', tasks=user_tasks, suggestions=suggestions)

@app.route('/add', methods=['POST'])
def add():
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    title = request.form.get('title', '').strip()
    desc = request.form.get('description', '').strip()
    suggestion = request.form.get('suggestion')

    if not title and suggestion:
        title = suggestion

    if not title:
        title = "-"
    if not desc:
        desc = "-"

    new_task = {
        "title": title,
        "desc": desc,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "done": False
    }

    tasks[username].append(new_task)
    return redirect('/index')

@app.route('/complete/<int:tid>')
def complete(tid):
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    if 0 <= tid < len(tasks[username]):
        tasks[username][tid]["done"] = True
    return redirect('/index')

@app.route('/delete/<int:tid>')
def delete(tid):
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    if 0 <= tid < len(tasks[username]):
        tasks[username].pop(tid)
    return redirect('/index')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)
