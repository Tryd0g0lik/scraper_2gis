# This is a sample Python script.
from scrape_paginator import Gis_paginator
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

    paginator = Gis_paginator(city="irkutsk", search_word="животные")
    map = ScraperEachAddress(city="irkutsk", search_word="животные центры", page_list=paginator.paginator_reference)
    i = 0
    while i < len(map.page_list):
    # if len(map.page_list) > 0:
        # page = map.object_soup
        page = map.start_working()
        map.scraper_companies(page)
        i +=1
        break
        # print("примет мир 10")
        # time.sleep(10)
        # print("примет мир")

    # map.save_files()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


""""
Динамичный постер 2gis.

ДобавитьЖ
	self.snijgp :str = '' #  краткое описание См. "описание.png"
    self.geometry_name :str = ''
 + если кампания имеет 2 телефона, то ыскфзук берет только один - Второй номер доступен при клике-JS
 + Пагинацию 
 + перебор кампаний из основной/базовой колонки проверить 
 + подкатегории
"""