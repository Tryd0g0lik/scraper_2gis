import urllib3 as urls

class Basic_gis():
	def __init__(self, city: str = '', search_word: str = ''):
		'''
		TODO: We make a request  by the URL into  the 'city' by 'search_word'
		 return uploading of html-pages from the 2gis.ru
		:param headers: your adding the ('Referer', f"https://2gis.ru/{city}/search/{requ_word}")
		:param city:
		:param search_word: categories for to the search
		'''
		self.сity_name = city;
		self.search_word = search_word;
		self.total_table = []


	def get_header(self):
		"""
		TODO: headers for the url-request
		:return: Reqest Headers
		"""
		self.headers = urls.HTTPHeaderDict()
		self.headers.add('User-Agent',
		                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.4.603 Yowser/2.5 Safa', )
		self.headers.add('sec-ch-ua-platform', '"Windows"')
		self.headers.add('Host', '2gis.ru')
		self.headers.add('Origin', 'https://2gis.ru')
		self.headers.add('sec-ch-ua', '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"')
		header_gis = "{}".format(self.headers, )
		return header_gis
	def get_city_name(self):
		city_gis = "{}".format(self.сity_name.__str__().strip())
		return city_gis

	def get_search_word(self):
		word_gis = "{}".format(self.search_word.__str__().strip(), )
		return word_gis

	def get_url(self, url,  head):
		'''
		:param url: page's addres from the 2gis
		:param head: Browser Request-Header
		:return: uploading the page from 2gis-url
		'''

		self.requests = urls.request("get", url=url,
		                 decode_content=True,
		                 timeout=3,
		                 headers=head)
		request_gis = "{}".format(self.requests, )
		return request_gis
