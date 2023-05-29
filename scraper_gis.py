from bs4 import BeautifulSoup as beauty
import urllib3 as urls
from urllib.parse import unquote, quote




class Gis_page():
	"""
	:properties: 'sity_name' - it's сity name

	"""
	def __init__(self, sity:str='', search_word:str=''):
		self.сity_name = sity;
		self.search_word = search_word;
		# Gis_page.start_working(self)

	def __search_church(self): # search the word
		sity = self.сity_name.__str__().strip()
		word = self.search_word.__str__().strip()

		self.headers = urls.HTTPHeaderDict()
		self.headers.add('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.4.603 Yowser/2.5 Safa',)
		self.headers.add('sec-ch-ua-platform', '"Windows"')
		self.headers.add('Host', '2gis.ru')
		self.headers.add('Origin', 'https://2gis.ru')
		self.headers.add('sec-ch-ua', '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"')

		requ_word = quote(word)
		self.headers.add('Referer', f"https://2gis.ru/{sity}/search/{requ_word}")
		header = self.headers

		t = urls.request("get", url=f"https://2gis.ru/{sity}/search/{requ_word}",
		                 decode_content=True,
		                 timeout=3,
		                 headers=header)

		self.pages:str = ''
		if t.status == 200:
			self.pages = unquote(t.data)


	def __scrap_gis(self,):
		'''
		TODO:  viewing the basis column
		:return:
		'''

		Gis_page.__search_church(self)
		sity = (self.сity_name).lower()
		print(f"<a href='/{sity}")

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


	def save_files(self): # save the search's result into the file
		Gis_page.__scrap_gis(self)
		with open( file=f"test_file.txt", encoding="utf-8",  mode="w") as f:
			print(str(self.object_soup))
			f.write(str(self.object_soup))
			f.close()

	def start_working(self):
		return Gis_page.__scrap_gis(self)

