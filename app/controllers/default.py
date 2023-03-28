from app import app
import mysql.connector
from flask import make_response, jsonify, request

app.config['JSON_SORT_KEYS'] = False

mysql = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='toor',
    database='tasks'
)

@app.route('/', methods=['GET'])
def index():
    return '<h1>Inicio da aplicação flask!!</h1>'


# List Tasks

@app.route('/tasks', methods=['GET'])
def listTasks():

    my_cursor = mysql.cursor()
    my_cursor.execute('SELECT * FROM tasks')
    tasks = my_cursor.fetchall()
    print(tasks)

    return make_response(
        jsonify(
            messagem='Task List',
            data=tasks
        )
    ), 200


# Add New Task

@app.route('/newtask', methods=['POST'])
def newTask():
    task = request.json
    print(task)

    my_cursor = mysql.cursor()

    find = f"SELECT * FROM tasks WHERE (title='{task['title']}')"
    
    my_cursor.execute(find)
    tasks = my_cursor.fetchall()

    if tasks:
        return {'Message': 'Sorry, task already added!'}, 409  

    else:    
        insert = f"INSERT INTO tasks (owner, title, status) VALUES ('{task['owner']}', '{task['title']}', '{task['status']}')"

        my_cursor.execute(insert)
        mysql.commit()

        return make_response(
            jsonify(
                messagem='Task Added!',
                data=task
            )
        ), 201


# Find Task By Owner

@app.route('/search/<owner>', methods=['GET'])
def searchtaskbyOwner(owner):

    task_owner = owner
    my_cursor = mysql.cursor()

    find = f"SELECT * FROM tasks WHERE (owner='{task_owner}')"
    
    my_cursor.execute(find)
    tasks = my_cursor.fetchall()

    if tasks:
        return make_response(
        jsonify(
            messagem='Task by owner!',
            data=tasks
            )
        )

    else:
        return {'Message': 'Sorry,owner not found'}, 404    
    
    
# Edit Tasks

@app.route('/edit', methods=['PUT'])
def editTask():
    task = request.json

    my_cursor = mysql.cursor()

    find = f"SELECT * FROM tasks WHERE (title='{task['title']}')"

    my_cursor.execute(find)
    tasks = my_cursor.fetchall()

    print(tasks)
    if tasks:
        update = f"UPDATE tasks SET status='{task['status']}' WHERE title=('{task['title']}')"
        my_cursor.execute(update)
        mysql.commit()

        my_cursor.execute(find)
        tasks = my_cursor.fetchall()

        return make_response(
            jsonify(
                messagem='Task Altered!',
                data=tasks
            )
        )

    else:
        return {'Message': 'Sorry, task not found!'}, 404
    


# Delete Tasks

@app.route('/delete/<title>', methods=['DELETE'])
def deleteTask(title):
    task_title = title
    my_cursor = mysql.cursor()

    find = f"SELECT * FROM tasks WHERE (title='{task_title}')"
    
    my_cursor.execute(find)
    tasks = my_cursor.fetchall()

    if tasks:
        
        delete = f"DELETE FROM tasks WHERE (title='{task_title}')"
        my_cursor.execute(delete)
        mysql.commit()

        return {'Message': 'Task deleted!'}, 200

    else:
        return {'Message': 'Sorry, task not found!'}, 404
