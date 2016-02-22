#!/usr/bin/env python

from eat.factory import create_app
from flask_script import Manager, Server

app = create_app()

manager = Manager(app)

manager.add_command("runserver", Server(
        use_debugger=True,
        use_reloader=True,
        host='0.0.0.0')
                    )

if __name__ == "__main__":
    manager.run()
