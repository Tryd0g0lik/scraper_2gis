from app_scraper_gis.scraper_gis import Gis_page
from bs4 import BeautifulSoup as beauty
from urllib.parse import unquote, quote
from urllib3 import request, Timeout,PoolManager
import re, os, time
from selenium import webdriver
from socket import timeout


from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from PIL import Image
import requests
from io import StringIO, BytesIO

class ScraperInnerPage(Gis_page):
	def __init__(self, city, search_word, page_list):
		'''
		TODO: viewing each address
		:param 'snijgp' it's the comments/reviews for a company
		:param 'geometry_name' it's  the companu's address
		:param 'phone' it's the company number phone
		:param 'email' it's the e-mail address
		:param 'work_mode' it's the time by which the company is working
		:param 'website' it's the URL of the site
		:param 'vk', tg', 'wa' it's the social network
		:param city:
		:param lat
		:param lon
		:param subcategory: This's a additional information about the company, sub-category
		:param search_word:
		'''
		super().__init__(city, search_word, page_list)
		self.lat: str = ''  # широта
		self.lon: str = ''  # долгота
		self.phone: str = ''
		self.email: str = ''
		self.work_mode: str = ''
		self.vk: str = ''  # ВКонтакте
		self.tg: str = ''  # Telegram
		self.wa: str = ''  # WhatsApp
		self.ok: str = ''  # OK
		self.website: str = ''
		self.info: str = ""
		self.subcategory: str = ""  # подкатегория

		self.snijgp: list = []  # Комментарий [{'user_ball': snijgp_ball}, {'user_fdsdsd':snijgp_comment}]
		self.pictures: list = []  # фото из комментариев

	def open_inner_page_company(self, data_url):
		'''

		:param data_url: URL from inner page company
		:return: Opening and load the html-page from the single company's page
		'''
		import urllib3 as urls
		self.headers['Referer'] = data_url
		header = "{}".format(self.headers)

		pages = request("get", url=data_url,
		                     decode_content=True,
		                     timeout=3)

		return pages

	def scrap_gis_inner(self, url):
		'''
		This's the analog the '__scrap_gis' only for a inner page company/. We got it's page when push
		title/name company from the 'object_soup'
		TODO: viewing the inner basis column for inner company's page
		:return: Datas about the one company
		'''

		response_inner = ScraperInnerPage.open_inner_page_company(self, url)
		if response_inner.status == 200:
			ScraperInnerPage.pages = unquote(response_inner.data)

			if len(ScraperInnerPage.pages) > 0:
				response_text = "{}".format(ScraperInnerPage.pages)
				soup = beauty(response_text, features="html.parser")

				# There is the Lon/lat attributes
				self.object_soup = ""
				self.object_soup = soup.find(id="root") \
					.contents[0].contents[0] \
					.contents[0].contents[0].contents[1].contents[0] \
					.contents[0].contents[1].contents[0].contents[0].find(name="a")

				page = ["{}".format(self.object_soup)]
				page = [page[0].replace("|", "")]
				ScraperInnerPage.scraper_continues_data_company(self, page)

				"""There  down is we search the time mode for the works and 
				self.name,      self.type_name,     self.reiting,   self.count,  
				self.address,   self.lat,	          self.lon,	      self.phone,
				self.email,	    self.work_mode,	    self.vk:str,	  self.tg:str, 
				self.wa:str,	  self.ok:str,	      website, 
				"""
				self.object_soup = ""
				self.object_soup = soup.find(id="root") \
					.contents[0].contents[0] \
					.contents[0].contents[0].contents[1].contents[0] \
					.contents[0].contents[1].contents[0].select("div[data-rack='true']")

				if bool(self.object_soup):

					test = self.object_soup[0].descendants
					page = []
					for elem in self.object_soup[0].descendants: page.append(elem)

					ScraperInnerPage.scraper_continues_data_company(self, page)

			# From the content the information block
			"""There  down is from the content the information block"""
			self.object_soup = self.object_soup[0].find_parents("div")[3] \
				.contents[0].contents[0].contents[0].contents[0].find_all(name='a')
			# url = "https://2gis.ru" + self.object_soup[1]['href']
			# ScraperInnerPage.scraper_info(self, url)
			# del url
			#
			# url = "https://2gis.ru" + self.object_soup[2]['href']
			# ScraperInnerPage.scraper_snijgp(self, url)
			# del url


			for i in range(len(self.object_soup) - 1):
				url = "https://2gis.ru" + self.object_soup[i]['href'] if 'gallery/firm' in str(self.object_soup[i]) \
					else None
				if url != None: ScraperInnerPage.scraper_photo_company(self, url)
				print('photo:', url)
			print("END")

		else:
			print("t.data: ", ScraperInnerPage.pages.status)
			return
		del response_inner

	def scraper_continues_data_company(self, page_list: list):
		'''
		TODO: continues scraper  target data
		:param page: - html of column sigle company
		:return: target data
		'''
		# Collecting the text expression

		get_phone = r'(tel:[(\+7)|(8)|(\+8)]{1}[0-9]{5,12})'
		get_WhatsApp = r'("WhatsApp" class="\w{3,10}" href="https:\/\/wa.me\/[0-9]{6,13})'
		get_mail = r'(mailto:\w{1,15}@\w{3,15}.\w{2,3})'
		get_ok = r'(https:\/\/ok\.ru\/group\/[0-9]{1,21})'
		get_tg = r'(href="https:\/\/t\.me/\+[0-9]{6,12}")'
		get_vk = r'(http(s{0,1}):\/\/vk\.com\/\w{1,21})'
		get_points = r'(points\/[0-9]{1,3}.[0-9]{1,10},?[0-9]{,3}.{1}[0-9]{1,10})'
		get_website = r'http(s{0,1}):\/\/\w{0,25}.{0,1}\w{2,25}[^(2gis)|(w3)|vk.].ru'
		# http://glavnoehvost.ru
		get_time_list = [
			r'(Ежедневно с [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Сегодня [c|с] [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Откроется [завтра]{0,1} {0,1}в [А-ЯЁа-яё]{0,25}[в| ]{1,3}[0-9]{2}:[0-9]{2})',
		]

		for page in page_list:

			if len(str(page)) > 15:
				if bool(re.search(get_points, str(page))) and self.lat == "" \
					and bool(re.search(r'points', str(page))):
					page = page.replace("|", "")
					lonLat = (re.search(get_points, str(page)).group())
					lonLat = re.search(r'[0-9]{1,2}.{1}[0-9]{1,10},{0,1}[0-9]{1,2}.{1}[0-9]{1,10}', str(lonLat)).group().strip() \
						.split(",")
					self.lon = lonLat[1]
					self.lat = lonLat[0]

					continue

				for get_text in get_time_list:
					if bool(re.search(get_text, str(page))):

						new_string = re.search(rf'{get_text}', str(page)).group() + ", "
						if new_string not in str(self.work_mode):
							self.work_mode += self.work_mode + str(new_string)

						else:
							None

						del new_string
						continue

				if bool(re.search(r'(mailto:([.\w@-]{,50}){,2})', str(page))) \
					and bool(re.search(get_mail, str(page))):
					self.email += re.search(r'(mailto:([.\w@-]{,50}){,2})', str(page)).group().lstrip("mailto").lstrip(":") + ", "

				if re.search('tel:', str(page)) \
					and bool(re.search(get_phone, str(page))):
					self.phone += (re.search(get_phone, str(page)).group()).lstrip("tel:") +", "

				if bool(re.search(get_WhatsApp, str(page))):
					self.wa += re.search(r'http(s){0,1}:\/\/wa.me\/[0-9]{1,20}', str(page)).group() + ", "

				if bool(re.search(get_ok, str(page))):
					self.ok += re.search(get_ok, str(page)).group() + ", "

				if bool(re.search(get_tg, str(page))):
					self.tg += re.search(rf'{get_tg}', str(page)).group().lstrip('href=').replace('"', "") + ", "

				if bool(re.search(r'(http(s{0,1}):\/\/vk\.com\/\w{1,21})', str(page))):
					self.vk += re.search(r'(http(s{0,1}):\/\/vk\.com\/\w{1,21})', str(page)).group() + ", "

				if bool(re.search(get_website, str(page))):
					self.website += re.search(get_website, str(page)).group() + ", "

				page_list.pop(0)
		del page, page_list

	def scraper_info(self, url):
		'''
			TODO: There  down is we search the:
		:param url: The variable stores a URL for tab. Our simple is a "Инфо".
		:param info: it's main-information about the company, It's took from is a tab "Инфо".
		:param subcategory: This's a additional information about the company, sub-category
		:return: subcategory and info
		'''
		info_page = request("get", url=url, decode_content=True)
		if info_page.status == 200:
			'''
				Scrapering data-info from the inf-html
			'''
			info_page = "{}".format(unquote(info_page.data), )
			soup = beauty(info_page, 'html.parser')
			response_text = soup.find(id="root").find(text="Контакты").find_parent("a").parent.parent.find_parents("div")[4].contents[1].contents[0].contents[0].select('div[data-divider="true"]')

			for i in range(len(response_text) - 1):
				tag_reg = r'((<a)[, \/\w="А-ЯЁа-яё]+[\w{2,10}="-: ]*"?>?)' #'((<a)[ \/\w="]+>)'
				tag_reg1 = r'(^ {0,1}|(<button class="\w{3,10}")|(<span [\w{2,10}="-: ]+)+|<span]+){1,20}>'
				tag_reg2 = r'([<\/spanbuto]{3,15}>){1,20}'

				if i == 0:
					'''
						Working with the info-block ('Инфо')
					'''
					self.info = str(response_text[i].find(name="span")).replace("<br/>", " ").replace("•", "").replace(" ", "")

					if bool(re.search(tag_reg1, str(self.info))):
						tag = re.search(tag_reg1, str(self.info)).group()
						self.info = self.info.replace(tag, "")
						del tag

					if bool(re.search(tag_reg2, str(self.info))):
						tag = re.search(tag_reg2, str(self.info)).group()
						self.info = self.info.replace(tag, "")
						del tag
					# print("self.info: ", self.info)
				else:
					index = True
					'''
						scraping the sub-cotegories from the info-block ('Инфо') 
					'''
					text = response_text[i].find(name="span")
					if text != None:
						while index and i <= len(response_text) - 1 :
							# print(i, " ===>> ", self.subcategory)
							if bool(re.search(tag_reg1, str(text))):
								tag = str(re.search(tag_reg1, str(text)).group())
								text = str(text).replace(tag, " ")
								del tag

							elif bool(re.search(tag_reg, str(text))):
								tag = str(re.search(tag_reg, str(text)).group())
								text = str(text).replace(tag, " ")
								del tag

							if bool(re.search(tag_reg2, str(text))):
								tag = str(re.search(tag_reg2, str(text)).group())
								text = str(text).replace(tag, "")
								del tag

							index = False if 'class' not in text \
								and 'button' not in text \
								and 'span' not in text \
								and 'div' not in text \
								and '<a ' not in text else True

						self.subcategory += text
						self.subcategory = str(self.subcategory).replace(r" {2,}[A-ZА-ЯЁ]", ", ")



					del text, index
				del tag_reg1, tag_reg2
			del response_text
		del info_page

	def scraper_snijgp(self, url):
		'''
		TODO: Working through the SELENIUM.
		 and IMG-file loading into folder from-the 2gis
		:param url: for a feedback block.
		:return snijgp: Feedback from people about the one company
		'''

		PATH = os.path.dirname(os.path.abspath(__file__)) + "\\chromedriver\\chromedriver.exe"
		chrome_options = Options()
		chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
		driver = webdriver.Chrome(executable_path=str(PATH), chrome_options=chrome_options)
		driver.get(str(url))

		'''
			JS  - scrolling the browser's window
		'''
		js_elem = """document.querySelector("#root > div > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div > div > div:nth-child(2) > div > div > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(1) > div > div")"""
		driver.execute_script(js_elem + '.scrollBy({top:' + js_elem + '.scrollHeight' + ', left: 0, behavior: "smooth"});')
		time.sleep(5)
		html = driver.page_source

		soup = beauty(str(html), 'html.parser')
		if len(soup.find(id="root").select('input[value="all"]')) > 0:
			response_text_common = soup.find(id="root").select('input[value="all"]')[0].find_parent("div").find_parents('div')[1].contents[2:]

			for i in range(0, len(response_text_common) - 1):

				'''
					pictures checking from feedback
				'''
				snijgp_img = "NAN" if len(response_text_common[i].contents) <= 2 \
					or bool(response_text_common[i].contents[len(response_text_common[i].contents)-2]) == False \
					or bool(response_text_common[i].contents[len(response_text_common[i].contents)-2].contents) == False \
					or bool(response_text_common[i].contents[len(response_text_common[i].contents)-2].contents[0]) == False \
					or bool(response_text_common[i].contents[len(response_text_common[i].contents)-2].contents[0].find("img")) == False \
					else response_text_common[i].contents[len(response_text_common[i].contents)-2].contents[0].find_all("img")
				if 'img' in str(snijgp_img):
					'''
						Thi's code (for in) it's IMG-file loading into folder from-the 2gis
					'''
					for ind in range(0, len(snijgp_img)):
						snijgp_img_src = snijgp_img[ind].attrs['src']

						'''
							URL-row is cleaning
						'''
						if bool(re.search(r'\?\w=[0-9]{2,3}$', str(snijgp_img_src))) == False:
							break

						else:
							w = re.search(r'\?\w=[0-9]{2,3}$', str(snijgp_img_src)).group()
							snijgp_img_src = str(snijgp_img_src).replace(w, '')
							del w

						'''
						There is file IMG loading from the 2Gis 
						'''
						url = requests.get(str(snijgp_img_src))
						img = Image.open(BytesIO(url.content))
						rename = str(self.name) + '_feedback_' + str(i) + '_img_' + str(ind)

						PATH_img = str(os.path.dirname(os.path.abspath(__file__))) + '/file'
						img.save(os.path.join(PATH_img, rename) + '.JPG', 'JPEG', quality=90)
						self.pictures.append(rename + '.JPG' + ', ')
						del snijgp_img_src, img, rename, PATH_img

				'''
					Commits copy in the your db from the 2Gis 
				'''
				snijgp_comment = "NAN" if len(response_text_common[i].contents) <= 2 \
					else response_text_common[i].contents[len(response_text_common[i].contents)-1].contents[0].find("a").text

				self.snijgp.append(snijgp_comment) if len(snijgp_comment) > 5 \
					else self.snijgp.append("NaN")

				del snijgp_comment
			del js_elem, html, response_text_common

			return
		else:
			return

	def scraper_photo_company(self, url):
		print("url00: ", url)
		'''
			Creting the timeout for the request-url into the company foto-block  
		'''
		# timeout = Timeout(connect =5.0, read=15.0)
		# timeout = timeout.read_timeout
		# http = PoolManager(timeout=timeout)


		photo_page = request("get", url=url, decode_content=True,)
		# photo_page = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')

		if photo_page.status == 200:
			photo_page = "{}".format(unquote(photo_page.data))

			try:
				soup = beauty(photo_page, 'html.parser')
				gallery_photo =  soup.find(id='root').contents[0].contents[0].contents[0].contents[0].contents[1].contents[0] \
					.contents[0].contents[1].contents[0].contents[0].contents[1].contents[0].contents[0].contents[0].contents[0] \
					.contents[0].contents[0].contents[1].contents[0].contents[0].contents[0]


				if bool(gallery_photo):

					for i in range(0, len(gallery_photo)):
						print("i, ", i)
						# print("Photo_compzny: ", gallery_photo[i]['src'])
			except ValueError:
				print("Is somthing wrong into the 'scraper_photo_company'/ It's search the 'gallery_photo'")

			''''
			soup.find(id='root').contents[0].contents[0].contents[0].contents[0].contents[1].contents[0].contents[0].contents[1].contents[0].contents[0].contents[1].contents[0].contents[0].contents[0].contents[0].contents[0].contents[0].contents[1].contents[0].contents[0].contents[0].contents[0].contents[0]
			'''