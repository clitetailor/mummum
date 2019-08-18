from flask import Blueprint, redirect, session, request, render_template
from server.db import Menu
from datetime import date
from server.utils.datetime import day_of_week

router = Blueprint('menu', __name__, url_prefix='/api')


@router.route('/menu/add', methods=["GET"])
def menu():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    if username != 'khuyenn':
        return "Hmm!"

    day = day_of_week(date.today())

    return render_template('menu/add.html', date=day)
