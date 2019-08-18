from flask import Blueprint, session, redirect
from bson import ObjectId
from server.db import Payed


router = Blueprint('payment', __name__)


@router.route('/pay/<id>')
def pay(id):
    if session['username'] == 'khanhtv2' or session['username'] == 'khuyenn':
        payed = Payed.find_one(ObjectId(id))
        if payed != 2:
            Payed.update_one({"_id": ObjectId(id)}, {
                             "$set": {"payed": 1 - payed['payed']}})
        return redirect('/debt/total')
    return "Not OK"
