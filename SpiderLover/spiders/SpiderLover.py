

import scrapy
import requests

class SpiderLover(scrapy.Spider):
    name='SpiderLover'
    start_urls = ['https://9isas.modareb.info/search?view=list']
    def start_requests(self):
        yield scrapy.Request(url = 'https://9isas.modareb.info/search?view=list', callback= self.parse)
    
    def parse(self, response):
        stories_urls = response.css('ul#blog-list-3 li a').xpath('@href').extract()
        yield from response.follow_all(stories_urls, callback = self.parse_stories_parts)

    def parse_stories_parts(self, response):
        stories_parts = response.css('div.leftside div a ::attr(href)').extract()
        yield from response.follow_all(stories_parts, callback = self.parse_stories_text)
        
        next_pageparts = response.css('div#nextSheet > a').xpath('@href').extract()
        if next_pageparts is not None:
            next_pageparts = response.urljoin(next_pageparts)
            yield scrapy.Request(next_pageparts , callback=self.parse_stories_parts)
 

    def parse_stories_text(self, response):
        stories_text = response.css('#fontconfig > div ::text').getall()
        yield {
            'text' : stories_text
        }
            

