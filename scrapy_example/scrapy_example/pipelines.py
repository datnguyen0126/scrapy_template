# Define your item pipelines here
#
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class QuotePipeline:

    def __init__(self) -> None:
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.con = sqlite3.connect("myquotes.db")
        self.curr = self.con.cursor()

    def create_table(self):
        self.con.execute("""drop table if exists quotes""")
        self.con.execute("""
            create table quotes(
                title text,
                author text,
                tags text
            )
        """)

    def store_db(self, item):
        self.con.execute("insert into quotes values (?,?,?)", (item['title'][0], item['author'][0], item['tags'][0])) 
        self.con.commit()


    def process_item(self, item, spider):
        print(f"My item: {item['title'][0]}")
        self.store_db(item=item)
        return item
