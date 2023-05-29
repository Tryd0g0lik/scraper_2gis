from bs4 import BeautifulSoup as beauty
import urllib3 as urls
from urllib.parse import unquote, quote




class Gis_page():
	"""
	:properties: 'city_name' - it's сity name

	"""
	def __init__(self, city:str='', search_word:str=''):
		self.сity_name = city;
		self.search_word = search_word;
		# Gis_page.start_working(self)

	def get_header(self):
		self.headers = urls.HTTPHeaderDict()
		self.headers.add('User-Agent',
		                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.4.603 Yowser/2.5 Safa', )
		self.headers.add('sec-ch-ua-platform', '"Windows"')
		self.headers.add('Host', '2gis.ru')
		self.headers.add('Origin', 'https://2gis.ru')
		self.headers.add('sec-ch-ua', '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"')

	def get_city_name(self):
		return self.сity_name.__str__().strip()

	def get_search_word(self):
		return self.search_word.__str__().strip()

	def get_url(self, url,  head):
		return urls.request("get", url=url,
		                 decode_content=True,
		                 timeout=3,
		                 headers=head)

	def search_church(self): # search the word
		city = Gis_page.get_city_name(self)
		word = Gis_page.get_search_word(self)

		Gis_page.get_header(self)
		requ_word = quote(word)
		self.headers.add('Referer', f"https://2gis.ru/{city}/search/{requ_word}")
		header = self.headers

		t = Gis_page.get_url(self,
			url=f"https://2gis.ru/{city}/search/{requ_word}",
			head=header
		)

		self.pages:str = ''
		if t.status == 200:
			self.pages = unquote(t.data)

		# self.headers['Referer'] = ''

	def __scrap_gis(self,):
		'''
		TODO:  viewing the basis column
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


	# def save_files(self): # save the search's result into the file
	# 	Gis_page.__scrap_gis(self)
	# 	with open( file=f"test_file.txt", encoding="utf-8",  mode="w") as f:
	# 		print(str(self.object_soup))
	# 		f.write(str(self.object_soup))
	# 		f.close()

	def start_working(self):
		return Gis_page.__scrap_gis(self)

