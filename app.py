from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, emit
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='template')
app.config["MONGO_URI"] = "mongodb://localhost:27017/chat"
app.secret_key = 'your_secret_key'

mongo = PyMongo(app)
socketio = SocketIO(app, cors_allowed_origins='*')  # Enable CORS

connected_users = {}


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error variable
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            error = "Invalid username or password."  # Set error message

    return render_template('login.html', error=error)  # Pass error to the template


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check for strong password
        if len(password) < 8 or not any(c.islower() for c in password) or \
                not any(c.isupper() for c in password) or not any(c.isdigit() for c in password) or \
                not any(c in '!@#$%^&*()_+' for c in password):
            return "Password must be at least 8 characters long and include uppercase, lowercase, numbers, and special characters.", 400

        # Check if the username already exists
        if mongo.db.users.find_one({'username': username}):
            return "Username already exists", 400

        # Insert new user
        mongo.db.users.insert_one({
            'username': username,
            'password': generate_password_hash(password)
        })
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'])


@socketio.on('connect')
def handle_connect():
    username = session.get('username')
    connected_users[request.sid] = username
    join_room(username)
    emit('user_list', list(connected_users.values()), broadcast=True)


@socketio.on('send_message')
def handle_message(data):
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']

    mongo.db.messages.insert_one({
        'sender': sender,
        'recipient': recipient,
        'message': message
    })

    socketio.emit('chat message', {
        'sender': sender,
        'recipient': recipient,
        'message': message
    }, room=recipient)


@socketio.on('disconnect')
def handle_disconnect():
    username = connected_users.pop(request.sid, None)
    if username:
        emit('user_list', list(connected_users.values()), broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)  # For development
