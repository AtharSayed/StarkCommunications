from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, emit
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='template')
app.config["MONGO_URI"] = "mongodb://localhost:27017/chat"
app.secret_key = 'your_secret_key'

mongo = PyMongo(app)
socketio = SocketIO(app, cors_allowed_origins='*')  # Enable CORS for SocketIO connections

connected_users = {}

# Route to redirect to the login page
@app.route('/')
def index():
    return redirect(url_for('login'))

# Route for logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error variable
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and password matches
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username  # Store username in session
            return redirect(url_for('chat'))  # Redirect to chat page
        else:
            error = "Invalid username or password."  # Set error message

    return render_template('login.html', error=error)  # Pass error to the template

# Route for signing up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check for strong password criteria
        if len(password) < 8 or not any(c.islower() for c in password) or \
                not any(c.isupper() for c in password) or not any(c.isdigit() for c in password) or \
                not any(c in '!@#$%^&*()_+' for c in password):
            return "Password must be at least 8 characters long and include uppercase, lowercase, numbers, and special characters.", 400

        # Check if the username already exists
        if mongo.db.users.find_one({'username': username}):
            return "Username already exists", 400

        # Insert new user into the database
        mongo.db.users.insert_one({
            'username': username,
            'password': generate_password_hash(password)
        })
        return redirect(url_for('login'))  # Redirect to login page

    return render_template('signup.html')  # Render signup page

# Route for the chat page
@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    return render_template('chat.html', username=session['username'])  # Render chat page

# Handle new socket connection
@socketio.on('connect')
def handle_connect():
    username = session.get('username')
    if username:  # Ensure that the user is logged in
        connected_users[request.sid] = username  # Store the connection with SID (Session ID)
        join_room(username)  # Join the room based on the username
        print(f'{username} connected')  # Debugging message
        emit('user_list', list(connected_users.values()), broadcast=True)  # Send updated user list

# Handle receiving and sending chat messages
@socketio.on('send_message')
def handle_message(data):
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']

    # Save the message to MongoDB
    mongo.db.messages.insert_one({
        'sender': sender,
        'recipient': recipient,
        'message': message
    })
    print(f"Message from {sender} to {recipient}: {message}")  # Debugging message

    # Emit the message to the recipient's room (private messaging)
    socketio.emit('chat message', {
        'sender': sender,
        'recipient': recipient,
        'message': message
    }, room=recipient)

# Handle socket disconnection
@socketio.on('disconnect')
def handle_disconnect():
    username = connected_users.pop(request.sid, None)  # Remove user from the connected list
    if username:
        print(f'{username} disconnected')  # Debugging message
        emit('user_list', list(connected_users.values()), broadcast=True)  # Update user list for everyone

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)  # Run the app with SocketIO

