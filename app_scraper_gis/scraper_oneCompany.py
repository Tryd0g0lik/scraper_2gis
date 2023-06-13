import datetime

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from app_scraper_gis.scraper_gis import Gis_page
from bs4 import BeautifulSoup as beauty
from urllib.parse import unquote
from urllib3 import request
import re, os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import requests

PATH = os.path.dirname(os.path.abspath(__file__)) + "\\chromedriver\\chromedriver.exe"
PATH_img = str(os.path.dirname(os.path.abspath(__file__))) + '\\file'


def makeFolder(name: str, path: str = "./"):
	if path == "./":
		name = os.path.dirname(os.path.abspath(__file__)) + '\\file\\' + name
		if not os.path.isdir(str(name)):
			os.mkdir(str(name))

	else:
		if not os.path.isdir(str(path) + str(name)):
			os.path.isdir(str(os.path.isdir(str(path) + str(name))))

	return


def getHtmlOfDriverChrome(url: str, selector: str = '', scroll: bool = False, click: bool = False):
	'''
		If we want make the click-action, means the XPATH format-SELECTOR inserting
		:param url: data-source
		:param path_chrom: path to the Chrome.exe (from is the Program files folder)
		:param selector: it's the path with the html-element for will be work with the JavaScript
		:return: page-html
	'''
	path_chrome: str = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

	browser = Options()
	browser.binary_location = path_chrome
	driver = webdriver.Chrome(
		executable_path=str(PATH),
		chrome_options=browser
	)
	driver.get(str(url))
	time.sleep(3)
	if selector == '':
		html = driver.page_source
	elif selector != '':
		if scroll == True:
			'''
				JS  - scrolling the browser's window
			'''

			js_elem = "document.querySelector('" + (selector).strip() + "')"
			driver.execute_script(
				js_elem + '.scrollBy({top:' + js_elem + '.scrollHeight' + ', left: 0, behavior: "smooth"});')
			del selector, js_elem

		elif click == True:
			'''
				Finding the html element and
				create the click-action for an element   
			'''

			element = driver.find_element(By.XPATH, selector)
			ActionChains(driver).click(element).perform()

		time.sleep(5)
		html = driver.page_source
	driver.close()
	return html


