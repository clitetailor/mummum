from flask import Blueprint, request, render_template
from datetime import datetime, date, timedelta
from server.db import Payed, get_data_of_date


router = Blueprint('week_summary', __name__)


@router.route('/week-summary', methods=['GET'])
def render_week_summary():
    if 'pay' in request.args:
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
    dates = [today + timedelta(days=i)
             for i in range(0 - today.weekday(), 7 - today.weekday())]
    res = []
    result = {}
    maps = []
    all = 0
    for d in dates:
        res += get_data_of_date(d.strftime("%Y-%m-%d"))
    for r in res:
        all += int(r['must_pay'])
        if r['name'] not in result:
            result[r['name']] = r['must_pay']
        else:
            result[r['name']] += r['must_pay']

    for k, v in result.items():
        thanhtoan = Payed.find_one({"name": k, "week": week})
        if thanhtoan is None:
            Payed.insert_one({"name": k, "payed": 0, "week": week})
            payed = 0
        else:
            payed = thanhtoan['payed']
        if payed == pay or pay == 2:
            maps.append({"name": k, "must_pay": v,
                         "payed": payed, "_id": thanhtoan['_id']})
    return render_template('week-summary.html', booked=maps, all=all, prev_weekday=prev_weekday,
                           next_weekday=next_weekday)
