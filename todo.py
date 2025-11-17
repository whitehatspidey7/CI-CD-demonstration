from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# Initialize the database (run once)
with app.app_context():
    db.create_all()

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>To-Do List</title>
</head>
<body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:40px;">

    <div style="max-width:600px; margin:auto; background:white; padding:30px; border-radius:12px; 
                box-shadow:0 4px 15px rgba(0,0,0,0.1);">

        <h1 style="text-align:center; color:#333; margin-bottom:25px;">📝 To-Do List</h1>

        <form action="{{ url_for('add') }}" method="POST" 
              style="display:flex; gap:10px; margin-bottom:25px;">
            <input type="text" name="content" placeholder="Add new task" required
                   style="flex:1; padding:12px; border:1px solid #ccc; border-radius:8px; font-size:15px;">
            <input type="submit" value="Add"
                   style="background:#007bff; color:white; border:none; padding:12px 20px; 
                          border-radius:8px; cursor:pointer; font-size:15px;">
        </form>

        <h2 style="color:#444; border-bottom:2px solid #ddd; padding-bottom:5px;">Incomplete Tasks</h2>
        <ul style="list-style:none; padding:0;">
        {% for task in incomplete %}
            <li style="background:#fff3cd; padding:12px 15px; margin:8px 0; border-radius:10px; 
                       display:flex; justify-content:space-between; align-items:center;">

                <span style="font-size:16px;">{{ task.content }}</span>

                <span>
                    <a href="{{ url_for('complete', task_id=task.id) }}"
                       style="background:#28a745; color:white; padding:6px 12px; border-radius:6px; 
                              text-decoration:none; margin-right:5px;">Complete</a>

                    <a href="{{ url_for('delete', task_id=task.id) }}"
                       style="background:#dc3545; color:white; padding:6px 12px; border-radius:6px; 
                              text-decoration:none;">Delete</a>
                </span>
            </li>
        {% endfor %}
        </ul>

        <h2 style="color:#444; border-bottom:2px solid #ddd; padding-bottom:5px; margin-top:30px;">Completed Tasks</h2>
        <ul style="list-style:none; padding:0;">
        {% for task in complete %}
            <li style="background:#d4edda; padding:12px 15px; margin:8px 0; border-radius:10px; 
                       display:flex; justify-content:space-between; align-items:center;">

                <span style="font-size:16px; text-decoration:line-through; color:#555;">
                    {{ task.content }}
                </span>

                <a href="{{ url_for('delete', task_id=task.id) }}"
                   style="background:#dc3545; color:white; padding:6px 12px; 
                          border-radius:6px; text-decoration:none;">Delete</a>
            </li>
        {% endfor %}
        </ul>

    </div>

</body>
</html>
'''

@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    return render_template_string(TEMPLATE, incomplete=incomplete, complete=complete)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    if not content:
        return redirect(url_for('index'))
    task = Todo(content=content)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = Todo.query.get_or_404(task_id)
    task.complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
