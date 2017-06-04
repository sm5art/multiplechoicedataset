import requests
import urllib
import re
from bs4 import BeautifulSoup

class GoogleSearch(object):
    def __init__(self):
        self.base_url = "https://www.google.com/search?q="
    """
    arguments: subject and dictionary containing all the dorks with key being the dork and the value being the dork value.
    returns: list of queried links and other information
    """
    def query_dork(self, subject, dorks):
        full_query = "%s " % subject
        for key in dorks:
            full_query += "{}: {} ".format(key, dorks[key])
        print full_query
        self.raw_query(full_query)


    def raw_query(self, query):
        full_url = self.base_url + urllib.quote_plus(query)
        req = requests.get(full_url)
        print self.process_response(req.text)

    def process_response(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        links = soup.find_all("div", class_="g")
        output = []
        pattern = re.compile("((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$")
        for link in links:
            a = link.find('a')
            we = pattern.findall(a['href'])[0]
            if len(we) > 6:
                full = "".join([ we[0], we[2], we[3], we[5], we[6] ])
                output.append(full)
        return output
