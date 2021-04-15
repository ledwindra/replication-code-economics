import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

def current_timestamp():
    '''
    Returns current timestamp for logging purposes
    '''
    
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def icpsr(file_name):
    '''
    Returns a list of DOIs in ICPSR
    '''

    with open(f'data/aea/{file_name}', 'r') as f:
        data = json.load(f)
        
    icpsr = [x['icpsr'] for x in data['article']]
    icpsr = [x for x in icpsr if x != None]

    return icpsr

def get_metadata(url):
    '''
    Download ICPSR metadata (Dublin Core)
    '''

    status_code = []
    while status_code not in [200, 404]:
        try:
            res = requests.get(url, timeout=5)
            status_code = res.status_code
            content = BeautifulSoup(res.content, features='html.parser')
            well = content.find_all('div', {'class': 'well'})
            for i in range(len(well)):
                try:
                    if well[i].find('h2', {'class': 'asideH2'}).text == 'Export Metadata':
                        well = well[i]
                        metadata = [x['href'] for x in well.find_all('a')]
                        return metadata[0]
                except AttributeError:
                    pass
        except Exception as e:
            print(f'{current_timestamp()}: {e}')
            sleep(3)
            continue

def parse_metadata(metadata):
    '''
    Parses metadata and returns into a JSON file
    '''

    status_code = []
    while status_code not in [200, 404]:
        try:
            res = requests.get(metadata, timeout=5)
            status_code = res.status_code
            content = BeautifulSoup(res.content, features='xml')
            try:
                file_name = content.find('identifier').text
                if not os.path.exists(f'data/aea-metadata/{file_name}.json'):
                    metadata = {
                        'datestamp': content.find('datestamp').text,
                        'title': content.find('title').text,
                        'creator': content.find('creator').text,
                        'identifier': [x.text for x in content.find_all('identifier')],
                        'description': content.find('description').text,
                        'subject': [x.text for x in content.find_all('subject')]
                    }
                    with open(f'data/aea-metadata/{file_name}.json', 'w') as f:
                        json.dump(metadata, f, indent=4)
            except AttributeError:
                pass
        except Exception as e:
            print(f'{current_timestamp()}: {e}')
            sleep(3)
            continue

if __name__ == '__main__':
    aea = os.listdir('data/aea/')
    icpsr = [icpsr(x) for x in aea]
    urls = []
    for i in icpsr:
        for j in i:
            if j != '':
                urls.append(j)
    for u in urls:
        print(f'{current_timestamp()}: {u}')
        parse_metadata(get_metadata(u))
