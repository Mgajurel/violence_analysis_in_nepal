import pandas as pd
import requests
import json
import re
import csv
import validators
import os
from collections import Counter
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from nepalitokanizer import NepaliTokenizer
from config import ratopati_re

domain_regex = re.compile(r'''^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n]+)''')
paragraph_regex = re.compile(r'''<p.*?>(.*?)</p>''', re.DOTALL | re.MULTILINE)

def read_news_csv(_path):
    news_df = pd.read_csv(_path)
    news_df = news_df['Source'].dropna()
    endpoints = news_df.to_list()
    return endpoints

def read_url_json(_path):
    with open(_path, 'r') as json_file:
        url_frequency_dict = json.load(json_file)
    return url_frequency_dict

def create_request_session():
    # Define the maximum number of retries
    max_retries = 2
    # Create a requests session object
    session = requests.Session()
    # Define the retry strategy
    retry_strategy = Retry(
        total=max_retries,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    # Mount the retry strategy to the requests session
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def make_request(endpoint, session, writer):
    response = session.get(endpoint)
    # Check the response status code
    if response.status_code == 200:
        # response.encoding = 'utf-8'
        find = ratopati_re.search(response.text)
        if find:
            title, date, content = find.group('title'), find.group('date'), find.group('main_news')
            info = paragraph_regex.findall(content)
            info = ' '.join(info)
            writer.writerow({
                'DATE': date,
                'TITLE': title,
                'MAIN_NEWS': info,
                'SOURCE_URL': endpoint
            })
            print("Request was successful")
        else:
            print("Regex Not working")
    else:
        print(endpoint)
        print("Request failed")


def get_max(url_frequency_dict):
    max_key = max(url_frequency_dict, key=lambda k: url_frequency_dict[k])
    url_frequency_dict.pop(max_key, None)
    return max_key

def create_freq_json(endpoints):
    domains = []
    for string in endpoints:
        match = domain_regex.search(string)
        if match:
            domains.append(match.groups(0))
    url_frequency_dict = dict(Counter(domains))
    automate_dict = { k[0]: v for k, v in url_frequency_dict.items() if v > 5}
    manual_dict = { k[0]: v for k, v in url_frequency_dict.items() if v <= 5}
    with open(os.path.join('..', 'config_json', 'automate_url_frequency.json'), mode='w') as json_file:
        json.dump(automate_dict ,json_file)
    with open(os.path.join('..', 'config_json', 'manual_url_frequency.json'), mode='w') as json_file:
        json.dump(manual_dict ,json_file)

def phase_2(endpoints):
    # PHASE 2 BEGIN
    session = create_request_session()
    with open(os.path.join('..', 'config_json', 'automate_url_frequency.json'), 'r') as j_file:
        url_frequency_dict = json.load(j_file)
    domain = get_max(url_frequency_dict)
    print(domain)
    required_endpoints = [end for end in endpoints if domain in end]
    with open('output.csv', mode='w', newline='') as csv_file:
        
        # Define the header row
        fieldnames = ['DATE', 'TITLE', 'MAIN_NEWS', 'SOURCE_URL']
        
        # Create the writer object
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        for end in required_endpoints:
            make_request(end, session, writer)
            # break
        # Write some data rows
    # PHASE 2 END

if __name__=='__main__':
    
    endpoints = read_news_csv(os.path.join('..','news.csv'))
    endpoints = [end for end in endpoints if validators.url(end)]
    # create_freq_json(endpoints)
    
    # print("URL FRQUENCY JSON CREATED")
    
    phase_2(endpoints)