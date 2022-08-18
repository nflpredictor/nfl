import scrapy
import json
from scrapy.crawler import CrawlerProcess
import os
import logging
#import boto3
#from botocore.client import Config as BotoConfig

class NFLTeamsLogosSpider(scrapy.Spider):
    name = 'nflteamslogos'

    start_urls = [
                'https://www.nfl.com/teams/'
    ]

    def parse(self, response):

        for teams in response.css('section.d3-l-grid--outer.d3-l-section-row'):
            #for day in daily_games.css('h3.Card__Header__Title.Card__Header__Title--no-theme'):
            for team in teams.css('div.d3-l-col__col-12'):
                #try:
                    yield{
                        #'week': response.css('div.custom--week.is-active > span.week.week-range::text').get(),
                        'team_name' : team.css('h4.d3-o-media-object__roofline.nfl-c-custom-promo__headline::text').get(),
                        'img_link' : team.css('img.img-responsive::attr(src').get()
                    }
            #except:
        #return super().parse(response, **kwargs)
        #next_page = response.css('a.nfl-o-table-pagination__next').attrib['href']
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)

# Name of the file where the results will be saved
path="01_scraping/json/"
filename = "nfl_teams_logos.json"

# if the file exist, remove this
if filename in os.listdir(path):
    os.remove(path+filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.DEBUG,
    #'FEED FORMAT' : ,
    'FEED URI' : path,
    "FEEDS": {
        path+filename : {"format": "json"},
    },
    "AUTOTHROTTLE_ENABLED" : False
})

# Start the crawling using the spider you defined above
process.crawl(NFLTeamsLogosSpider)
process.start()

#client = boto3.client('s3',aws_access_key_id=os.environ['AWS_ACCESS_KEY'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
#upload_file_bucket = "nflpredictor-scrapy"
#upload_file_key = filename
#client.upload_file(path+filename,upload_file_bucket,upload_file_key)
