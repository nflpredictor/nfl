
from os import link
import os
from unicodedata import name
import logging
import json
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import pandas as pd

# open file with url


my_file = open("url_list_secours.txt", "r")
content = my_file.read()
list_urls = content.split("\n")[:-1]



# df = pd.read_json("espn_scores.json")

# list_url = list(df["gamecast"])

class ESPNGamesCastHelpSpider(scrapy.Spider):

    name = 'espngamescasthelp'

    # Url to start your spider from 
    #example : ['https://www.espn.com/nfl/game/_/gameId/401326129']
    start_urls = list_urls

    # Callback function that will be called when starting your spider
    
    def parse(self, response):

        # split url to recover idgame   
        split_url = response.url.split("gameId/")
        
        
        yield {

            "idgame" : split_url[-1],           
                                    #//*[@id="gamepackage-game-information"]/article/div/div[1]/div/div[2]  
                                    # //*[@id="gamepackage-game-information"]/article/div/div[1]/div/div[1]/span/@data-date'
            "date" :  response.xpath('//*[@id="gamepackage-game-information"]/article/div/div[1]/div/div[2]/span/@data-date').get(),
                                    
                                    
                                    #//*[@id="gamepackage-game-information"]/article/div/div[1]/div/div[1]
                                    # '//*[@id="gamepackage-game-information"]/article/div/div[1]/figure/figcaption/div/text()').get().strip(),
            "stade" : response.xpath('//*[@id="gamepackage-game-information"]/article/div/div[1]/div/div[1]/text()').get(),
               
            "location" : response.xpath('//*[@id="gamepackage-game-information"]/article/div/div[2]/ul/li/div/text()').get().strip(),

                                            
            "attendance" : response.xpath('//*[@id="gamepackage-game-information"]/article/div/div[2]/div[@class="game-info-note capacity"]/text()').get(),
            "capacity" : response.xpath('//*[@id="gamepackage-game-information"]/article/div/div[2]/div[@class="attendance"]/div[@class="game-info-note capacity"]/text()').get(),

                                        
            "people" : response.xpath('//*[@id="gamepackage-game-information"]/article/div/div[2]/div[@class="attendance"]/span/text()').get(),
            # NFL odds                       
            "line" : response.xpath('//*[@id="gamepackage-game-information"]/article/div/div[2]/div[1]/div[1]/ul/li[1]/text()').get(),
            # Over/under predictions usually involve the number of goals scored in a football match
            "over_under" :  response.xpath('//*[@id="gamepackage-game-information"]/article/div/div[2]/div[1]/div[1]/ul/li[2]/text()').get(),
            
                                       
            }
        

# Name of the file where the results will be saved
filename = "json/gamescast_2.json"

# if th file exist, remove this
if filename in os.listdir():
     os.remove(filename)



# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    #'FEED FORMAT' : ,
    'FEED URI' : '../../json/',
    "FEEDS": {
        filename : {"format": "json"},
    },
    "AUTOTHROTTLE_ENABLED" : False
})

# Start the crawling using the spider you defined above
process.crawl(ESPNGamesCastHelpSpider)
process.start()
