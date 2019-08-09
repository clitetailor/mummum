# -*- coding: utf-8 -*-

from flask_script  import Manager
from app import create_app
from flask import request, abort, session
from werkzeug.contrib.fixers import ProxyFix

app = create_app()
manager = Manager(app)
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.before_request
def test():
    if session.has_key('ip'):
        if session['ip'] != request.remote_addr:
            abort(403)
    if "favicon.ico" in request.full_path:
        abort(200)

@manager.command
def runserver():
    """Run in local machine."""
    app.run(host='127.0.0.1', port=9090,debug = True)

if __name__ == "__main__":
    manager.run(default_command='runserver')
