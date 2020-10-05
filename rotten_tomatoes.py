import requests as req
from bs4 import BeautifulSoup as soup
import csv




with open("rotten_tomatoes.csv","w",newline="",encoding="utf-8") as cfile:
    writer = csv.DictWriter(cfile,fieldnames = ["date","review"])
    writer.writeheader()
    for i in range(1,16):
        page = soup(req.get(f"https://www.rottentomatoes.com/m/mulan_2020/reviews?type=&sort=&page={i}").content, "lxml")
        containers = page.find_all("div",{"class":"review_area"})
        for container in containers:
            date = container.find("div",{"class":"review-date"}).text.strip()
            review = container.find("div",{"class":"the_review"}).text.strip()
            writer.writerow({
                "date":date,
                "review":review
            })