def get_data_of_date(day):
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


def get_data(weekday):
    try:
        if len(weekday) == 0:
            weekday = day_of_week(date.today())

        data = Menu.find({"date": weekday})

        return map(lambda item: {
            "path": item["path"],
            "price": str(item["price"]),
            "name": item["name"],
            "code": item["code"]
        }, data)
    except:
        return []
