import json
import pandas as pd
import boto3
from botocore.client import Config as BotoConfig
#from credentials import access_key,secret_access_key
import os

s3 = boto3.client('s3',aws_access_key_id=os.environ['AWS_ACCESS_KEY'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
s3_obj = s3.get_object(Bucket='nflpredictor-scrapy', Key='espn_rosters.json')
json_data = s3_obj["Body"].read().decode('utf-8')
data = json.loads(json_data)

urls = []
url_dict = {}

for url in data:
    urls.append(url['player_url'])
urls = list(set(urls))    

urls_dict = { i : urls[i] for i in range(0, len(urls)) }
#urls_dict

# Name of the file where the results will be saved
path="01_scraping/json/"
filename = "espn_players_urls.json"

# if the file exist, remove this
if filename in os.listdir(path):
    os.remove(path+filename)

with open(path+filename, "w") as outfile:
    json.dump(urls_dict, outfile, indent=3)

client = boto3.client('s3',aws_access_key_id=os.environ['AWS_ACCESS_KEY'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
upload_file_bucket = "nflpredictor-scrapy"
upload_file_key = filename
client.upload_file(path+filename,upload_file_bucket,upload_file_key)