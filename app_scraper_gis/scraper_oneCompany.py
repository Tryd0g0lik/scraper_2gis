from app_scraper_gis.driver_chromeBrowser import ActionDriverChrome
from app_scraper_gis.scraper_gis import Gis_page
from bs4 import BeautifulSoup as beauty
from urllib.parse import unquote
from urllib3 import request
import re, os, logging
from collections import Counter
from PIL import Image
from io import BytesIO
import requests




def makeFolder(name: str, path: str = "./"):
	'''
		Create the folder
		:param name: Name folder/catalog
		:param path: Path into the location for new folder/catalog
		:return:
	'''
	if path == "./":
		name = os.path.dirname(os.path.abspath(__file__)) + '\\file\\' + name
		if not os.path.isdir(str(name)):
			os.mkdir(str(name))

	else:
		if not os.path.isdir(str(path) + str(name)):
			os.path.isdir(str(os.path.isdir(str(path) + str(name))))

	return

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
		self.phone: str = []
		self.email: str = ''
		self.work_mode: list = []
		self.vib: str = ''  # Viber
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

	def parser_page(self, html_page):
		'''
		TODO:
		:param html_page: it's has tag-html got after action by request to url
		:return: page parsed
		'''
		page = html_page
		response_text = "{}".format(unquote(page))#.encode('utf-8', error='ignore').decode('utf-8')
		return beauty(response_text, features="html.parser")
	def open_inner_page_company(self, data_url):
		'''

		:param data_url: URL for inner page company
		:return: Opening and load the html-page from the single company's page
		'''
		import urllib3 as urls
		self.headers['Referer'] = data_url
		header = "{}".format(self.headers)

		pages = request("get", url=data_url,
		                decode_content=True,
		                timeout=3)
		return pages

	def scrap_gis_inner(self, url:str, ):
		'''
		This's the analog the '__scrap_gis' only for a inner page company/. We got it's page when push
		title/name company from the 'object_soup'
		TODO: viewing the inner basis column for inner company's page
		:param url: data-source
		:return: Datas about the one company
		'''

		# Открываем страницу
		try:
			'''
				Click on woking mode time
			'''
			html = ActionDriverChrome(url=url)
			html.page_loading()
			html_page = html.get_page()
			soup = ScraperInnerPage.parser_page(self, html_page=html_page)
			html.closed_browser()
		except AttributeError:

			print('AttributeError scraper_oneCompany.py: Что не так с атрибутами из scrap_gis_inner()' + str(logging.exception("message")))
			return

		if len(html_page) > 100: # checking a symbol count
			'''
				only making a check
			'''
			'''
				 :param Lon and lat: There is params the longitude and latitude 
			  '''

			object_soup = soup.find(text="Проехать").find_parent('a')
			lonLat = re.search(r'[0-9]{1,2}.{1}[0-9]{1,10},{0,1}[0-9]{1,2}.{1}[0-9]{1,10}', str(object_soup)).group() \
				.strip().split(",")
			self.lon = lonLat[1]
			self.lat = lonLat[0]
			del object_soup

			# checking = bool(soup.find_all(id='root')[0] \
			#      .find(name="div") \
			#      .find(name="div") \
			#      .find_all(name="div")[0] \
			#      .find(name="div").find(text='Контакты'))
			checking = bool(soup.find(id='root').find(text='Контакты'))
			del soup

			if checking:
				'''
					basic work after the checking
				'''
				# html_page = html.page_loadeing()
				html.selector='//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div[2]'
				html.action_click(click=True)
				# html.selector = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div[3]/div[2]/div/button'
				html.selector = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div[2]/div/a'
				html.action_click(click=True)
				html_page = html.get_page()
				soup = ScraperInnerPage.parser_page(self, html_page)
				html.closed_browser()



				'''
					:param work_mode: time's work mode + WWW + social-networks + Email + Phone's number ...
				'''
				soup = ScraperInnerPage.parser_page(self, html_page)
				ScraperInnerPage.scrap_contacts(self, soup)

			'''
				working with info-block
			'''
			soup = ScraperInnerPage.parser_page(self, html_page)
			ScraperInnerPage.scraper_info(self, soup)
			# del url, html_page


			soup = ScraperInnerPage.parser_page(self, html_page)
			ScraperInnerPage.scraper_snijgp(self, html, soup)

			"""
				:param snijgp: it's feedback
			"""
			if bool(soup.find(text='Фото')):
				url = "https://2gis.ru" + soup.find(text='Фото').parent['href']

				if url != None: ScraperInnerPage.scraper_photo_company(self, url, '')
				del url

		del html
		return

	def scrap_contacts(self, soup):
		get_phone = r'(tel:[(\+7)|(8)|(\+8)]{1}[0-9]{5,12})'
		get_mail = r'(mailto:(\w{1,}_{,2}.){1,}@\w{3,15}.\w{2,3})'
		get_website = r'http(s{0,1}):\/\/\w{0,25}.{0,1}\w{2,25}[^(2gis)|(w3)|vk.].\w{2,5}'
		get_time_list = [
			r'(Ежедневно с [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Круглосуточно)',
			r'(Сегодня [c|с] [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Откроется [(завтра)|(через)]+ [в 0-9А-ЯЁа-яё]{0,32}[в 0-9:]{,10})', ]

		'''
		Поиск рабочего времени в Пн, Вт - Вс
		'''
		page = soup.find(text="Контакты").find_parents('div')[6]
		for elem in get_time_list:
			if bool(re.search(elem, str(page))):
				resp = re.search(elem, str(page)).group()
				self.work_mode.append(resp)
		del resp, get_time_list

		for elem in ['Пн', 'Вт', 'Пн', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']:
			if bool(soup.find(text=elem)) and len(soup.find(text=elem).parent.parent.contents) > 0:
				self.work_mode.append( elem + ': ' + soup.find(text=elem).parent.parent.contents[1].text)
		del elem

		'''
			Email
		'''
		resp = soup.find(text='Контакты').find_parents('div')[6]
		self.email = re.search(get_mail, str(resp)).group() if bool(re.search(get_mail, str(resp))) else \
			'NaN'
		del resp

		'''
			Phone number 
		'''
		resp = re.search(get_phone, str(page))
		if bool(resp):
			self.phone.append(resp.group() if resp.group() not in str(self.phone) else 'NaN')
		del resp

		'''
			WWW
		'''
		resp = re.search(get_website, str(page))
		self.website = resp.group() if bool(resp) else 'NaN'
		del resp, page

		'''
			social's networks 
		'''
		for elem in ['WhatsApp', 'ВКонтакте', 'Viber', 'Telegram']:
			if bool(soup.find(text=elem)):
				resp = soup.find(text=elem).find_parent(name='a')['href']
				if elem == 'WhatsApp':
					self.wa = resp
				elif elem == 'ВКонтакте':
					self.vk = resp
				elif elem == 'Viber':
					self.vib = resp
				elif elem == 'Telegram':
					self.tg = resp
			del resp, elem
		del get_phone, get_mail, get_website

	def scraper_info(self, soup):
		'''
			Scrapering data-info from the info-html
		'''
		if bool(soup.find(text='Инфо')):
			url = "https://2gis.ru" + soup.find(text='Инфо').parent['href']
			del soup
			html = ActionDriverChrome(url)
			html.page_loading()
			html_page = html.get_page()

			soup = ScraperInnerPage.parser_page(self, html_page)
			html.closed_browser()
			# ------------------------
			response_text = \
				(soup.find(id="root").find(text="Инфо").find_parent("a").parent.parent.find_parents("div")[4].contents[
					1].contents[0].contents[0].select('div[data-divider="true"]'))

			self.info = '{}'.format(response_text[0].text).encode('cp1251', errors='replace').decode('cp1251')
			self.info = re.sub(r'[ |•]', ' ', (self.info))

			'''
				sub-category
			'''
			for i in range(1,len(response_text)):
				str__ = response_text[i].text
				l = []
				[l.append(v) for v in re.findall(r'[А-ЯЁ]', str__) if v not in str(l)]
				for v in l:
					str__ = str__.replace(v, ' // ' + v) #.replace('\u200b', ' ') \ .encode('utf-8', 'ignore').decode('cp1251') .replace(" ", ' ')
						 #.replace('\U0001f60a', '')
				# regex = re.compile("u'200b'", re.UNICODE)
				self.subcategory += str__.encode('cp1251', errors='replace').decode('cp1251') #re.sub( re.compile("u'200b'", re.UNICODE), " ", str__).encode('cp1251').decode('cp1251')
			del str__, l,v

	def scraper_snijgp(self, html, soup):
		if bool(soup.find(text='Отзывы')):
			url = "https://2gis.ru" + soup.find(text='Отзывы').parent['href']

			# if len(soup.find(text='Отзывы').parent.find_parents('div')[6].contents) > 1:
			selector = """#root > div > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div > div > div:nth-child(2) > div > div > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(1) > div > div"""
			html = ActionDriverChrome(url, selector)
			html.page_loading()
			html_page = html.get_page()
			# ------------------
			resp = (soup.find(text='Отзывы').parent.find_parents('div')[6].contents[1].contents)
			html.action_acroll(scroll=True)

			while True:
				html_page = html.get_page()
				html_page = ('{}'.format(html_page)).encode('cp1251', errors='replace').decode('cp1251')
				soup = ScraperInnerPage.parser_page(self, html_page)
				resp2 = (soup.find(text='Отзывы').parent.find_parents('div')[6].contents[1].contents)
				if len(resp2) > len(resp):
					html.action_acroll(scroll=True)
					resp = resp2
					continue
				break
			del soup, resp

			html_page = html.get_page()
			soup = ScraperInnerPage.parser_page(self, html_page)
			resp2 = (soup.find(text='Отзывы').parent.find_parents('div')[6].contents[1].contents)

			for elem in resp2[2:]:
				str_ = '{}'.format(elem.text.encode('cp1251', errors="replace").decode('cp1251'))
				self.snijgp.append([str_])
				del elem
			del resp2
			html.closed_browser()


	def scraper_photo_company(self, url, selector: str = ''):
			'''
			:param url:  the source company's block-foto
			:param selector: it's the path with the html-element for will be work with the JavaScript
			:return: the folder where id saving foto-files
			'''
			html = ActionDriverChrome(url, selector)
			html.page_loading()
			html_page = html.get_page()
			html.action_click(click=True)

			html_page = "{}".format(unquote(html_page))
			# soup = beauty(str(html_page), 'html.parser')
			soup = ScraperInnerPage.parser_page(self,html_page)
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

