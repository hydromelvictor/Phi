$(document).ready(function() {
    let socketio = io.connect('http://127.0.0.1:5000');
    socketio.on('connect', () => {
        joinRoom(room);
    });

    socketio.on('disconnect', () => {
        leaveRoom(room);
    })

    socketio.on('message', data => {
        $('#chatt').append(
            '<li class="card container">\
                <span class="card-title">\
                   <span>' + data.username + ' - ' + data.tm + '</span>\
                </span>\
                <span>' + data.msg + '</span><br>\
            </li>'
        );
    });

    $('#btn').on('click', () => {
        let entries = $('#entries').val();
        if (entries.length) {
            socketio.send({'msg': entries, 'username': username, 'room': room});
        }
        $('#entries').val('');
        $('#entries').focus();
    })

    function leaveRoom(room) {
        socketio.emit('leave', {'username': username, 'room': room});
    }

    function joinRoom(room) {
        socketio.emit('join', {'username': username, 'room': room});
    }

});

/*
document.addEventListener('DOMContentLoaded', () => {
    let socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        socket.send("connected");
    });

    socket.on('message', data => {
        const li = document.createElement('li');
        const divm = document.createElement('div');
        const spantime = document.createElement('span')
        spantime.innerHTML = data.tm;
        const div = document.createElement('div');
        div.innerHTML = data.msg;
        divm.appendChild(spantime);
        li.appendChild(divm);
        li.appendChild(div)
        document.querySelector('#chatt').append(li);

    });

    document.querySelector('#btn').onclick = () => {
        socket.send({ 'msg': document.querySelector('#entries').value, 'username': username, 'room': room });
        document.querySelector('#entries').value = '';
    }

    document.querySelector('.lik').forEach(li => {
        li.onclick = () => {
           let newroom = li.querySelector('.room').value;
           if (newroom == room) {
            printMsg(msg);
           } else {
            leaveRoom(room);
            joinRoom(newroom);
            room = newroom;
           }
        }
    });

    function leaveRoom(room) {
      socket.emit('leave', {'username': username, 'room': room});
    }

    function joinRoom(room) {
      socket.emit('join', {'username': username, 'room': room});
      document.querySelector('#entries').innerHTML = ''; 
    }

    function printMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#entries').append(p);
    }
});
*/