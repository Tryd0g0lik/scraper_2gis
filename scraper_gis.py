
from bs4 import BeautifulSoup as beauty
import requests
import asyncio as asyncs
import webbrowser
import sys
import socket as s
import json
import urllib3 as urls
import os

from urllib.parse import unquote, quote
class Gis_page():
	def __init__(self, sity:str='', search_word:str=''):
		self.sity = sity;
		self.search_word = search_word;

	def __search_church(self):
		sity = self.sity.__str__()
		word = self.search_word.__str__()

		header_var2 = {

			'Accept': 'application/json, text/plain, */*',
			'Accept-Language': 'ru,en;q=0.9',
			'Cache-Control': 'no-cache',
			'Content-Type': 'application/json',
			'Cookie': 'spid=1679455253675_1770c0b1510abbbdc0853ba604c88630_18b4g7maext0cglv; _2gis_webapi_user=a66814e5-e144-4ecf-aac7-b0e78bc3639f; dg5_pos=82.942781%3B55.017395%3B11; _ym_uid=1679455254592884560; _ym_d=1679455254; _ga=GA1.2.446518772.1679455254; _sa=SA1.0da0215d-3381-470e-933c-595c4661b35f.1679625761; tmr_lvid=7f50349d1ac38812179ad2743b795bc9; tmr_lvidTS=1680748131977; _gid=GA1.2.1690325002.1685144286; _ym_isad=1; _2gis_webapi_session=2134fd48-4873-48a9-b46c-6ea0c37fe2ba; tmr_detect=1%7C1685151536260',
			'Host': '2gis.ru',
			'Origin': 'https://2gis.ru',
			'Referer': f"https://2gis.ru/",
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': '"Windows"',
			'Sec-Fetch-Dest': 'Document',# 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'same-origin',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.4.60',
		}

		header_var3 = {

			'Accept': 'text/plain',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'ru,en;q=0.9',
			'Cache-Control':' no-cache',
			'Connection': 'keep-alive',
			'Host':'jam.api.2gis.com',
			'Origin': 'https://2gis.ru',
			'Pragma': 'no-cache',
			'Referer': 'https://2gis.ru/',
			'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"',
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': "Windows",
			'Sec-Fetch-Dest': 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'cross-site',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.4.603 Yowser/2.5 Safari/537.36'

		}
		headers = urls.HTTPHeaderDict()
		headers.add('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.4.603 Yowser/2.5 Safa',)
		headers.add('sec-ch-ua-platform', '"Windows"')
		headers.add('Host', '2gis.ru')
		headers.add('Origin', 'https://2gis.ru')
		headers.add('sec-ch-ua', '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"')
		# headers.add('Content-Type', 'application/json')
		# headers.add('Accept', 'application/json, text/plain, */*')
		# headers.add('Accept-Language', 'ru,en;q=0.9')

		word_sity = str(self.sity).strip()
		search_word = self.search_word.strip()
		# response = requests.get(f"https://2gis.ru/{word_sity}", headers=header_var)
		# return requests.get(f"https://2gis.ru/novosibirsk/{word_sity}/{search_word}", headers=header_var2, timeout=3 )
		# t = webbrowser.open(f"https://2gis.ru/novosibirsk/search/церкви")
		res_word = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in word)

		requ_word = quote(word)
		requ_sity= quote(sity)
		print(sity)
		headers.add('Referer', f"https://2gis.ru/{sity}/search/{requ_word}")
		t = urls.request("get", url=f"https://2gis.ru/{sity}/search/{requ_word}",
		                 decode_content=True,
		                 timeout=3,
		                 headers=headers)
		# print("t.status :", t.status, " ", t.data)

		# if t.status == 200:
		self.pages = unquote(t.data)



	def __scrap_gi(self,):
		Gis_page.__search_church(self)
		sity = (self.sity).lower()
		print(f"<a href='/{sity}")
		response_text = self.pages
		# print("response_text: " + response_text)
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

	def save_files(self):
		Gis_page.__scrap_gi(self)
		DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
		# os.fdopen(newline="{DESKTOP}/test_file.txt", encoding="utf-8").close()
		with open( file=f"test_file.txt", encoding="utf-8",  mode="w") as f:
			f.write(str(self.object_soup))
			f.close()
