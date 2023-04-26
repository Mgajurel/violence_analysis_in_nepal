import pandas as pd
import requests
import csv
import validators
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from nepalitokanizer import NepaliTokenizer
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import configparser

config = configparser.ConfigParser()
config.read(os.path.join('..', 'config_json', 'news_tags.ini'))

def read_news_csv(_path):
    news_df = pd.read_csv(_path)
    date_df = news_df['Publication Date']
    endpoint_df = news_df['Source'].dropna()
    endpoints = endpoint_df.to_list()
    date = date_df.to_list()
    _list = list(zip(date, endpoints))
    return _list

def create_request_session():
    # Disable InsecureRequestWarning
    urllib3.disable_warnings(InsecureRequestWarning)

    # Create a session object
    session = requests.Session()

    # Create an HTTPAdapter object with retry strategy and SSL verification disabled
    retry_strategy = Retry(
        total=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=1, pool_maxsize=1, pool_block=True)
    adapter.poolmanager.pool_classes_by_scheme['https'].verify = False
    adapter.poolmanager.pool_classes_by_scheme['http'].verify = False
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    return session


def make_request(date, endpoint, session, domain, writer):
    response = session.get(endpoint)
    # Check the response status code
    if response.status_code == 200:
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        header_tag = config[domain]['header_tag']
        body_tag = config[domain]['body_tag']
        body_class = config[domain]['body_class']
        title = soup.find(header_tag)
        # div_class = soup.find('div', {'class': 'nws__title--card'})
        # title = ''
        # if div_class:
        #     title = div_class.find('h2')

        if not title:
            title = "SEE TITLE IN LINK"
        try:
            title = title.text.strip()
            div_container = soup.find(body_tag, {'class': body_class})
            content = ''
            if div_container:
                p_element = div_container.find_all('p')
                for p in p_element:
                    content += p.text.strip() + ' '
            content = content.replace('\n', '')
            content = content.replace(' ', '')
            title = title.replace('\n', '')
        except AttributeError:
            print("No Div" )
            print(endpoint)
        else:
            writer.writerow({
                'DATE': date,
                'TITLE': title,
                'MAIN_NEWS': content,
                'SOURCE_URL': endpoint
            })
            print("Request was successful")
    else:
        print(endpoint)
        print("Request failed")

def run(valid_date_endpoints, domain):
    # PHASE 2 BEGIN
    session = create_request_session()
    required_date_endpoints = [(date, url) for date, url in valid_date_endpoints if domain in url]
    with open('output.csv', mode='w', newline='') as csv_file:
        # Define the header row
        fieldnames = ['DATE', 'TITLE', 'MAIN_NEWS', 'SOURCE_URL']
        
        # Create the writer object
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        for date, end in required_date_endpoints:
            make_request(date, end, session, domain, writer)
            # break
    # PHASE 2 END

if __name__=='__main__':
    date_endpoints = read_news_csv(os.path.join('..','news.csv'))
    valid_date_endpoints = [(date, url) for date, url in date_endpoints if validators.url(url)]
    domains = config.sections()
    for domain in domains:
        print(domain)
        run(valid_date_endpoints, domain)
        break