#!/usr/bin/env python3
""" runner """
from phi import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()
