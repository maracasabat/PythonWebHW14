# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import lxml.html
from bs4 import BeautifulSoup

from .models import Person, Keywords


class Hw14SpiderPipeline:
    def process_item(self, item, authors):
        engine = create_engine('sqlite:///hw14.db')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        return item
