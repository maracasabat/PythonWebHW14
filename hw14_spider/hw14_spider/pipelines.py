
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from .models import Person, Keywords, Quotes

start_urls = "http://quotes.toscrape.com/"


class Hw14SpiderPipeline(object):
    def process_item(self, item, authors):
        engine = create_engine("sqlite:///database.db.sqlite3")
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        try:
            exist = 0
            if item["keywords"] and item["author"] and item["quote"]:
                name = item["author"][0]
                for person in session.query(Person).all():
                    if f"{name}" == person.author_name:
                        exist = 1
            if exist == 0:
                author_url = item["author_url"]
                author_url_clean = author_url[10:-13] + "/"
                author_url_clean_full_path = start_urls + author_url_clean

                response = requests.get(author_url_clean_full_path)
                soup = BeautifulSoup(response.text, "lxml")
                birthday = soup.find(class_="author-born-date").get_text(strip=True)
                place = soup.find(class_="author-born-location").get_text(strip=True)
                name = item["author"][0]
                new_person = Person(
                    author_name=f"{name}",
                    author_url=f"{author_url_clean_full_path}",
                    birthday_and_place_of_born=f"{birthday} {place}",
                )

                session.add(new_person)
                session.commit()

            if item["keywords"] and item["author"] and item["quote"]:
                clean_quote = item["quote"]
                clean_quote = clean_quote[1:-1]
                for person in session.query(Person).all():
                    if f"{name}" == person.author_name:
                        id = person.id
                        quotes = Quotes(quote=f"{clean_quote}", author_id=int(id))
                        session.add(quotes)

            if item["keywords"] and item["author"] and item["quote"]:
                for keyword in item["keywords"]:
                    keywords = Keywords(keyword=f"{keyword}")
                    session.add(keywords)

            session.commit()

        finally:
            session.close()

        return item
