from scraper_gis import Gis_page
import re
from bs4 import BeautifulSoup

class Gis_paginator(Gis_page):
	def __init__(self, city:str, search_word:str):
		super().__init__(self, city, search_word)
		self.object_soup
		Gis_paginator.start_working(self)

	def __scrap_gis(self,):
		pass

	def searching_referencePaginator(self):
		pass

	def start_working(self):
		return Gis_page.__scrap_gis(self)