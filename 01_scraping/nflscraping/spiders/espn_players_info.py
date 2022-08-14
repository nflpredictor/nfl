from os import link
from types import NoneType
from unicodedata import name
import json
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
import os
import logging
import boto3
import urllib.request
from credentials import access_key,secret_access_key

class ESPNPlayersInfoSpider(scrapy.Spider):
    name = 'espnplayersinfo'
    #print(os.listdir())
    def __init__(self):

        s3 = boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)
        s3_obj = s3.get_object(Bucket='nflpredictor-scrapy', Key='espn_players_urls.json')
        json_data = s3_obj["Body"].read().decode('utf-8')
        self.data = json.loads(json_data)
        #with open('01_scraping/json/espn_players_urls.json', encoding='utf-8') as data_file:
        #   self.data = json.load(data_file)

    def start_requests(self):
        for i in self.data:
            request = scrapy.Request(self.data[i], callback=self.parse)
            yield request

    def parse(self, response):
        split = response.url.split("/")
        if bool(response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[3]/text()').get()):
            yield{
                "id player" : split[7],
                "url" : response.url,
                "first name" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/h1/span[1]/text()').get(),
                "last name" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/h1/span[2]/text()').get(),
                "actual team" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[1]/a/text()').get(),
                "status" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[5]/div[2]/div/span/text()').get(),
                "team url" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[1]/a/@href').get(),
                "#" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[2]/text()').get(),
                "position" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[3]/text()').get(),
                "HT/WT" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[1]/div[2]/div/text()').get(),
                "Birthdate" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[2]/div[2]/div/text()').get(),
                "College" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[3]/div[2]/div/a/text()').get(),
                "Draft" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[4]/div[2]/div/text()').get(),
                "Fantasy Draft Rank" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[2]/div[2]/section/div/div[1]/div[1]/div[2]/span/text()').get(),
                "Fantasy '%' rostered" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[2]/div[2]/section/div/div[1]/div[2]/div[2]/span/text()').get()
            }
        else:
            yield{
               "id player" : split[7],
                "url" : response.url,
                "first name" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/h1/span[1]/text()').get(),
                "last name" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/h1/span[2]/text()').get(),
                "actual team" : 'retired',
                "status" : 'retired',
                "team url" : 'retired',
                "#" : 'retired',
                "position" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li/text()').get(),
                "Birthdate" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[2]/div[2]/div/text()').get(),
                "College" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[3]/div[2]/div/a/text()').get(),
            }

# Name of the file where the results will be saved
path="01_scraping/json/"
filename = "espn_players_info.json"

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
    'FEED URI': path,
    "FEEDS": {
        path+filename : {"format": "json"},
    },
    "AUTOTHROTTLE_ENABLED" : False
})

#process = CrawlerProcess()
process.crawl(ESPNPlayersInfoSpider)
process.start()

client = boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)
upload_file_bucket = "nflpredictor-scrapy"
upload_file_key = filename
client.upload_file(path+filename,upload_file_bucket,upload_file_key)