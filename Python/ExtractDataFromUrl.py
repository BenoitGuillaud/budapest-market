# import packages
import urllib.request
import re
from bs4 import BeautifulSoup
import csv

# define filename(s)
urls_file = "elado_urls_2017_05_17(2).txt"   # contains urls to open
out_file = "extraction_elado_2017_05_17(2).txt"        # output file with data

with open(out_file, 'w', newline='\n', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')

    with open(urls_file) as urls:
        err_count = 0
        count = 1

        for url in urls:
            # create soup from url with exception handling
            try:
                page = urllib.request.urlopen(url).read()
                soup = BeautifulSoup(page, 'html.parser')  # lxml, html.parser, html5lib
                print(url.strip('\n'), '  (iteration ', count,')')


                # meta
                meta = soup.find_all('meta')[4]['content']
                meta = meta.replace('\n', '')

                # district
                district_regex = re.compile("(\d+\.\sker).let")
                if district_regex.search(meta) is None:
                    district = ''
                else:
                    district = district_regex.search(meta).group(1)

                # varos
                varos_regex = re.compile("\(([A-Z].+)\)")
                if varos_regex.search(meta) is None:
                    varos = ''
                else:
                    varos = varos_regex.search(meta).group(1)

                # title
                title = soup.find('title').string  # title = soup.find('title').get_text()
                title = title.replace('\n', '')

                # price
                price_regex = re.compile("Ft")
                price = soup.find(text=price_regex)

                price_regex = re.compile("(\d+,?\d+)")
                price = price_regex.search(price).group(1).replace(" Ft", "")
                price = price_regex.search(price).group(1).replace(",", ".")

                # area
                area_regex = re.compile("\u006d\u00b2", re.UNICODE)  # unicode for m²
                area = soup.find(text=area_regex)

                area_regex = re.compile("(\d+)")
                area = area_regex.search(area).group(1)

                # rooms: full-rooms and half-rooms
                rooms_regex = re.compile("szoba")
                rooms = soup.find(text=rooms_regex)

                fullrooms_regex = re.compile("^(\d+)")
                if fullrooms_regex.search(rooms) is None:
                    fullrooms = 0
                else:
                    fullrooms = fullrooms_regex.search(rooms).group(1)

                halfrooms_regex = re.compile("\+(\s?)(\d?).+fél")# ("\+.+(\d).+fél")
                if halfrooms_regex.search(rooms) is None:
                    halfrooms = 0
                elif halfrooms_regex.search(rooms).group(1) == '':
                    halfrooms = 1
                else:
                    halfrooms = halfrooms_regex.search(rooms).group(2)

                # coord: lat and long
                coord_regex = re.compile("center")
                coord = str(soup.find_all(src=coord_regex))

                lat_regex = re.compile("(47\.\d+),")
                lat = lat_regex.search(coord).group(1)
                long_regex = re.compile("(19\.\d+)")
                long = long_regex.search(coord).group(1)

                # listing
                listing = soup.find('b', class_="listing-id").string

                # floor, lift, heating, view
                condition = ''
                floor = ''
                storeys = ''
                lift = ''
                ceiling = ''
                heating = ''
                aircon = ''
                bathtoil = ''
                orient = ''
                view = ''
                balcony = ''
                parking = ''
                garcess = ''
                utility = ''
                for td in soup.find_all('td'):
                    if td.string == "Ingatlan állapota":
                        condition = td.next_element.next_element.next_element.string
                    elif td.string == "Emelet":
                        floor = td.next_element.next_element.next_element.string
                    elif td.string == "Épület szintjei":
                        storeys = td.next_element.next_element.next_element.string
                    elif td.string == "Lift":
                        lift = td.next_element.next_element.next_element.string
                    elif td.string == "Belmagasság":
                        ceiling = td.next_element.next_element.next_element.string
                    elif td.string == "Fűtés":
                        heating = td.next_element.next_element.next_element.string
                    elif td.string == "Légkondicionáló":
                        aircon = td.next_element.next_element.next_element.string
                    elif td.string == "Fürdő és WC":
                        bathtoil = td.next_element.next_element.next_element.string
                    elif td.string == "Tájolás":
                        orient = td.next_element.next_element.next_element.string
                    elif td.string == "Kilátás":
                        view = td.next_element.next_element.next_element.string
                    elif td.string == "Erkély":
                        balcony = td.next_element.next_element.next_element.string
                        bal_regex = re.compile("(\d+\.?\d+)")
                        if bal_regex.search(balcony) is None:
                            balcony = 0
                        else:
                            balcony = bal_regex.search(balcony).group(1)
                    elif td.string == "Parkolás":
                        parking = td.next_element.next_element.next_element.string
                    elif td.string == "Tetőtér":
                        garcess = td.next_element.next_element.next_element.string
                    elif td.string == "Komfort":
                        utility = td.next_element.next_element.next_element.string

                # build list with all feature values and write in file
                values = [
                    [listing, price, area, rooms, fullrooms, halfrooms, district, varos,
                     condition, floor, storeys, lift, heating, view, lat, long, orient,
                     parking, balcony, aircon, ceiling, utility, bathtoil, garcess]
                ]

                writer.writerows(values)
                count = count + 1
                
            except:
                print("Error with url: ", url)
                err_count = err_count + 1
                continue  # returns to beginning of for-loop

    print("Number of errors: ", err_count)
