from datetime import date, datetime, timedelta
from pymongo import MongoClient

client = MongoClient()
db = client['lunch']
Booking = db['booking']
def getDataofDate(day):
    try:
        res = []
        books = Booking.find({"day": day})
        for book in books:
            if book['price'] > 0:
                res.append({
                    "name": book['name'],
                    "price": book['price'],
                    "amount": book['amount'],
                    "must_pay": (book['price'] - 5) * book['amount'] if books.count() >= 10 else book['price'] * book['amount']
                })
        return res
    except:
        return []
def tonghop():
    today = date.today()
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
        maps.append({"name": k, "must_pay": v})
    print maps
tonghop()
