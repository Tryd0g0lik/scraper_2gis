# This is a sample Python script.
from app_scraper_gis.scrape_paginator import Gis_paginator
from app_scraper_gis.scraper_companies import ScraperCompanies
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
  city: str = ['Abakan', 'Almetyevsk', 'Anadyr', 'Armavir', 'Arkhangelsk', 'Astrakhan', 'Balakovo', 'Barnaul', 'Belgorod','Beloretsk', 'Biysk']
  thema: str = ['Магазин', 'Кладбища', 'Церкви', 'Храмы', 'Соборы', 'Колумбарии', 'Крематории', 'Помощь в организации похорон',
     'Памятники надгробия',
     'Ритуальные услуги для животных']
  start_page = 0

  for c in city:
    for t in thema:
      returned_file_name = t
      paginator = Gis_paginator(city=c, search_word=t)

      i = 0

      while i != len(paginator.paginator_reference) - start_page:
        page = ScraperCompanies(city=c, filename=returned_file_name, search_word=t,
                           references=paginator.paginator_reference, start_page=start_page)
        page.scraper_companies(page.soup_main)
        paginator.paginator_reference.pop(0)
        print(i)
        city.pop(0)
        thema.pop(0)
        start_page = 0
        i+=1
        time.sleep(2)
