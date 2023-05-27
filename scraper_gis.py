from bs4 import BeautifulSoup as beauty
import urllib3 as urls
from urllib.parse import unquote, quote


class Gis_page():
	def __init__(self, sity:str='', search_word:str=''):
		self.sity = sity;
		self.search_word = search_word;

	def __search_church(self): # search the word
		sity = self.sity.__str__()
		word = self.search_word.__str__()


		headers = urls.HTTPHeaderDict()
		headers.add('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.4.603 Yowser/2.5 Safa',)
		headers.add('sec-ch-ua-platform', '"Windows"')
		headers.add('Host', '2gis.ru')
		headers.add('Origin', 'https://2gis.ru')
		headers.add('sec-ch-ua', '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"')

		word_sity = str(self.sity).strip()
		search_word = self.search_word.strip()


		requ_word = quote(word)
		headers.add('Referer', f"https://2gis.ru/{sity}/search/{requ_word}")
		t = urls.request("get", url=f"https://2gis.ru/{sity}/search/{requ_word}",
		                 decode_content=True,
		                 timeout=3,
		                 headers=headers)

		# if t.status == 200:
		self.pages = unquote(t.data)



	def __scrap_gi(self,): # viewing
		Gis_page.__search_church(self)
		sity = (self.sity).lower()
		print(f"<a href='/{sity}")
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
		Gis_page.__scrap_gi(self)
		with open( file=f"test_file.txt", encoding="utf-8",  mode="w") as f:
			f.write(str(self.object_soup))
			f.close()
