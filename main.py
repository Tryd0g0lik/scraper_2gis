# This is a sample Python script.
from app_scraper_gis.scrape_paginator import Gis_paginator
from app_scraper_gis.scraper_address import ScraperEachAddress
import time
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    city: str = "irkutsk"
    thema: str = "животные центры"
    returned_file_name = 'test_csv'
    paginator = Gis_paginator(city=city, search_word=thema)
    map = ScraperEachAddress(city=city, filename=returned_file_name, search_word=thema, references=paginator.paginator_reference)
    page = map.object_soup
    map.scraper_companies(page)
    i = 0

    while i < len(map.references):
        page = map.start_working()
        map.scraper_companies(page)
        i +=1
        time.sleep(1)
        break




























""""
Динамичный постер 2gis.

ДобавитьЖ
	self.snijgp :str = '' #  краткое описание См. "описание.png"
    self.geometry_name :str = ''
 + проверить ПОЛУЧЕННЫЕ данные на уникальность 
 + подкатегории
"""