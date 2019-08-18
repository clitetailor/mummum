from flask import Blueprint, Markup, session, redirect, request, render_template
from datetime import datetime
from server.db import Payed, get_data


router = Blueprint("index", __name__)

@router.route('/', methods=['GET'])
def index():
    if "username" not in session:
        return redirect("/login")

    msg = ''
    if "msg" in session:
        msg = session['msg']
        session.pop('msg', None)

    date = ''
    if request.remote_addr == "192.168.6.111":
        try:
            date = request.args.get('date')
        except:
            pass

    data = get_data(date)

    week = datetime.now().strftime("%U")
    guys1 = []

    for i in range(1, 4):
        ll = Payed.find({"week": str(int(week) - i), "payed": 0})
        if ll is None:
            break
        for l in ll:
            guys1.append(l)
    payed = True

    for guy in guys1:
        if guy['name'] == session['username']:
            payed = False
            break

    return render_template('index.html', msg=Markup(msg), image_list=data, payed=payed)
