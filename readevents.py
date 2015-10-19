# -*- coding: utf-8 -*-
import re
import requests
from lxml import html

def readevents(url):
    page = requests.get(url)

    tree = html.fromstring(page.text)
    events = tree.xpath('//li[@class="ev_td_li"]')

    # get times
    times = map(lambda x: filter(lambda c: c not in u'\n\xa0\t', x.text), events)

    # get event names
    names = map(lambda e: e.xpath('a[@class="ev_link_row"]/text()')[0], events)

    pat = re.compile(r'var addy_text\d+ = \'(.*?)\'')
    def getorganization(e):
        start = e.text_content().find('var addy_text')
        end = e.text_content()[start:].find(';') + start
        code = str(e.text_content()[start:end])

        m = pat.match(code)
        return m.group(1)

    organizations = map(lambda e: getorganization(e.xpath('i')[0]), events)

    categories = map(lambda e: e.xpath('a[@class="ev_link_cat"]/text()')[0], events)


    return zip(times, names, organizations, categories)

if __name__ == "__main__":
    import sys
    from datetourl import datetourl
    from tabulate import tabulate

    url = datetourl(sys.argv[1])
    print 'url: %s' % url

    print tabulate(readevents(url))