class ScraperInnerPage(Gis_page):
	def __init__(self, city, search_word, references):
		'''
		TODO: viewing each geometry_name
		:param references: list links on pages
		:param 'snijgp' it's the comments/reviews for a company
		:param 'geometry_name' it's  the companu's geometry_name
		:param 'phone' it's the company number phone
		:param 'email' it's the e-mail geometry_name
		:param 'work_mode' it's the time by which the company is working
		:param 'website' it's the URL of the site
		:param 'vk', tg', 'wa' it's the social network
		:param city:
		:param lat
		:param lon
		:param subcategory: This's a additional information about the company, sub-category
		:param search_word:
		:param src_img_feedback: it's the image-src from the feedback-block
		:param src_img_company: it's the image-src from the company info-block
		'''
		super().__init__(city, search_word, references)
		self.lat: str = ''  # широта
		self.lon: str = ''  # долгота
		self.phone: str = ''
		self.email: str = ''
		self.work_mode: list = []
		self.vk: str = ''  # ВКонтакте
		self.tg: str = ''  # Telegram
		self.wa: str = ''  # WhatsApp
		self.ok: str = ''  # OK
		self.website: str = ''
		self.info: str = ""
		self.subcategory: str = ""  # подкатегория
		self.snijgp: list = []  # Комментарий [{'user_ball': snijgp_ball}, {'user_fdsdsd':snijgp_comment}]
		self.src_img_feedback: list = []  # фото из комментариев
		self.src_img_company: list = []

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

	def scrap_gis_inner(self, url, ):
		'''
		This's the analog the '__scrap_gis' only for a inner page company/. We got it's page when push
		title/name company from the 'object_soup'
		TODO: viewing the inner basis column for inner company's page
		:param url: data-source
		:return: Datas about the one company
		'''

		# response_inner = ScraperInnerPage.open_inner_page_company(self, url)
		try:
			response_inner =getHtmlOfDriverChrome(url=url, click=True,
			                      selector='//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div[2]')
		except AttributeError:
			print('AttributeError scraper_oneCompany.py: Что не так с атрибутами из scrap_gis_inner()' )
			return

		if type(response_inner) == str and len(response_inner) > 300:
			ScraperInnerPage.pages = unquote(response_inner)

			if len(ScraperInnerPage.pages) > 0:
				response_text = "{}".format(ScraperInnerPage.pages)
				soup = beauty(response_text, features="html.parser")

				'''
				 There is the Lon/lat attributes
			 '''
				self.object_soup = ""
				self.object_soup = soup.find(id="root") \
					.contents[0].contents[0] \
					.contents[0].contents[0].contents[1].contents[0] \
					.contents[0].contents[1].contents[0].contents[0].find(name="a")

				page = ["{}".format(self.object_soup)]
				page = [page[0].replace("|", "")]
				ScraperInnerPage.scraper_continues_data_company(self, page)

				"""There  down is search the time mode (self.work_mode) for the works and 
				self.name,      self.type_name,     self.reiting,   self.count,  
				self.geometry_name,   self.lat,	          self.lon,	      self.phone,
				self.email,	    	    self.vk:str,	  self.tg:str, 
				self.wa:str,	  self.ok:str,	      website, 
				"""
				self.object_soup = ""
				self.object_soup = soup.find(id="root") \
					.contents[0].contents[0] \
					.contents[0].contents[0].contents[1].contents[0] \
					.contents[0].contents[1].contents[0].select("div[data-rack='true']")

				if bool(self.object_soup):
					page = []
					for elem in self.object_soup[0].descendants: page.append(elem)

					ScraperInnerPage.scraper_continues_data_company(self, page)

			'''
				From the content the information block
				There  down is from the content the information block
			'''
			self.object_soup = self.object_soup[0].find_parents("div")[3] \
				.contents[0].contents[0].contents[0].contents[0].find_all(name='a')
			url = "https://2gis.ru" + self.object_soup[1]['href']
			ScraperInnerPage.scraper_info(self, url)

			url = "https://2gis.ru" + self.object_soup[2]['href']
			selector = """#root > div > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div > div > div:nth-child(2) > div > div > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(1) > div > div"""
			ScraperInnerPage.scraper_snijgp(self, url, selector)
			del url, selector

			for i in range(0, len(self.object_soup)):
				url = "https://2gis.ru" + self.object_soup[i]['href'] if 'gallery/firm' in str(self.object_soup[i]) \
					else None
				if url != None: ScraperInnerPage.scraper_photo_company(self, url, '')
				del url
			print("END")
			del response_inner
			return

		else:
			None

	def scraper_continues_data_company(self, page_list: list):
		'''
		TODO: continues scraper  target data
		:param page_list: it's a list has  tags-html/  Everyone element from the list check -
		 will be this element has the tadas or not. if yes, then this element cleaned using
		  regular-regrowth. Will been get datas of the doata-sources
		:param page: - html of the column  sigle company
		:return: target data
		'''
		get_phone = r'(tel:[(\+7)|(8)|(\+8)]{1}[0-9]{5,12})'
		get_WhatsApp = r'("WhatsApp" class="\w{3,10}" href="https:\/\/wa.me\/[0-9]{6,13})'
		get_mail = r'(mailto:\w{1,15}@\w{3,15}.\w{2,3})'
		get_ok = r'(https:\/\/ok\.ru\/group\/[0-9]{1,21})'
		get_tg = r'(href="https:\/\/t\.me/\+[0-9]{6,12}")'
		get_points = r'(points\/[0-9]{1,3}.[0-9]{1,10},?[0-9]{,3}.{1}[0-9]{1,10})'
		get_website = r'http(s{0,1}):\/\/\w{0,25}.{0,1}\w{2,25}[^(2gis)|(w3)|vk.].ru'
		get_time_list = [
			r'(Ежедневно с [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Круглосуточно)',
			r'(Сегодня [c|с] [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Откроется [(завтра)|(через)]+ [в 0-9А-ЯЁа-яё]{0,32}[в 0-9:]{,10})',
		]
		# r'([[(Пн)&(Вт)&(Ср)&(Чт)&(Пт)&(Сб)&(Bc)]&[([0-9]{2}:[0-9]{2}[( до )|-][0-9]{2}:[0-9]{2})|-]){1,}',

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

						new_string = re.search(rf'{get_text}', str(page)).group()
						if new_string not in str(self.work_mode):
							self.work_mode.append(new_string.replace('\u200b', ' ') \
							                      .replace(" ", ' ').replace('\U0001f60a', ''))

						else:
							None

						del new_string
						continue

				'''
					getting the info-that from the one company, It's a common column from the basic page/
				'''
				if bool(re.search(r'(mailto:([.\w@-]{,50}){,2})', str(page))) \
					and bool(re.search(get_mail, str(page))):
					email = re.search( \
						r'(mailto:([.\w@-]{,50}){,2})', \
						str(page)).group().lstrip("mailto") \
						        .lstrip(":") + ", "
					self.email += email + ', ' if email not in self.email else '' \
					                                                           ''
				if re.search('tel:', str(page)) \
					and bool(re.search(get_phone, str(page))):
					url = self.title_link_company

					'''
						Selenium - driver Chrome
					'''
					html = getHtmlOfDriverChrome(
						url,
						selector='//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div[3]/div[2]/div/button',
						click=True
					)
					'''
						find a[href='tel:']
					'''
					phone_button = beauty(html, 'html.parser').find(text="Контакты").find_parents(name="div")[6] \
						.contents[0].parent.contents[1].contents[0].contents[0].contents[0].contents[2].find_all("a")

					'''
						checking the what to me found
					'''

					if bool(phone_button) and len(phone_button) > 1:
						for i in range(len(phone_button)):
							phone = str((re.search(get_phone, str(phone_button)).group()).lstrip("tel:") \
							            .lstrip('+'))
							self.phone += phone + ", " if phone not in self.phone else ''

					else:
						phone = str((re.search(get_phone, str(page)).group()).lstrip("tel:") \
						            .lstrip('+'))
						self.phone += phone + ", " if phone not in self.phone else ''

				if bool(re.search(get_WhatsApp, str(page))):
					wa = re.search(r'http(s){0,1}:\/\/wa.me\/[0-9]{1,20}', str(page)).group() + ", "
					self.wa += wa + ', ' if wa not in self.wa else ''

				if bool(re.search(get_ok, str(page))):
					ok = re.search(get_ok, str(page)).group() + ", "
					self.ok += ok + ', ' if ok not in self.ok else ''

				if bool(re.search(get_tg, str(page))):
					tg = re.search(rf'{get_tg}', str(page)).group().lstrip('href=').replace('"', "") + ", "
					self.tg += tg + ', ' if tg not in self.tg else ''

				if bool(re.search(r'(http(s{0,1}):\/\/vk\.com\/\w{1,21})', str(page))):
					vk = re.search(r'(http(s{0,1}):\/\/vk\.com\/\w{1,21})', str(page)).group() + ", "
					self.vk += vk + ', ' if vk not in self.vk else ''

				if bool(re.search(get_website, str(page))):
					website = re.search(get_website, str(page)).group() + ", "
					self.website += website + ', ' if website not in self.website else ''

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
			response_text = \
			soup.find(id="root").find(text="Контакты").find_parent("a").parent.parent.find_parents("div")[4].contents[
				1].contents[0].contents[0].select('div[data-divider="true"]')

			for i in range(len(response_text) - 1):
				tag_reg = r'((<a)[, \/\w="А-ЯЁа-яё]+[\w{2,10}="-: ]*"?>?)'
				tag_reg1 = r'(^ {0,1}|(<button class="\w{3,10}")|(<span ?[\w="-: ]*)+>){1,20}'
				tag_reg2 = r'([<\/spanbuto]{3,15}>){1,20}'

				if i == 0:
					'''
						Working with the info-block ('Инфо')
					'''
					info = str(response_text[i].find(name="span")).replace("•", "")
					self.info = info.encode('cp1251', 'ignore').decode('cp1251')
					del info

					if bool(re.search(tag_reg1, str(self.info))):
						self.info = re.sub(tag_reg1, '', str(self.info))

					if bool(re.search(tag_reg2, str(self.info))):
						self.info = re.sub(tag_reg2, '', str(self.info))

				else:
					index = True
					'''
						scraping the sub-cotegories from the info-block ('Инфо') 
					'''

					text = response_text[i].find(name="span")
					if text != None:
						while index and i <= len(response_text) - 1:
							if bool(re.search(tag_reg1, str(text))):
								text = re.sub(tag_reg1, ' // ', str(text))

							if bool(re.search(tag_reg, str(text))):
								text = re.sub(tag_reg, ' // ', str(text))

							if bool(re.search(tag_reg2, str(text))):
								text = re.sub(tag_reg2, '', str(text))

							index = False if 'class' not in text \
							                 and 'button' not in text and 'span' not in text \
							                 and 'div' not in text and '<a ' not in text else True

						self.subcategory += text.replace('​', "").replace('\u200b', '') \
							.replace('\U0001f60a', '')
						self.subcategory = str(self.subcategory).replace(r" {2,}[A-ZА-ЯЁ]", ", ")

					del text, index
				del tag_reg1, tag_reg2
			del response_text
		del info_page

	def scraper_snijgp(self, url, selector):
		'''
		TODO: Working through the SELENIUM.
		 and IMG-file loading into folder from-the 2gis
		:param url: for a feedback block.
		:param selector: it's the path with the html-element for will be work with the JavaScript
		:return snijgp: Feedback from people about the one company
		'''

		html = getHtmlOfDriverChrome(url, selector, scroll=True)
		soup = beauty(str(html), 'html.parser')
		if len(soup.find(id="root").select('input[value="all"]')) > 0:
			response_text_common = \
			soup.find(id="root").select('input[value="all"]')[0].find_parent("div").find_parents('div')[1].contents[2:]
			for i in range(0, len(response_text_common) - 1):

				'''
					pictures checking from feedback
				'''
				snijgp_img = "NAN" if len(response_text_common[i].contents) <= 2 \
				                      or bool(
					response_text_common[i].contents[len(response_text_common[i].contents) - 2]) == False \
				                      or bool(
					response_text_common[i].contents[len(response_text_common[i].contents) - 2].contents) == False \
				                      or bool(
					response_text_common[i].contents[len(response_text_common[i].contents) - 2].contents[0]) == False \
				                      or bool(
					response_text_common[i].contents[len(response_text_common[i].contents) - 2].contents[0].find("img")) == False \
					else response_text_common[i].contents[len(response_text_common[i].contents) - 2].contents[0].find_all("img")
				if 'img' in str(snijgp_img):
					'''
						This's code (for in) it's IMG-file loading into folder from-the 2gis
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

						self.src_img_feedback.append((snijgp_img_src).strip())
						del snijgp_img_src
						print('photo_feelback', self.src_img_feedback)

				'''
					Commits copy in the your db from the 2Gis 
				'''
				snijgp_comment_link = "NAN" if len(response_text_common[i].contents) <= 2 \
					else response_text_common[i].contents[len(response_text_common[i].contents) - 1].contents[0].find("a") \
					.text.replace(" ", ' ')

				'''
					and delete UNICODE 
				'''
				self.snijgp.append( \
					"(" + str(snijgp_comment_link).encode('cp1251', 'ignore').decode('cp1251') + ")") \
					if len(snijgp_comment_link) > 5 \
					else self.snijgp.append("NaN")

				del snijgp_comment_link
			del selector, html, response_text_common

			return
		else:
			return

	def scraper_photo_company(self, url, selector: str = ''):
		'''
		:param url:  the source company's block-foto
		:param selector: it's the path with the html-element for will be work with the JavaScript
		:return: the folder where id saving foto-files
		'''
		html = getHtmlOfDriverChrome(url, selector, click=True)
		soup = beauty(str(html), 'html.parser')
		src_img_company = soup.find_all("img")

		'''
			checking count the collected reference
		'''
		if bool(src_img_company) and len(src_img_company) > 0:
			''' Collecting before the 4 pictures '''

			for i in range(0, len(src_img_company[:4])):
				if 'srcset' in str(src_img_company[i]):
					self.src_img_company.append(src_img_company[i]['srcset'])
				elif 'src' in str(src_img_company[i]):
					self.src_img_company.append(src_img_company[i]['src'])
				else:
					break
		del src_img_company


'''
	from PIL import Image
	from io import BytesIO
	# Getting pictures from the source
	url = requests.get(str(src))

	img = Image.open(BytesIO(url.content))

'''