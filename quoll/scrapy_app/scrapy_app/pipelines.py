# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql

from quoll.quoll import settings


class StoreEventPipeline(object):

    def __init__(self):
        print('pipline')
        # self.connect = pymysql.connect(
        #     host=settings.DATABASES['default']['HOST'],
        #     db=settings.DATABASES['default']['NAME'],
        #     user=settings.DATABASES['default']['USER'],
        #     password=settings.DATABASES['default']['PASSWORD'],
        #     charset='utf8',
        #     use_unicode=True)
        # self.cursor = self.connect.cursor()

    def insert(self, query, args=None):
        try:
            self.cursor.execute(query, args)
            self.connect.commit()
            return self.cursor.lastrowid
        except:
            self.connect.rollback()

    def update(self, query, args=None):
        try:
            self.cursor.execute(query, args)
            self.connect.commit()
        except:
            self.connect.rollback()

    def is_exist(self, query, args=None):
        self.cursor.execute(query, args)
        return self.cursor.fetchone()


    def process_item(self, item, spider):
        query = """SELECT * FROM events WHERE url = %s"""
        exist = self.is_exist(query, item['url'])
        if not exist:
            venue_exist_query = """SELECT id FROM venues WHERE name = %s"""
            venue_exist = self.is_exist(venue_exist_query, item['venue'])
            if not venue_exist:
                venue_insert_query = """INSERT INTO venues(name, address) VALUES (%s, %s)"""
                venue_id = self.insert(venue_insert_query, (item['venue'], item['address']))
            else:
                venue_id = venue_exist[0]

            artist_exist_query = """SELECT id FROM artists WHERE name = %s"""
            fetched_artists = item['artists']
            artist_ids = []
            for artist_name in fetched_artists:
                artist_exist = self.is_exist(artist_exist_query, artist_name)
                if not artist_exist:
                    artist_insert_query = """INSERT INTO artists(name) VALUES (%s)"""
                    artist_ids.append(self.insert(artist_insert_query, artist_name))
                else:
                    artist_ids.append(artist_exist[0])

            event_insert_query = """
                            INSERT INTO events(title, url, image, body, date, time, venue_id, price) VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s)
                            """
            event_id = self.insert(event_insert_query, (
                        item['title'],
                        item['url'],
                        item['image'],
                        item['body'],
                        item['date'],
                        item['time'],
                        venue_id,
                        item['price']))

            performer_insert_query = """INSERT INTO performers(artist_id, event_id) VALUES (%s, %s)"""
            performer_exist_query = """SELECT * FROM performers WHERE artist_id = %s AND event_id = %s"""
            for artist_id in artist_ids:
                performer_exist = self.is_exist(performer_exist_query, (artist_id, event_id))
                if not performer_exist:
                    self.insert(performer_insert_query, (artist_id, event_id))
        else:
            # would not updating venue, artists
            event_update_query = """
                        UPDATE events set title = %s, url = %s, image = %s, body = %s, date = %s, time = %s, price = %s
            """
            self.update(event_update_query, (
                        item['title'],
                        item['url'],
                        item['image'],
                        item['body'],
                        item['date'],
                        item['time'],
                        item['price']))

        return item
