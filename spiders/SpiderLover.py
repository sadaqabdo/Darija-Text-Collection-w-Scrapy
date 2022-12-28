import scrapy
import requests

class SpiderLover(scrapy.Spider):
    name='SpiderLover'
    start_urls = ['www.9esa.com']
    def start_requests(self):
        yield scrapy.Request(url = 'https://www.9esa.com/search?view=list', callback= self.parse)
    #collecting urls of the stories
    def parse(self, response):
        stories_urls = response.css('#listOfStories li div a').xpath('@href').extract()
        yield from response.follow_all(stories_urls, callback = self.parse_stories_parts)
    #collecting the urls of stories' parts
    def parse_stories_parts(self, response):
        stories_parts = response.css('#daily-posts div div.content h2 a ::attr(href)').extract()
        yield from response.follow_all(stories_parts, callback = self.parse_stories_text)
    #next_page        
        next_pageparts = response.css('#pager > a').xpath('@href').extract()
        if next_pageparts is not None:
            url_str = ' '.join(map(str, next_pageparts))

            next_pageparts = response.urljoin(url_str)
            yield scrapy.Request(next_pageparts , callback=self.parse_stories_parts)
    #extracting text
    def parse_stories_text(self, response):
        stories_text = response.css('#content div.story-body > div ::text').getall()
        yield {
            'text' : stories_text
        }

    
