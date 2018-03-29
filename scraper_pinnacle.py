from bs4 import BeautifulSoup
import urllib2
import re

url = "https://www.pinnacle.com/en/odds/match/soccer/england/england-premier-league?sport=True"
response = urllib2.urlopen(url)
page_source = response.read()
soup = BeautifulSoup(page_source, "lxml")


containers = soup.findAll("table", {"class": "odds-data"})

resultsAndOdds = []
regex   =   re.compile('.*ng-if.*')
for container in containers:
    tds = container.findAll("td",{"class": "game-name name"})
    for td in tds:
        print td
        names = td.findAll("span")
        for name in names:
            print name














