from app_scraper_gis.scraper_basic import Basic_gis
from urllib.parse import unquote, quote
import re
from bs4 import BeautifulSoup as beauty

class Gis_paginator(Basic_gis):
	def __init__(self, city:str, search_word:str):
		'''
		TODO: Scraping a 2gis-page for to getting the pagination
		:param city:
		:param search_word:
		'''
		super().__init__(city, search_word)
		self.paginator_reference = Gis_paginator.start_working(self)
	def __scrap_gis(self):
		try:
			city = "{}".format(Basic_gis.get_city_name(self), )
		except ValueError:
			print('scraper_address.py: Что то не так с названием города!')
			return

		requ_word = quote("{}".format(Basic_gis.get_search_word(self)))
		Basic_gis.get_header(self)

		self.headers.add('Referer', f"https://2gis.ru/{city}/search/{requ_word}")

		url = self.headers['Referer']
		Basic_gis.get_url(self, url, self.headers)


	def sraper_referencePaginator(self, find: str = 'paginator'):
		'''
		:paran paginator_list: we geting the <a> - list html-tags which is reference of the paginator.
		:param find: What we searching. 'paginator' - we searching now the 'paginator'
		:return:
		'''
		Gis_paginator.__scrap_gis(self)
		self.pages = ''
		if self.requests.status == 200 \
			and find in ['p', 'pagin', 'paginator', 'pagination']:
			self.pages = "{}".format(unquote(self.requests.data))
			soup = beauty(self.pages, 'html.parser')
			self.paginator_list = soup.find(id="root").contents[0].contents[0] \
				.contents[0].contents[0].contents[1].contents[0] \
				.contents[0].contents[1].contents[0].contents[0] \
				.contents[0].contents[1].contents[1].contents[0] \
				.contents[0].contents[0].contents[0].contents[2].find_all(name="a")
		else:
			print('scraper_address.py: requests.status != 200')
			return

	def sraper_paginator(self):
		'''

		:return: Pulling up the href of the 'paginator_list and return the links list.
		'''
		main_page = self.headers['Referer']
		paginator_reference: list = [main_page,]
		for i in range(0, len(self.paginator_list) - 1):
			word_ru: str = re.search(r"([а-яё%20 -]{3,40}){1,3}", self.paginator_list[i]['href']).group()
			word_ru_unicode = quote(word_ru)
			href_unicode = str(self.paginator_list[i]['href']).replace(str(word_ru), word_ru_unicode)
			paginator_reference.append("https://2gis.ru" + href_unicode) if bool(self.paginator_list[i]) else None
		del self.paginator_list
		return paginator_reference

	def start_working(self):
		Gis_paginator.sraper_referencePaginator(self)
		return Gis_paginator.sraper_paginator(self)