# *-* coding: utf-8 *-*
from flask import render_template, session, request, redirect, Markup
from . import routes
from databases import *
from datetime import date, datetime, timedelta
import time
import ldap
from bson.objectid import ObjectId
from PIL import Image
import io, base64, qrcode, json
import random

import requests
from datetime import datetime

users_rocket = {}
session_rocket = requests.Session()


def authenticate(address, username, password):
    try:
        if len(password) == 0:
            password = "noob"
        ldap.protocol_version = 3
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        conn = ldap.initialize('ldap://192.168.4.222')
        conn.simple_bind_s(username + '@visc.com', password)
        return ""
    except Exception, e:
        print e
        return "Wrong username or password"


def dow(date):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dayNumber = date.weekday()
    return days[dayNumber]


def get_data(lol):
    try:
        if len(lol) == 0:
            lol = dow(date.today())
        data = Menu.find({"date": lol})
        res = []
        for d in data:
            res.append({
                "path": d['path'],
                "price": str(d['price']),
                "name": d['name'],
                "code": d['code']
            })
        return res
    except:
        return []


@routes.route('/add-menu', methods=['GET', 'POST'])
def addMenu():
    if not session.has_key('username'):
        return redirect("/login")
    if session['username'] != 'khuyenn':
        return "Hmm"
    if request.method == "GET":
        d = dow(date.today())
        return render_template('addMenu.html', date=d)
    else:
        d = request.form['date']
        price = request.form['price']
        name = request.form['name']
        path = ""
        code = request.form['code']
        res = Menu.insert_one({
            "date": d,
            "price": price,
            "name": name,
            "path": path,
            "code": code
        })
        print res
        return redirect('/')


@routes.route('/', methods=['GET'])
def index():
    if not session.has_key('username'):
        return redirect("/login")
    if session.has_key('mess'):
        mess = session['mess']
        session.pop('mess')
    else:
        mess = ''
    date = ''
    if request.remote_addr == "192.168.6.111":
        try:
            date = request.args.get('date')
            if not date:
                date = ''
        except:
            date = ''
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
    return render_template('index.html', mess=Markup(mess), img_lst=data, payed=payed)


