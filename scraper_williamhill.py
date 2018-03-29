from bs4 import BeautifulSoup
import urllib2
import re

url = "http://sports.williamhill.com/bet/en-gb/betting/t/295/English+Premier+League.html"
response = urllib2.urlopen(url)
page_source = response.read()
soup = BeautifulSoup(page_source, "lxml")


containers = soup.findAll("table", {"class": "tableData"})
resultsAndOdds = []
regex   =   re.compile('.*mkt_namespace.*')
for container in containers:
    tbodys = container.findAll("tbody")
    for tbody in tbodys:
        trs =   tbody.findAll("tr",{"class":"rowOdd"})
        for tr in trs:
            names = tr.findAll("a",{"title":None})
            for name in names:
                print name.text

            divs  = tr.findAll("div",{"class":"eventprice"})
            for div in divs:
                print div.text
                print ord(div.text[23])
                for i in xrange (0,len(div.text)):
                    print str(i) + '  ---->   ' + str(div.text[i])
                if div.text[20] == '/':
                    print float((float(div.text[19]) + float(div.text[21]) ) / float(div.text[21]))
                elif div.text[21] == '/' and ord(div.text[23]) == 9:

                    print float((float(div.text[19])*10 + float(div.text[20]) + float(div.text[22]) ) / float(div.text[22]))

                elif div.text[21] == '/' and ord(div.text[23]) != 9:

                    print float((float(div.text[19])*10 + float(div.text[20]) + float(div.text[22])*10 + float(div.text[23]) ) / (float(div.text[22])*10 + float(div.text[23])  ))

            








