#!/usr/bin/env python3
""" runner """
import phi

if __name__ == '__main__':
    app = phi.create_app()
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
