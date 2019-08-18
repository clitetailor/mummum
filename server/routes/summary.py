from flask import Blueprint, request, render_template
from datetime import datetime, timedelta
from server.db import Booking, Payed, LuckyGuys
import requests
import random

router = Blueprint('summary', __name__)

@router.route('/view-summary', methods=['GET'])
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
    print("guys1 ", guys1)
    luck_guys = []
    booked_res = []
    for book in booked:
        if book['name'] in guys1:
            for i in range(int(book['amount'])):
                luck_guys.append(book['name'])
        if "Comnhanh" not in book['item']:
            all_sumo += int(book['price']) * book['amount']
            if book['item'] not in menus_sumo:
                menus_sumo[book['item']] = book['amount']
            else:
                menus_sumo[book['item']] += book['amount']
            if int(book['price']) != 0:
                sum_sumo += book['amount']
        else:
            all_nieu += int(book['price']) * book['amount']
            if book['item'] not in menus_nieu:
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
    print("guys ", guys)
    white_list = ["khuyenn", "anhvtm3", "quyenntm1",
                  "linhld3", "hoapt32", "dungntt29"]
    for wl in white_list:
        if wl in guys:
            guys.remove(wl)
    bk_sumo = []
    bk_nieu = []
    for k, v in menus_sumo.items():
        bk_sumo.append({"name": k, "num": v})
    for k, v in menus_nieu.items():
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
