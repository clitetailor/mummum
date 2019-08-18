from flask import Blueprint, redirect, session, request, render_template
from server.db import Users
from datetime import datetime
from server.utils.auth import authenticate

router = Blueprint('login', __name__, url_prefix='/api')


@router.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if "Wrong" not in authenticate("", username, password):
        session['username'] = username
        session['ip'] = request.remote_addr
        Users.insert(
            {"username": username, "ip": request.remote_addr, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
        return redirect('/')
    else:
        return render_template('login.html', msg="Login fail")
