# import packages
import urllib.request
import re
from bs4 import BeautifulSoup
import csv

# define ingatlan query url
query_url = "http://ingatlan.com/listar/elado+lakas+nem-berleti-jog+tegla-epitesu-lakas+budapest+v-vi-vii-ker"

# define the number of pages (from manual search)
npages = 199

# define filename(s)
out_filename = "kiado_urls_2017_05_17.txt"


with open(out_filename, 'w', newline='\n', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')

    err_count = 0
    for page in range(1,npages+1):
        # create url to parse
        url = query_url + '?page=' + str(page)
        print(url)

        # create soup from url with exception handling
        try:
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html,'lxml') #lxml, html.parser, html5lib
        except:
            print("Error with url: ",url)
            err_count = err_count + 1
            continue # returns to beginning of for-loop

        # retrieve all listings urls in the html (tag <a title="Details" href=xxx)
        tags_a = soup.find_all('a', class_='rowclick rowClickCSS', href=True)

        # build a list of all urls
        href_list = list()
        for tag in tags_a:
            regex = re.compile("/(\d+)#?")
            href = "http://ingatlan.com/" + regex.search(tag['href']).group(1)
            href_list.append(href)

        # removes duplicates
        href_list = list(set(href_list))

        # write to file
        for href in href_list:
            writer.writerow([href])

print("Error count =", err_count)