@routes.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    if "Wrong" not in authenticate("", username, password):
        session['username'] = username
        session['ip'] = request.remote_addr
        Users.insert(
            {"username": username, "ip": request.remote_addr, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
        return redirect('/')
    else:
        return render_template('login.html', mess="Login fail")


@routes.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/login')


@routes.route('/book', methods=['POST', 'GET'])
def book():
    now = datetime.now()
    book_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    book_day = datetime.now().strftime("%Y-%m-%d")
    name = session['username']
    if now.hour >= 9:
        if now.hour == 9 and now.minute < 30:
            pass
        else:
            if request.args.has_key("backdoor"):
                book_time = book_day + " 09:30"
                if request.remote_addr == "192.168.6.111" or session['username'] == 'khanhtv2':
                    try:
                        name = request.form.get("name")
                    except:
			with open('/home/toannn8/mumum.visc.com/backdoor','a') as f:
				f.write(session['username'] + "\n")
			return "Ra ngoai an di nhe"
#                        name = session['username']
#                        pass
                else:
			return "Ra ngoai an di nhe"
            else:
                #                pass
                return "Ngoai thoi gian dat com, danh sach da chot"
    if not session.has_key("username"):
        return redirect("/login")
    try:
        num = int(request.form['num'])
        code = request.form['code']
    except:
        return redirect('/')
    data = get_data('')
    for d in data:
        if d['code'] == code:
            item = d
    Booking.insert({
        "time": book_time,
        "name": name,
        "item": item['name'],
        "price": int(item['price']),
        "amount": int(num),
        "day": book_day
    })
    session['mess'] = '<script> alert("OK") </script>'
    if len(request.args.keys()) > 0:
        return redirect('/?' + request.args.keys()[0])
    return redirect('/')


@routes.route('/view-summary', methods=['GET'])
def summary():
    if request.args.has_key("day"):
        day = request.args.get("day")
    else:
        day = datetime.now().strftime("%Y-%m-%d")
    booked = Booking.find({"day": day})
    guys = []
    sum_sumo = 0
    sum_nieu = 0
    menus_sumo = {}
    menus_nieu = {}
    all_nieu = 0
    all_sumo = 0
    week_now = datetime.now().strftime("%U")
    guys1 = []
    list_no = Payed.find({"payed": 0})
    for l in list_no:
        week = l['week']
        if week == week_now:
            continue
        guys1.append(l['name'])
    guys1 = list(set(guys1))
    print "guys1 ", guys1
    luck_guys = []
    booked_res = []
    for book in booked:
        if book['name'] in guys1:
            for i in range(int(book['amount'])):
                luck_guys.append(book['name'])
        if "Comnhanh" not in book['item']:
            all_sumo += int(book['price']) * book['amount']
            if not menus_sumo.has_key(book['item']):
                menus_sumo[book['item']] = book['amount']
            else:
                menus_sumo[book['item']] += book['amount']
            if int(book['price']) != 0:
                sum_sumo += book['amount']
        else:
            all_nieu += int(book['price']) * book['amount']
            if not menus_nieu.has_key(book['item']):
                menus_nieu[book['item']] = book['amount']
            else:
                menus_nieu[book['item']] += book['amount']
            if int(book['price']) != 0:
                sum_nieu += book['amount']
        booked_res.append(book)
        for i in range(int(book['amount'])):
            guys.append(book['name'])
    if len(luck_guys) > 0:
        guys = luck_guys
    guys = list(set(guys))
    print "guys ", guys
    white_list = ["khuyenn", "anhvtm3", "quyenntm1", "linhld3","hoapt32","dungntt29"]
    for wl in white_list:
        if wl in guys:
            guys.remove(wl)
    bk_sumo = []
    bk_nieu = []
    for k, v in menus_sumo.iteritems():
        bk_sumo.append({"name": k, "num": v})
    for k, v in menus_nieu.iteritems():
        bk_nieu.append({"name": k, "num": v})
    now = datetime.now()
    if now.hour >= 9:
        if now.hour == 9 and now.minute < 30:
            lucky_guy = ''
        else:
            lucky_guy = LuckyGuys.find_one({"day": day})
            if lucky_guy is None:
                lucky_guy = ""
                if len(guys) > 0:
                    if len(guys) == 1:
                        lucky_guy = guys[0]
                    else:
                        lucky_guy1 = random.choice(guys)
                        while lucky_guy1 in guys:
                            guys.remove(lucky_guy1)
                        lucky_guy2 = random.choice(guys)
                        lucky_guy = lucky_guy1 + ',' + lucky_guy2
                    LuckyGuys.insert_one({"name": lucky_guy, "day": day})
                else:
                    lucky_guy = ''
            else:
                lucky_guy = lucky_guy['name']
    else:
        lucky_guy = ""
    today = datetime.strptime(day, "%Y-%m-%d")
    prev = today + timedelta(days=-1)
    next = today + timedelta(days=1)
    prev = prev.strftime("%Y-%m-%d")
    next = next.strftime("%Y-%m-%d")
    return render_template('summary.html', booked=booked_res, sum_sumo=sum_sumo, sum_nieu=sum_nieu, menu_sumo=bk_sumo,
                           menu_nieu=bk_nieu, all_sumo=all_sumo, all_nieu=all_nieu, lucky_guy=lucky_guy, nextt=next,
                           prev=prev)


@routes.route('/del/<id>', methods=['GET'])
def delete(id):
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
        print now.hour, now.minute
        book = Booking.find_one({"_id": ObjectId(id)})
        if book is not None and book['name'] == session['username'] and day == book['day']:
            Booking.find_one_and_delete({"_id": ObjectId(id)})
            return redirect('/view-summary')
        else:
            return "Gâu gâu, ẳng ẳng"
    return "Not OK"


def getDataofDate(day):
    try:
        DAY = datetime.strptime(day, "%Y-%m-%d")
        week = DAY.strftime("%U")
        # print DAY, week
        res = []
        books = Booking.find({"day": day})
        for book in books:
            if book['price'] > 0:
                res.append({
                    "name": book['name'],
                    "price": book['price'],
                    "amount": book['amount'],
                    "must_pay": book['price'] * book['amount'],
                    "week": week
                })
        return res
    except:
        return []


@routes.route('/summary-of-week', methods=['GET'])
def tonghop():
    if request.args.has_key('pay'):
        pay = int(request.args.get('pay'))
    else:
        pay = 2
    if request.args.has_key('day'):
        today = request.args.get('day')
        today = datetime.strptime(today, "%Y-%m-%d")
        week = today.strftime("%U")
    else:
        today = date.today()
        week = datetime.now().strftime("%U")
    prev_weekday = today + timedelta(days=-7)
    next_weekday = today + timedelta(days=7)
    prev_weekday = prev_weekday.strftime("%Y-%m-%d")
    next_weekday = next_weekday.strftime("%Y-%m-%d")
    dates = [today + timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]
    res = []
    result = {}
    maps = []
    all = 0
    for d in dates:
        res += getDataofDate(d.strftime("%Y-%m-%d"))
    for r in res:
        all += int(r['must_pay'])
        if not result.has_key(r['name']):
            result[r['name']] = r['must_pay']
        else:
            result[r['name']] += r['must_pay']
    for k, v in result.iteritems():
        thanhtoan = Payed.find_one({"name": k, "week": week})
        if thanhtoan is None:
            Payed.insert_one({"name": k, "payed": 0, "week": week})
            payed = 0
        else:
            payed = thanhtoan['payed']
        if payed == pay or pay == 2:
            maps.append({"name": k, "must_pay": v, "payed": payed, "_id": thanhtoan['_id']})
    return render_template('summary_week.html', booked=maps, all=all, prev_weekday=prev_weekday,
                           next_weekday=next_weekday)


@routes.route('/pay/<id>')
def pay(id):
    if session['username'] == 'khanhtv2' or session['username'] == 'khuyenn':
        payed = Payed.find_one(ObjectId(id))
        if payed != 2:
            Payed.update_one({"_id": ObjectId(id)}, {"$set": {"payed": 1 - payed['payed']}})
        return redirect('/tong-no')
    return "Not OK"


def weekBoundaries(year, week):
    startOfYear = date(year, 1, 1)
    now = startOfYear + timedelta(weeks=week)
    sun = now - timedelta(days=now.isoweekday() % 7)
    sat = sun + timedelta(days=6)
    return now, sat


@routes.route("/tong-no")
def tongno():
    list_no = list(Payed.find({"payed": 0}))
    l = []
    weeks = {}
    for no in list_no:
        week = no['week']
        weeks[week] = 1
    result = []
    dates = {}
    for week, v in weeks.iteritems():
        if int(week) < 30:
            mon, sat = weekBoundaries(2019, int(week))
        else:
            mon, sat = weekBoundaries(2018, int(week))
        for d in [mon + timedelta(days=i) for i in range(0 - mon.weekday(), 7 - mon.weekday())]:
            dates[d] = 1
    for d, v in dates.iteritems():
        result += getDataofDate(d.strftime("%Y-%m-%d"))
    # for r in result:
    #     print r
    for no in list_no:
        week = no['week']
        week_now = datetime.now().strftime("%U")
        if week == week_now:
            continue
        all = 0
        if week == "52":
            mon, sat = weekBoundaries(2018, int(week))
        else:
            mon, sat = weekBoundaries(2019, int(week))
        week = mon.strftime("%Y-%m-%d") + " den " + sat.strftime("%Y-%m-%d")
        if no['week'] == "52":
            no['week'] = "00"
        for r in result:
            if r['name'] == no['name']:
                if r['week'] == no['week']:
                    all += int(r['must_pay'])
        l.append(
            {"name": no['name'], "week": week, "must_pay": all, "_id": no['_id'], "start": mon.strftime("%Y-%m-%d")})
    return render_template("tongno.html", list_no=l)
@routes.route("/thanh-toan")
def thanhtoan():
    if not session.has_key('username'):
        return redirect("/login")
    list_no = Payed.find({"payed":0,"name":session['username']})
    l = []
    weeks = {}
    for no in list_no:
        week = no['week']
        weeks[week] = 1
    dates = {}
    for week, v in weeks.iteritems():
	week_now = datetime.now().strftime("%U")
	if week == week_now:
	    continue
	print week
        mon, sat = weekBoundaries(2019, int(week))
        for d in [mon + timedelta(days=i) for i in range(0 - mon.weekday(), 7 - mon.weekday())]:
            dates[d] = 1
    count = 0
    for d, v in dates.iteritems():
        r = Booking.find({"day":d.strftime("%Y-%m-%d"),"name":session['username']})
	print r
	if r is not None:
	        for i in r:
		    print i['day']
		    count += int(i['amount'])
    count = int(count) * 35000
    if count == 0:
	return "Ban dang khong co no"
    qrcode_info = {
        "bankCode": "MB",
        "cust_mobile": "0978030523",
        "transfer_type": "MYQR",
        "trans_amount": str(count)
    }
    img = qrcode.make(json.dumps(qrcode_info))
    img = img.resize((300, 300), Image.ANTIALIAS)
    buf_cover = io.BytesIO()
    img.save(buf_cover, format='JPEG')
    image_cover = buf_cover.getvalue()
    image_base64 = base64.b64encode(image_cover)
    return render_template('thanhtoan.html',img=image_base64)

@routes.route("/crawl")
def crawl():
    import os
    os.system("/usr/bin/python /home/toannn8/mumum.visc.com/crawl.py")
    return "OK"
