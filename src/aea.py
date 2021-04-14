import argparse
import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

def issue(journal):
    url = f'https://www.aeaweb.org/journals/{journal}/issues'
    status_code = None
    while status_code != 200:
        try:
            res = requests.get(url)
            status_code = res.status_code
            content = BeautifulSoup(res.content, features='html.parser')
            journalprev = content.find('section', {'class': 'journal-preview-group'})
            issue = journalprev.find_all('a')
            issue = [x['href'] for x in issue]
        except Exception as e:
            print(e)

    return issue

def article(issue):
    url = f'https://www.aeaweb.org{issue}'
    status_code = None
    while status_code != 200:
        try:
            res = requests.get(url)
            status_code = res.status_code
            content = BeautifulSoup(res.content, features='html.parser')
            article = content.find_all('article')
        except Exception as e:
            print(e)
    try:
        article = {
            'issue_url': url,
            'publication_date': content.find('meta', {'name': 'citation_publication_date'})['content'],
            'article': [x.find('a')['href'] for x in article]
        }
        file_name = issue.replace('/issues/', '')
        with open(f'data/issue/{file_name}.json', 'w') as f:
            json.dump(article, f, indent=4)
    except TypeError:
        return None

def paper(issue):
    with open(f'data/issue/{issue}', 'r') as f:
        data = json.load(f)
    
    articles = []
    for article in data['article']:
        url = f'https://www.aeaweb.org{article}'
        status_code = None
        while status_code != 200:
            try:
                res = requests.get(url)
                status_code = res.status_code
                content = BeautifulSoup(res.content, features='html.parser')
                icpsr = content.find('a', {'class': 'track-icpsr'})
            except Exception as e:
                print(e)
        try:
            icpsr = icpsr['href']
        except TypeError:
            icpsr = None
        
        articles.append({
            'url': url,
            'icpsr': icpsr
        })

    articles = {'article': articles}
    data.update(articles)
    file_name = issue.replace('/issues/', '')
    with open(f'data/issue/{file_name}', 'w') as f:
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
    issues = issue(journal=JOURNAL)
    articles = [article(x) for x in issues]
    issues = os.listdir('data/issue')
    [paper(x) for x in issues]