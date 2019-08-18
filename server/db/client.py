from pymongo import MongoClient

client = MongoClient()

db = client['lunch']
Users = db['users']
Booking = db['booking']
Menu = db['menu']
Payed = db['payed']
PayedHTUD = db['htud']
LuckyGuys = db['luckyguys']
