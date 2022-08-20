#from credentials import access_key, secret_access_key
from http import client
import scrapy
import json
from scrapy.crawler import CrawlerProcess
import os
import logging
import boto3
from botocore.client import Config as BotoConfig

class ODDS2021Spider(scrapy.Spider):
    name = 'odds2021'

    urls_weeks=[]
    for week in range(1,19):
        #for year in range(2017,2022:
        urls_weeks.append("https://gridirongames.com/nfl-weekly-betting-lines/?Year=2021&Week="+ 
            str(week))
    
    start_urls=urls_weeks

    def parse(self, response):

        split = response.url.split("/")
        #print(split)

        for games in response.css('tbody'):
            for rows in games.css('//*/tr'):
                if bool(games.xpath('//*[@id="main"]/div/div[2]/table/tbody/tr/th').get()):
            #try:
                #idgame = scores.css('section.Scoreboard.bg-clr-white.flex.flex-auto.justify-between::attr(id)').get()
                    yield{
                        #'week': response.css('div.custom--week.is-active > span.week.week-range::text').get(),
                        #'season' : split[9],
                        'week' : split[4],
                        'awayteam': rows.xpath('//*[@id="main"]/div/div[2]/table/tbody/tr/td[2]/div[2]::text').get(),
                        'hometeam': rows.xpath('//*[@id="main"]/div/div[2]/table/tbody/tr/td[1]/div[2]::text').get(),
                        'oddaway': rows.xpath('//*[@id="main"]/div/div[2]/table/tbody/tr/td[4]::text').get(),
                        'oddhome' : rows.xpath('//*[@id="main"]/div/div[2]/table/tbody/tr/td[3]::text').get()
                        }
            #except:
        #return super().parse(response, **kwargs)
        #next_page = response.css('a.nfl-o-table-pagination__next').attrib['href']
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)

# Name of the file where the results will be saved
path="01_scraping/json/"
filename = "odds_2021.json"

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
process.crawl(ODDS2021Spider)
process.start()

#client = boto3.client('s3',aws_access_key_id=os.environ['AWS_ACCESS_KEY'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

#upload_file_bucket = "nflpredictor-scrapy"
#upload_file_key = filename

#client.upload_file(path+filename,upload_file_bucket,upload_file_key)
