# -*- coding: utf-8 -*-
import datetime
import logging

from scrapy.spiders import CrawlSpider

from scrapy_app.items import Event


def compose_list_url(start_date, offset):
    return 'https://www.indievox.com/event/get-more-event-date-list?style=poster&content=event_ticket&content_container_id=event-ticket-block&start_date=' + start_date + '&end_date=2030-12-31&key_word=&load_more=1&pagenation_type=full-page-more&pagenation_expand_col=&offset=' + str(offset) + '&length=7'


class IndievoxSpider(CrawlSpider):
    name = 'indievox'
    allowed_domains = ['indievox.com']
    today = datetime.date.today()
    today_formatted = today.strftime('%Y-%m-%d')
    offset = 0
    start_urls = [compose_list_url(today_formatted, offset)]

    # name = 'indievox'
    # allowed_domains = ['indievox.com']
    # start_urls = ['http://indievox.com/']
    #
    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    def parse(self, response):
        # for event in response.css('div.event-block'):
        event = response.css('div.event-block')[0]
        detail = event.xpath('a/@href').extract_first()
        title = event.css('div.event-data').xpath('h5/a/@title').extract_first()
        image = event.xpath('a/img/@src').extract_first()
        url = response.urljoin(detail)
        meta = {'processing_event': Event(title=title, image=image, url=url)}
        yield response.follow(detail, self.parse_detail, meta=meta)

        # infinite scroll
        # if len(response.css('div.event-block')) > 0:
        #     self.offset += 7
        #     yield response.follow(compose_list_url(self.today_formatted, self.offset))

    def parse_detail(self, response):
        event = response.meta['processing_event']

        event['body'] = response.css('h1+ div').extract_first()  # html body

        # \n                                            2018/04/21(Sat) 19:30
        event['date'] = response.css('tr:nth-child(2) td::text')[0].re_first('[\s]{44}(\d{4}\/\d{2}\/\d{2})')
        event['time'] = response.css('tr:nth-child(2) td::text')[0].re_first('(\d{2}\:\d{2})')
        event['venue'] = response.css('tr:nth-child(5) td a::text').re_first('\s{53}(.*)\s{48}')
        event['address'] = response.css('tr:nth-child(6) td::text').re_first('\s{97}(.*)')
        event['price'] = response.css('tr:nth-child(1) td::text').re_first('\s{45}(.*)\s{40}')

        # might have <a> and raw text element inside artist <td>
        linked_artists = response.css('tr:nth-child(3) td a::text').extract()
        unlinked_artists = response.css('tr:nth-child(3) td::text').re('\w{2,}')
        event['artists'] = linked_artists + unlinked_artists

        yield event
