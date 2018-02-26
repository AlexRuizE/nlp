""" Classes to obtain, process and classify local newspapers in Mexico. 
Specific publications as all sub-classes of the main class GetText, 
which should not be used on its own but only as a master template."""

import requests
import bs4
import os
import json
import datetime
import re
import string
import random


class GetText():
    def __init__(self):
        """Base class for all publications to be scraped.
        Initializes a list to be populated with article URL's, a dictionary
        where values will be text of articles, and an exception-counter for monitoring.
        This class should not be used by itself, only as superclass."""
        self.urls = []
        self.d = {}
        self.exceptions = {}

    def load_data(self):
        """Load existing data, if exists."""
        if os.path.exists(self.raw_loc):
            with open(self.raw_loc, 'r') as f:
                self.d = json.load(f)

    def get_html(self, url):
        """Get parsable HTML from given URL."""
        html = requests.get(url)
        status = 'Page status code: {}. Reason: {}.'.format(html.status_code, html.reason)
        if html.status_code == 200:
            html = bs4.BeautifulSoup(html.text, 'lxml')
            print(status)
            return html
        else:
            raise RuntimeError(status)

    def hub_links(self, page_num):
        """Get URLs from hub page."""
        page_num = str(page_num)
        hub = ''.join([self.base_url, self.section, page_num])
        html = self.get_html(hub)
        elements = html.find_all(self.tag_, class_= self.class_, href=True)
        try:
            urls = [element['href'] for element in elements]
            if len(urls) is not 0:
                print('{} page {} SUCCESSFULL.\n'.format(self.publication.upper(), page_num))
                return urls
            else:
                raise RuntimeError('Empty result for page {}'.format(page_num))
        except KeyError:
            raise KeyError('No URLs in hub page {}.'.format(page_num))

    def get_article(self, html):
        """Get content from a specific URL."""
        content = [p.text for p in html.find_all('div', class_=self.class_text)]
        if len(content) == 1: # List should have a single element (the content).
            content = self.clean_string(content[0])
            return content
        else:
            raise RuntimeError('This article list has too many or too few cases.') # in page {url}.'.format(page_num)

    def clean_string(self, a_string):
        """Mild cleanup."""
        a_string = re.sub('/',u' ', a_string)
        a_string = re.sub('\s{2,}',u' ', a_string)
        a_string = re.sub('\'s',u'', a_string)
        a_string = re.sub('\n', ' ', a_string)
        a_string = a_string.replace(u'\xa0', u' ')
        a_string = a_string.split(' ')
        for element in a_string:
            if len(element) == 0: # 0 is empty string, 20 is to avoid urls and other garbage.
                a_string.remove(element)
            elif len(element)>20:
                a_string.remove(element)
        a_string = ' '.join(a_string)
        return a_string

    def unique_id(self):
        """Generate unique random ID per article per publication."""
        random_str = ''.join(random.choices(string.ascii_letters, k=10))
        while random_str in self.d: # Guarantee unique IDs.
            random_str = ''.join(random.choices(string.ascii_letters, k=10))
        return '_'.join([self.id_str, random_str])

    def is_in_dict(self, url):
        return any(url in self.d[k].values() for k in self.d if k!='last_updated')

    def get_date(self, html):
        """Get date from a specific URL. Looks at the ratio of digits to alphanumeric characters
        to attempt to identify the most likely date from other elements with the same tag."""
        date = [p.text for p in html.find_all(self.tag_date, class_=self.class_date)]
        num_digits = [sum(map(str.isdigit, i)) for i in date]
        num_char = [len(p) for p in date]
        most_likely_date = [p for p in map(lambda x,y:x/y, num_digits,num_char)]
        most_likely_date = most_likely_date.index(max(most_likely_date))
        date = date[most_likely_date].strip()
        return date

    def last_updated(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def save_json(self):
        """Save dictionary with text in specified path as json. Pat and dictionary
        are init values from GetText subclasses."""
        with open(self.raw_loc, 'w') as f: #TODO CREATE FOLDER WITH HISTORICAL BACKUPS.
            json.dump(self.d, f)

    def dump_text(self, k):
        """Move raw text from json to text file for processing."""
        with open(self.processed_loc+k+'.txt','w') as f:
            f.write(self.d[k]['content'])

    def get_text_files(self):
        """List of files which already have been dumped as text from raw json."""
        return os.listdir(self.processed_loc)

# Subclasses for specific publications.
class VozMich(GetText):
    """La Voz de Michoacan. Subclass with specifics to this publication"""
    def __init__(self):
        super().__init__()
        self.publication = 'La Voz de Michoacan'
        self.id_str = 'vm'
        self.base_url = 'http://www.lavozdemichoacan.com.mx'
        self.section = '/seccion/seguridad/page/'
        self.raw_loc = 'data/raw/voz_de_michoacan.json' # Clean raw data
        self.processed_loc = 'data/processed/vm/' # Text/annotated
        self.tag_ = 'a'
        self.class_ = 'noteTitle'
        self.class_text = 'contentS'
        self.tag_date = 'p'
        self.class_date = 'dateS'
