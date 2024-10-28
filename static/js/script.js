const socket = io.connect('http://localhost:5000');

// Function to send a message
function sendMessage() {
    const recipient = document.getElementById('recipient').value;
    const message = document.getElementById('message').value;

    socket.emit('send_message', { sender: username, recipient, message });
    document.getElementById('message').value = ''; // Clear the input field
}

// Listen for chat messages
socket.on('chat message', function(data) {
    const messageElement = document.createElement('div');
    messageElement.textContent = `${data.sender}: ${data.message}`;
    document.getElementById('messages').appendChild(messageElement);
});

// Listen for updated user list
socket.on('user_list', function(users) {
    const userList = document.getElementById('userList');
    userList.innerHTML = ''; // Clear existing users
    users.forEach(user => {
        const li = document.createElement('li');
        li.textContent = user;
        userList.appendChild(li);
    });
});
