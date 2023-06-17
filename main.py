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
def return_sity_name(name:(str, list)):
    response = ''
    if type(name) == str:
      name = [name]
    for elem in name:
      response = elem
      name.pop()
      break
    return response
def return_rubric_name(name:(str, list)):
    response = ''
    if type(name) == str:
      name = [name]
    for elem in name:
      response = elem
      name.pop()
      break
    return response

if __name__ == "__main__":

    city: str = "armawir" # return_sity_name(["irkutsk", 'armawir'])# "irkutsk" # armawir
    thema: str = "кладбище" # return_rubric_name(["кладбище", 'морг']) животные
    returned_file_name = thema

    paginator = Gis_paginator(city=city, search_word=thema)
    map = ScraperEachAddress(city=city, filename=returned_file_name,  search_word=thema, references=paginator.paginator_reference)
    page = map.object_soup
    map.scraper_companies(page)
    i = 0

    while i < len(map.references):
        page = map.start_working()
        map.scraper_companies(page)
        i +=1
        time.sleep(1)
        break
'''

soup.find(id="root") \
.contents[0].contents[0] \
.contents[0].contents[0].contents[1].contents[0] \
.contents[0].contents[1].contents[0].find(text="Инфо")
'''

""""
    Динамичный постер 2gis.

    ДобавитьЖ
    self.geometry_name :str = ''
    + проверить ПОЛУЧЕННЫЕ данные на уникальность 
    + подкатегории
"""
