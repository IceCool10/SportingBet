from selenium import webdriver
from bs4 import BeautifulSoup
import urllib2

url = "https://sports.bwin.com/en/sports/4/46/betting/premier-league#leagueIds=46&sportId=4"
response = urllib2.urlopen(url)
page_source = response.read()
soup = BeautifulSoup(page_source, "lxml")

containers = soup.findAll("table", {"class": "marketboard-event-without-header__markets-list"})


resultAndOdds = []
for container in containers:
    divs = container.findAll('div')
    texts = [div.text  for div in divs if div.text != "\n\n"]
    it = iter(texts)
    resultAndOdds.append(list(zip(it, it)))
    print texts

titlesElements = soup.findAll("div", {"class":"mb-option-button__option-name mb-option-button__option-name--odds-4"})
titlesTexts = [title.text for title in titlesElements]
oddsElements   = soup.findAll("div", {"class":"mb-option-button__option-odds"})
oddsTexts   = [title.text for title in oddsElements]
#print "OddsText : " + str(oddsTexts)
#print "Title Texts : " + str(titlesTexts)
print "resultAndOdds : " + str(resultAndOdds)
