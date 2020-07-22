from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv
import time

def parse_price(price):
    return float(price.replace(" ","").replace(",", "."))

def get_data_day(name, day, month, year):
    page = get(f'https://www.gpw.pl/archiwum-notowan?fetch=0&type=10&instrument={name}&date={day}-{month}-{year}&show_x=Poka%C5%BC+wyniki')
    bs = BeautifulSoup(page.content, 'html.parser')
    try:

        name = bs.find('tbody').find('td', class_="left").get_text()
        date = bs.find('tbody').find_all('td')[1].get_text()
        startPrice = parse_price(bs.find('tbody').find_all('td')[3].get_text())
        maxPrice = parse_price(bs.find('tbody').find_all('td')[4].get_text())
        minPrice = parse_price(bs.find('tbody').find_all('td')[5].get_text())
        closePrice = parse_price(bs.find('tbody').find_all('td')[6].get_text())
        changeOfCourse = parse_price(bs.find('tbody').find_all('td')[7].get_text())
        quantity = parse_price(bs.find('tbody').find_all('td')[8].get_text())
        cursor.execute('INSERT INTO stockQuotes VALUES (?, ?, ?, ?, ?, ?, ?, ?)',(name,date,startPrice,minPrice,maxPrice,closePrice,changeOfCourse,quantity))
        db.commit()
        print(name, date,startPrice,minPrice,maxPrice,closePrice,changeOfCourse,quantity)

    except AttributeError:
        pass

db = sqlite3.connect('dane.db')
cursor = db.cursor()

if len(argv) > 1 and argv[1] == 'setup':
    cursor.execute('''CREATE TABLE stockQuotes (name TEXT, date TEXT, startPrice REAL, minPrice REAL, maxPrice REAL, closePrice REAL, changeOfCourse REAL, quantity REAL)''')
    quit()


tic = time.perf_counter()
for year in range(2015,2021):
    for month in range(1,13):
        for day in range(1,32):
            get_data_day('CDPROJEKT',day,month,year)
            print(f'{day}-{month}-{year}')
toc = time.perf_counter()
print(f"Pobieranie trwało {toc - tic:0.4f} sekund")

db.close()