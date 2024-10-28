const socket = io();

function sendMessage() {
    const messageInput = document.getElementById('message');
    const message = messageInput.value;
    socket.emit('send_message', message);
    messageInput.value = '';
}

socket.on('receive_message', function(message) {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += `<p>${message}</p>`;
});
