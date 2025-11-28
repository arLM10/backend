from flask import Flask, jsonify, request
from paste.httpheaders import category

tasks = []
task_id_counter = 1

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify ({
    'message': 'Welcome to Task Manager API',
    'status': 'running'
    })

@app.route('/hello')
def hello():
    return jsonify ({
    'message': 'Hello, World!'})

@app.route('/api/info')
def info():
    return jsonify ({
    'app_name': 'Task Manager',
    'version': '1.0',
    'author': 'omsekhar'
    })

@app.route('/api/status')
def status():
    return jsonify ({
    'database': 'connected',
    'server': 'running',
    'uptime': '24 hours'
    })

@app.route('/api/greet')
def greet():
    name = request.args.get('name','Guest')

    return jsonify ({
    'message': f'Hello, {name}!',
    'greeting': 'Welcome to Task Manager'
    })

@app.route('/api/add')
def add():
    a = request.args.get('a',1)
    b = request.args.get('b',2)
    a = int(a)
    b = int(b)
    c = a+b
    return jsonify ({'result':c,
                     'operation':'addition'})


@app.route('/api/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()

    new_task = {
        'id': task_id_counter,
        'title': data.get('title'),
        'description': data.get('description'),
        'completed': False
    }

    tasks.append(new_task)
    task_id_counter += 1

    return jsonify(new_task), 201

@app.route('/api/tasks', methods=['GET'] )
def get_tasks():
    return jsonify({
        'tasks': tasks,
        'count': len(tasks)
    }), 200

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Find task with matching ID
    task = next((t for t in tasks if t['id'] == task_id), None)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify(task), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
