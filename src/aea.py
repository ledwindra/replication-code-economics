import argparse
import json
import os
from typing import Type
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

def current_timestamp():
    '''
    Returns current timestamp for logging purposes
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def issue(journal):
    '''
    Returns all of issues for any journal in AEA
    '''
    url = f'https://www.aeaweb.org/journals/{journal}/issues'
    print(f'{current_timestamp()}: {url}')
    status_code = None
    while status_code != 200:
        try:
            res = requests.get(url, timeout=5)
            status_code = res.status_code
            content = BeautifulSoup(res.content, features='html.parser')
            journalprev = content.find('section', {'class': 'journal-preview-group'})
            issue = journalprev.find_all('a')
            issue = [x['href'] for x in issue]
        except Exception as e:
            print(f'{current_timestamp()}: {e}')
            sleep(3)

    return issue

def article(issue):
    '''
    Returns all of articles in the corresponding issue of any journal in AEA
    '''

    # we don't need to re-download existing files
    file_name = issue.replace('/issues/', '')
    if not os.path.exists(f'data/tmp/{file_name}.json'):
        url = f'https://www.aeaweb.org{issue}'
        print(f'{current_timestamp()}: {url}')
        status_code = None
        while status_code != 200:
            try:
                res = requests.get(url, timeout=5)
                status_code = res.status_code
                content = BeautifulSoup(res.content, features='html.parser')
                article = content.find_all('article')
                articles = []
                for a in article:
                    try:
                        articles.append(a.find('a')['href'])
                    except TypeError:
                        pass
                article = {
                    'issue_url': url,
                    'publication_date': content.find('meta', {'name': 'citation_publication_date'})['content'],
                    'article': articles
                }
                with open(f'data/tmp/{file_name}.json', 'w') as f:
                    json.dump(article, f, indent=4)
            except Exception as e:
                print(f'{current_timestamp()}: {e}')
                sleep(3)

def paper(issue):
    '''
    Returns all of papers and whether or not they have replication materials in ICPSR
    '''

    # we don't need to re-download existing files
    file_name = issue.replace('/issues/', '')
    if not os.path.exists(f'data/aea/{file_name}.json'):
        with open(f'data/tmp/{issue}', 'r') as f:
            data = json.load(f)
        
        articles = []
        for article in data['article']:
            url = f'https://www.aeaweb.org{article}'
            print(f'{current_timestamp()}: {url}')
            status_code = None
            while status_code != 200:
                try:
                    res = requests.get(url, timeout=5)
                    status_code = res.status_code
                    content = BeautifulSoup(res.content, features='html.parser')
                    icpsr = content.find('a', {'class': 'track-icpsr'})
                    try:
                        icpsr = icpsr['href']
                    except TypeError:
                        icpsr = None
                except Exception as e:
                    print(f'{current_timestamp()}: {e}')
                    sleep(3)

            articles.append({
                'url': url,
                'icpsr': icpsr
            })

        # the reason i update the dictionary is to update the value
        # whether any paper has any replication material in ICPSR
        # if nothing the corresponding paper will have null value
        articles = {'article': articles}
        data.update(articles)
        file_name = issue.replace('/issues/', '')
        with open(f'data/aea/{file_name}', 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == '__main__':
    journals = [
        'aer',
        'aeri',
        'app',
        'pol',
        'mac',
        'mic',
        'jel',
        'jep',
        'pandp'
    ]
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-j', '--journal', type=str, choices=journals, help=f'Journal name: {journals}', metavar='')
    ARGS = PARSER.parse_args()
    JOURNAL = ARGS.journal
    issues = sorted(issue(journal=JOURNAL))
    articles = [article(x) for x in issues]
    issues = sorted(os.listdir('data/tmp'))
    [paper(x) for x in issues]
    os.rmdir('data/tmp')