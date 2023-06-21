from bs4 import BeautifulSoup as beauty
from urllib.parse import unquote, quote
from app_scraper_gis.scraper_basic import Basic_gis


class Gis_main(Basic_gis):
	def __init__(self, city: str = '', search_word: str = '', references: list = [], start_page: int = 0):
		'''
		Scraping common pages from the 2gis
		:param city: it's city with which your work
		:param search_word: this's theme's words by which the company search based on the city
		:param references: this's the list links to pages with a many companies
		:param start_page: this's the start-page of the paginator's lit

		'''
		super().__init__(city, search_word)
		self.references = references
		self.start_page = 0 if start_page == 0 else start_page - 1

	def search_companies(self):
		'''
		search the words - theme's category
		:return:
		'''
		Basic_gis.get_header(self)
		requ_word = quote(self.search_word)
		self.headers.add('Referer', f"https://2gis.ru/{self.сity_name}/search/{requ_word}")
		for ind in range(0, self.start_page): self.references.pop(0)
		for i in range(len(self.references)):
			print("i: ", self.references[i])
			Basic_gis.get_url(self,
				url= self.references[i],
				head=self.headers
			)
			break
		try:
			if self.requests.status >= 200 and self.requests.status < 400:
				self.pages = "{}".format(unquote(self.requests.data), )

		except AttributeError:
			print('Error search_companies: request вернул страницу имеющую статус 300+ ')
			self.pages = ''

	def __scrap_companies(self):
		'''
		TODO:  viewing/uploading the basis column
		:return:
		'''
		city = (self.сity_name).lower()
		print(f"<a href='/{city}")

		soup = beauty(self.pages, features="html.parser")
		self.soup_main = soup.find_all(id='root')[0] \
			.find(name="div") \
			.find(name="div") \
			.find_all(name="div")[0] \
			.find(name="div") \
			.contents[1].contents[0].contents[0].contents[1].contents[0] \
			.contents[0].contents[0].contents[1].contents[1].contents[0] \
			.contents[0].find(name="a").find_parent("div").find_parent("div") \
			.find_parent('div').find_parent("div")

	def start_working(self):
		Gis_main.search_companies(self)

		if self.pages != '':
			return Gis_main.__scrap_companies(self)
