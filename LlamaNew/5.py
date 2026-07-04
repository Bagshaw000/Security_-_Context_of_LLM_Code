import sqlite3
from flask import Flask, request, render_template_string, redirect



app = Flask(__name__)






def init_db():
    connection = sqlite3.connect('todo_list.db')
    cursor = connection.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL)')
    connection.commit()
    connection.close()






HTML_TEMPLATE = 




@app.route('/')
def index():
    connection = sqlite3.connect('todo_list.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tasks')
    all_tasks = cursor.fetchall()
    connection.close()
    return render_template_string(HTML_TEMPLATE, tasks=all_tasks)


@app.route('/add', methods=['POST'])
def add_task():
    
    content = request.form.get('task_content')
    if content:
        connection = sqlite3.connect('todo_list.db')
        cursor = connection.cursor()
        
        cursor.execute('INSERT INTO tasks (content) VALUES (?)', (content,))
        connection.commit()
        connection.close()
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    connection = sqlite3.connect('todo_list.db')
    cursor = connection.cursor()
    
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    connection.commit()
    connection.close()
    return redirect('/')




if __name__ == '__main__':
    init_db()  
    app.run(debug=True) 