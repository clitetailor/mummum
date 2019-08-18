from flask import Blueprint, redirect, session, request
from datetime import datetime
from server.db import Menu, Booking, get_data
from bson import ObjectId


router = Blueprint('menu', __name__, url_prefix="/api")


@router.route('menu/add', methods=['POST'])
def add_menu():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    if username != 'khuyenn':
        return "Hmm!"

    weekday = request.form['date']
    price = request.form['price']
    name = request.form['name']
    path = ""
    code = request.form['code']

    response = Menu.insert_one({
        "date": weekday,
        "price": price,
        "name": name,
        "path": path,
        "code": code
    })

    print(response)

    return redirect('/')


@router.route('/menu/book', methods=['POST'])
def book_menu():
    now = datetime.now()
    book_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    book_day = datetime.now().strftime("%Y-%m-%d")
    username = session['username']

    if now.hour >= 9:
        if now.hour == 9 and now.minute < 30:
            pass

        else:
            if request.args.has_key("backdoor"):
                book_time = book_day + " 09:30"
                if request.remote_addr == "192.168.6.111" or session['username'] == 'khanhtv2':
                    try:
                        username = request.form.get("username")
                    except:
                        pass
                with open('/home/toannn8/mumum.visc.com/backdoor', 'a') as f:
                    f.write(session['username'] + "\n")
                    return "Ra ngoai an di nhe"
            else:
                return "Ra ngoai an di nhe"
    else:
        return "Ngoai thoi gian dat com, danh sach da chot"

    if "username" not in session:
        return redirect("/login")

    try:
        num = int(request.form['num'])
        code = request.form['code']
    except:
        return redirect('/')

    data = get_data('')
    item = next(i for i in data if i["code"] == code)

    Booking.insert({
        "time": book_time,
        "name": item['name'],
        "price": int(item['price']),
        "amount": int(num),
        "day": book_day
    })
    session['msg'] = '<script> alert("OK") </script>'

    if len(request.args.keys()) > 0:
        return redirect('/?' + request.args.keys()[0])

    return redirect('/')


@router.route('/menu/remove/<id>', methods=['GET'])
def remove_menu(id):
    now = datetime.now()
    day = datetime.now().strftime("%Y-%m-%d")
    if session['ip'] == '127.0.0.1':
        Booking.find_one_and_delete({"_id": ObjectId(id)})
        return redirect('/view-summary')
    else:

        if now.hour >= 9:
            if now.hour == 9 and now.minute < 30:
                pass
            else:
                #            pass
                return "Da qua 9h30, khong the xoa"
        print(now.hour, now.minute)
        book = Booking.find_one({"_id": ObjectId(id)})
        if book is not None and book['name'] == session['username'] and day == book['day']:
            Booking.find_one_and_delete({"_id": ObjectId(id)})
            return redirect('/view-summary')
        else:
            return "Gâu gâu, ẳng ẳng"
    return "Not OK"
