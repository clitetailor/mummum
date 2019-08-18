from flask import Blueprint, request, render_template, session, redirect
from datetime import datetime, timedelta
from server.db import Booking, Payed
from server.utils.datetime import week_boundaries
from PIL import Image
import requests
import qrcode
import base64
import io
import json


router = Blueprint('payment', __name__)


@router.route("/payment", methods=["GET"])
def render_payment_page():
    if "username" not in session:
        return redirect("/login")

    list_no = Payed.find({"payed": 0, "name": session['username']})
    l = []
    weeks = {}
    for no in list_no:
        week = no['week']
        weeks[week] = 1
    dates = {}
    for week, v in weeks.items():
        week_now = datetime.now().strftime("%U")
        if week == week_now:
            continue
        print(week)
        mon, sat = week_boundaries(2019, int(week))
        for d in [mon + timedelta(days=i) for i in range(0 - mon.weekday(), 7 - mon.weekday())]:
            dates[d] = 1
    count = 0
    for d, v in dates.items():
        r = Booking.find({"day": d.strftime("%Y-%m-%d"),
                          "name": session['username']})
    print(r)
    if r is not None:
        for i in r:
            print(i['day'])
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

    return render_template('payment.html', img=image_base64)
