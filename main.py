# This is a sample Python script.
from scraper_address import ScraperEachAddress, ScraperInnerPage
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

from scraper_gis import Gis_page as Gp


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    map = ScraperInnerPage(city="moscow", search_word="Кладбища")
    # map.save_files()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

""""
Динамичный постер 2gis.

После того как основная колонка проскрапиться,  
иследоваься начинает только последняя компания. (__scrap_gis_inner)
__scrap_gis_inner - не все кампании попадают сюда

ДобавитьЖ
	self.snijgp :str = '' #  краткое описание См. "описание.png"
    self.geometry_name :str = ''
 + Пагинацию 
 + перебор кампаний из основной/базовой колонки проверить 
 + подкатегории
"""