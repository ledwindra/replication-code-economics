import argparse
import crossref_commons.retrieval
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

def repec_page(base, journal):
    '''
    Returns total page for a certain journal in RePEc
    '''

    repec = f'{base}/{journal}.html'
    print(f'{current_timestamp()}: {repec}')
    status_code = []
    while status_code != 200:
        try:
            res = requests.get(repec, timeout=5)
            status_code = res.status_code
            content = BeautifulSoup(res.content, features='html.parser')
            pagination = content.find('ul', {'class': 'pagination flex-wrap'})
            href = [x for x in pagination.find_all('a')]
            urls = []
            for h in href:
                try:
                    urls.append(h['href'])
                except KeyError:
                    pass
        except Exception as e:
            sleep(3)
        urls = set(urls)
        return len(urls)

def repec_paper(base, page, journal):
    '''
    Returns a list of paper URLs from RePEc.
    Examples:
        - https://ideas.repec.org/a/oup/restud/v87y2020i6p2511-2541..html
        - https://ideas.repec.org/a/oup/restud/v87y2020i6p2473-2510..html
    '''

    url = f'{base}/{journal}.html'
    if page > 1:
        url = f'{base}/{journal}{page}.html'
    print(f'{current_timestamp()}: {url}')
    status_code = []
    while status_code != 200:
        try:
            res = requests.get(url, timeout=5)
            status_code = res.status_code
            content = BeautifulSoup(res.content, features='html.parser')
            content = content.find('div', {'id': 'content'})
            href = content.find_all('a')
            urls = []
            for h in href:
                try:
                    urls.append(h['href'])
                except KeyError:
                    pass
        except Exception as e:
            sleep(3)
    
    return urls

def download(base, paper):
    '''
    Returns download URL from RePEc.
    Examples:
        - http://hdl.handle.net/10.1093/restud/rdaa026
        - http://hdl.handle.net/10.1093/restud/rdz066
    '''

    url = f'{base}/{paper}'
    print(f'{current_timestamp()}: {url}')
    res = requests.get(url, timeout=5)
    content = BeautifulSoup(res.content, features='html.parser')
    download = content.find('div', {'id': 'download'})

    return download

def crossref(download, path):
    '''
    Download metadata from Crossref into a JSON file
    '''
    try:
        paper = download.find('input', {'type': 'radio'})['value']
        inputval = {
            'https://hdl.handle.net/': 'https://doi.org/',
            'http://hdl.handle.net/': 'https://doi.org/'
        }
        for key, value in inputval.items():
            paper = paper.replace(key, 'https://doi.org/')
        print(f'{current_timestamp()}: {paper}')
        file_name = paper.replace('https://doi.org/', '')
        file_name = file_name.replace('/', '-')
        # no need to re-download existing file
        if not os.path.exists(f'{path}/{file_name}.json'):
            try:
                paper = crossref_commons.retrieval.get_publication_as_json(paper)
                sleep(3)
                with open(f'{path}/{file_name}.json', 'w') as f:
                    json.dump(paper, f, indent=4)
            except ValueError:
                print(f'DOI {paper} does not exist')
    except AttributeError:
        pass

if __name__ == '__main__':
    journals = [
        # These are not an exhaustive list
        's/aea/aecrev', # American Economic Review
        's/aea/jeclit', # Journal of Economic Literature
        's/aea/jecper', # Journal of Economic Perspectives
        's/eee/jfinec', # Journal of Financial Economics
        's/kap/jecgro', # Journal of Economic Growth
        's/oup/qjecon', # The Quarterly Journal of Economics
        's/oup/restud', # Oxford University Press
        's/oup/rfinst', # Review of Financial Studies
        's/ucp/jpolec', # Journal of Political Economy
        's/wly/emetrp' # Econometrica
    ]
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-j', '--journal', type=str, choices=journals, help=f'Journal name: {journals}', metavar='')
    ARGS = PARSER.parse_args()
    JOURNAL = ARGS.journal
    PATH = f"data/crossref/{JOURNAL.replace('/', '-')}"
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    BASE = 'https://ideas.repec.org'
    page = repec_page(BASE, JOURNAL)
    paper = [repec_paper(BASE, x, JOURNAL) for x in range(1, page+1)]
    papers = []
    for i in paper:
        for j in i:
            papers.append(j)
    download = [download(BASE, x) for x in papers]
    crossref = [crossref(x, PATH) for x in download]
