import csv
import requests
from bs4 import BeautifulSoup
import re

url = "https://mediakit.iportal.ru/our-team"
headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}

if __name__ == '__main__':
    resultArray = [["Город", "Имя", "Должность", "Почта"]]
    rank, email = [], []

    response = requests.get(url, headers=headers)
    text = response.text.replace("<br>", " ")
    soup = BeautifulSoup(text, "lxml")

    cities = soup.find_all("div",
                           attrs={"data-elem-id": {
                               "1596441248760", "1635348635083",
                               "1596441835050"}})

    names = soup.find_all("div",
                          attrs={"data-elem-id": {
                              "1648717220470", "1635348635117",
                              "1596441301499", "1654226718646",
                              "1596441835055", "1629779928279",
                              "1599793822858", "1629081944686",
                              "1637296945024", "1652700872756",
                              "1652701798296", "1642996413669",
                              "1673600278514", "1652702166877"}})

    ranks = soup.find_all("div",
                          attrs={"data-elem-id": {
                              "1648717229809", "1635348635122",
                              "1596441448712", "1596441835072",
                              "1599793822884", "1629081944695",
                              "1637296945030", "1652700178564",
                              "1652700889499", "1652701843642",
                              "1642996413676", "1643959011978",
                              "1673600074049", "1629779928286"}})

    for data in ranks:
        try:
            data.find_next("a")
            rank.append(
                re.match(r"[А-я-\s]+",
                         data.text).group())
            email.append(
                re.search(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
                          data.text).group())
        except:
            email.append("--")

    for i in range(0, len(cities)):
        try:
            resultArray.append([cities[i].text,
                                names[i].text,
                                rank[i],
                                email[i]])
        except IndexError:
            resultArray.append([cities[i].text])

    with open("test.csv", "w", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=',', )
        for data in resultArray:
            writer.writerow(data)
