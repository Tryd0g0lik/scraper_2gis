from bs4 import BeautifulSoup as beauty
import requests
import asyncio as asyncs
import webbrowser
import sys
import socket as s

class Gis_page():
	def __init__(self, sity:str='', search_word:str=''):
		self.sity = sity;
		self.search_word = search_word;

	def __search_church(self):
		header_var2 = {

			'Accept': 'application/json, text/plain, */*',
			'Accept-Language': 'ru,en;q=0.9',
			'Cache-Control': 'no-cache',
			'Content-Type': 'application/json',
			'Cookie': 'spid=1679455253675_1770c0b1510abbbdc0853ba604c88630_18b4g7maext0cglv; _2gis_webapi_user=a66814e5-e144-4ecf-aac7-b0e78bc3639f; dg5_pos=82.942781%3B55.017395%3B11; _ym_uid=1679455254592884560; _ym_d=1679455254; _ga=GA1.2.446518772.1679455254; _sa=SA1.0da0215d-3381-470e-933c-595c4661b35f.1679625761; tmr_lvid=7f50349d1ac38812179ad2743b795bc9; tmr_lvidTS=1680748131977; _gid=GA1.2.1690325002.1685144286; _ym_isad=1; _2gis_webapi_session=2134fd48-4873-48a9-b46c-6ea0c37fe2ba; tmr_detect=1%7C1685151536260',
			'Host': '2gis.ru',
			'Origin': 'https://2gis.ru',
			'Referer': 'https://2gis.ru/novosibirsk',
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': '"Windows"',
			'Sec-Fetch-Dest': 'Document',# 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'same-origin',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.4.60',
		}

		word_sity = str(self.sity).strip()
		search_word = self.search_word.strip()
		# response = requests.get(f"https://2gis.ru/{word_sity}", headers=header_var)
		return requests.get(f"https://2gis.ru/novosibirsk/{word_sity}/{search_word}", headers=header_var2, timeout=3 )



	def scrap_gi(self,):
		response = Gis_page.__search_church(self)
		sity = (self.sity).lower()
		print(f"<a href='/{sity}")
		response_text = response.text
		# print("response_text: " + response_text)
		soup = beauty(response_text, features="html.parser")
		object_soup = soup.find_all(id='root')[0] \
			.find(name="div") \
			.find(name="div") \
			.find_all(name="div")[0] \
			.find(name="div") \
			.contents[1].contents[0].contents[0].contents[1]
		# s.socket.settimeout(5)



		dict_var = []

		# for ele in object_soup:
		print("object_soup: ", object_soup)

