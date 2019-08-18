from flask import Blueprint, render_template, session, redirect
from server.utils.session import session_rocket

router = Blueprint('user', __name__)


@router.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@router.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/login')
