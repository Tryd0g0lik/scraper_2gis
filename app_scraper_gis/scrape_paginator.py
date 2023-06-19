from app_scraper_gis.scraper_basic import Basic_gis
from urllib.parse import unquote, quote
import re
from bs4 import BeautifulSoup as beauty

class Gis_paginator(Basic_gis):
	def __init__(self, city:str, search_word:str):
		'''
		TODO: Scraping a 2gis-page for to get the paginated list-reference
		:param city: city name which you want  receive paginated-pages
		:param search_word:
		'''
		super().__init__(city, search_word)
		self.paginator_reference = Gis_paginator.start_working(self)
	def __scrap_gis(self):

		requ_word = quote(self.search_word)
		Basic_gis.get_header(self)
		self.headers.add('Referer', f"https://2gis.ru/{self.сity_name}/search/{requ_word}")
		url = self.headers['Referer']

		Basic_gis.get_url(self, url, self.headers)


	def sraper_paginator(self, find: str = 'paginator'):
		'''
		:paran paginator_list: we geting the <a> - list html-tags which is reference of the paginator.
		:param find: What we searching. 'paginator' - we searching now the 'paginator'
		:return:
		'''
		self.pages = ''
		Gis_paginator.__scrap_gis(self)

		if self.requests.status == 200 \
			and find in ['p', 'pagin', 'paginator', 'pagination']:
			self.pages = unquote(self.requests.data)
			soup = beauty(self.pages, 'html.parser')
			self.paginator_list = soup.find(id="root").contents[0].contents[0] \
				.contents[0].contents[0].contents[1].contents[0] \
				.contents[0].contents[1].contents[0].contents[0] \
				.contents[0].contents[1].contents[1].contents[0] \
				.contents[0].contents[0].contents[0].contents[2].find_all(name="a")
		else:
			print('scraper_companies.py: requests.status != 200')
			return

	def parser_paginator(self):
		'''

		:return: Pulling up the href of the 'paginator_list and return the links list.
		'''
		main_page = self.headers['Referer']
		paginator_reference: list = [main_page,]
		for i in range(0, len(self.paginator_list) - 1):
			for i in range(len(self.paginator_list)):

				word_ru: str = re.search(r"([а-яё%20 -]{3,40}){1,3}", self.paginator_list[i]['href']).group()
				word_ru_unicode = quote(word_ru)
				href_unicode = str(self.paginator_list[i]['href']).replace(str(word_ru), word_ru_unicode)
				paginator_reference.append('https://2gis.ru' + href_unicode)
		del self.paginator_list
		return paginator_reference

	def start_working(self):
		Gis_paginator.sraper_paginator(self)
		return Gis_paginator.parser_paginator(self)