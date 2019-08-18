from datetime import date, datetime, timedelta
from pymongo import MongoClient

client = MongoClient()
db = client['lunch']
Booking = db['booking']


def extract_book(book, sale_off):
    return {
        "name": book['name'],
        "price": book['price'],
        "amount": book['amount'],
        "must_pay": (book['price'] - sale_off) * book['amount']
    }


def get_data_of_date(day):
    try:
        books = Booking.find({"day": day})
        sale_off = 5 if books.count() >= 10 else 0

        return list(map(
            lambda book: extract_book(book, sale_off),
            filter(lambda book: book['price'] > 0, books)
        ))
    except:
        return []


def summary():
    today = date.today()
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
        maps.append({"name": k, "must_pay": v})

    print(maps)


if __name__ == "__main__":
    summary()
