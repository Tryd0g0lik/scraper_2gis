from bs4 import BeautifulSoup as beauty
from urllib.parse import unquote, quote

from app_scraper_gis.scraper_basic import Basic_gis


class Gis_page(Basic_gis):
	"""
	:properties: 'city_name' - it's сity name

	"""
	def __init__(self, city: str = '', search_word: str = '', references: list = []):
		super().__init__(city, search_word)
		self.references = references
		# Gis_page.start_working(self)

	def search_church(self): # search the word
		'''
		search the words - theme's category
		:return:
		'''
		city = Basic_gis.get_city_name(self)
		word = Basic_gis.get_search_word(self)

		Basic_gis.get_header(self)
		requ_word = quote(word)
		self.headers.add('Referer', f"https://2gis.ru/{city}/search/{requ_word}")
		header = self.headers

		for i in range(len(self.references)):
			print("i: ", self.references[i])
			Basic_gis.get_url(self,
				url= self.references[i], #f"https://2gis.ru/{city}/search/{requ_word}",
				head=header
			)

			break

		self.pages:str = ''
		# self.references.pop(0)
		if self.requests.status == 200:
			self.pages = "{}".format(unquote(self.requests.data), )

	def __scrap_gis(self,):
		'''
		TODO:  viewing/uploading the basis column
		:return:
		'''

		Gis_page.search_church(self)
		city = (self.сity_name).lower()
		print(f"<a href='/{city}")

		if self.pages != '':
			response_text = self.pages
			soup = beauty(response_text, features="html.parser")
			self.object_soup = soup.find_all(id='root')[0] \
				.find(name="div") \
				.find(name="div") \
				.find_all(name="div")[0] \
				.find(name="div") \
				.contents[1].contents[0].contents[0].contents[1].contents[0] \
				.contents[0].contents[0].contents[1].contents[1].contents[0] \
				.contents[0].find(name="a").find_parent("div").find_parent("div") \
				.find_parent('div').find_parent("div")
		# page = "{}".format(self.object_soup, )

		return self.object_soup

	def start_working(self):
		return Gis_page.__scrap_gis(self)
