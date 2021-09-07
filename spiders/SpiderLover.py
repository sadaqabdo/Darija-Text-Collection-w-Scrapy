import scrapy
import requests

class SpiderLover(scrapy.Spider):
    name='SpiderLover'
    start_urls = ['https://yoururl.com']
    def start_requests(self):
        yield scrapy.Request(url = 'https://yoururl.com', callback= self.parse)
#collecting urls of the stories
    def parse(self, response):
        stories_urls = response.css('ul#blog-list-3 li a').xpath('@href').extract()
        yield from response.follow_all(stories_urls, callback = self.parse_stories_parts)
#collecting the urls of stories' parts
    def parse_stories_parts(self, response):
        stories_parts = response.css('div.leftside div a ::attr(href)').extract()
        yield from response.follow_all(stories_parts, callback = self.parse_stories_text)
#next_page        
        next_pageparts = response.css('div#nextSheet > a').xpath('@href').extract()
        if next_pageparts is not None:
            next_pageparts = response.urljoin(next_pageparts)
            yield scrapy.Request(next_pageparts , callback=self.parse_stories_parts)
#extracting text
     def parse_stories_text(self, response):
        stories_text = response.css('#fontconfig > div ::text').getall()
        yield {
            'text' : stories_text
        }
        
    
