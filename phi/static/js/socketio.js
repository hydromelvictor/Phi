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
