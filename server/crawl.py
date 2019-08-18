from bs4 import BeautifulSoup
from datetime import date, datetime
from pymongo import MongoClient
import requests

client = MongoClient()
proxies = {
    'http': 'http://192.168.5.8:3128',
    'https': 'https://192.168.5.8:3128'
}
db = client['lunch']


Menu = db['menu']
Menu.drop()
days = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"]


def dow(date):
    dayNumber = date.weekday()
    return days[dayNumber]


def sumo():
    j = 1
    for i in range(2, 8):
        r = requests.get(
            'http://comhopsumo.com/product-category/cac-thu-trong-tuan/com-van-phong-thu-' + str(i), proxies=proxies)
#	print r.content
        soup = BeautifulSoup(r.content, 'lxml')
        menus = soup.find_all("div", {"class": "product-small box"})
#	print menus
        for menu in menus:
            img = menu.findAll('img')
            name = menu.find_all(class_="name product-title")[0].text
            price = 35
            link = img[0]['src']
#	    print name,link
            file_name = 'sumo' + str(j) + '.jpg'
            res = {
                'date': days[i - 2],
                'path': file_name,
                'name': "Sumo " + name,
                'price': price,
                'code': str(j)
            }
            print(res)
            Menu.insert_one(res)
            j += 1
            file_name = '/home/toannn8/mumum.visc.com/static/com/' + file_name
            link = 'http:' + link
            data = requests.get(link, stream=True, proxies=proxies)
            data.raise_for_status()
            data.raw.decode_content = True
            with open(file_name, 'wb') as f:
                f.write(data.content)


def comnieu():
    for i in range(2, 8):
        url = "http://comnieuvanphong.vn/122%s/thu-%s.html" % (i, i)
        r = requests.get(url, proxies=proxies)
        # print (r.content)
        soup = BeautifulSoup(r.content, 'lxml')
        menus = soup.find("ul", {"class": "list-pro"})
        menus = menus.findAll('li')
        j = 1
        for menu in menus:
            img = menu.find("img")['src']
            name = menu.find("img")['alt']
            price = menu.findAll("p", {"class": "price"})[0].text
            if len(price) > 7:
                price = price[:2]
            else:
                price = 0
                continue
            price = str(int(price) + 15)
            file_name = img[12:]
            res = {
                'date': days[i - 2],
                'path': file_name,
                'name': "Com nieu " + name,
                'price': price,
                'code': "nieu" + str(j)
            }
            j += 1
            if (int(res['price']) > 30):
                Menu.insert_one(res)
            file_name = '/data/webroot/mumum.visc.com/static/com/' + file_name
            link = 'http://comnieuvanphong.vn/' + img
            data = requests.get(link, stream=True, proxies=proxies)
            data.raise_for_status()
            data.raw.decode_content = True
            with open(file_name, 'wb') as f:
                f.write(data.content)


def comnhanh():
    j = 1
    for i in range(2, 8):
        r = requests.get(
            'http://comnhanh.vn/thuc-don-ngay-thu-' + str(i), proxies=proxies)
        soup = BeautifulSoup(r.content, 'lxml')
        menus = soup.find_all(class_="col-sm-4")
        for menu in menus:
            img = menu.findAll('img')
            name = menu.findAll('a')[1].text
            price = 30
            link = img[0]['src']
            print(name, link)
            file_name = 'comnhanh' + str(j) + '.jpg'
            res = {
                'date': days[i - 2],
                'path': file_name,
                'name': "Comnhanh " + name,
                'price': price,
                'code': 'nhanh'+str(j)
            }
            print(res)
            Menu.insert_one(res)
            j += 1
            file_name = '/data/webroot/mumum.visc.com/static/com/' + file_name
            link = 'http://comnhanh.vn' + link
            data = requests.get(link, stream=True, proxies=proxies)
            data.raise_for_status()
            data.raw.decode_content = True
            with open(file_name, 'wb') as f:
                f.write(data.content)


def crawl():
    sumo()
    # comnhanh()
    # comnieu()


if __name__ == "__main__":
    crawl()
