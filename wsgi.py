#!/usr/bin/env python3
""" runner """
from phi import create_app, app

if __name__ == '__main__':
    socketio = create_app()
    socketio.run(app)
