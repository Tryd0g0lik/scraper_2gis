from app_scraper_gis.scraper_gis import Gis_page
from bs4 import BeautifulSoup as beauty
from urllib.parse import unquote, quote
import urllib3 as urls
import re

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
		self.info: str = ""
		self.subcategory: str = ""  # подкатегория

		self.snijgp: str = ''  # Комментарий

	def open_inner_page_company(self, data_url):
		'''

		:param data_url: URL from inner page company
		:return: Opening and load the html-page from the single company's page
		'''
		import urllib3 as urls
		self.headers['Referer'] = data_url
		header = "{}".format(self.headers)

		pages = urls.request("get", url=data_url,
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
		# print("__scrap_gis_inner")
		# url = "{}".format(self.nameCompanyLingGis, )

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
			#
			"""There  down is from the content the information block"""
			self.object_soup = self.object_soup[0].find_parents("div")[3] \
				.contents[0].contents[0].contents[0].contents[0].find_all(name='a')
			url = "https://2gis.ru" + self.object_soup[1]['href']
			ScraperInnerPage.scraper_infoCommitPictures(self, url)
			del url
			print("END")

		else:
			print("t.data: ", ScraperInnerPage.pages.status)
			return

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
		get_points = r'(points\/[0-9]{1,2}.{1}[0-9]{1,10},{0,1}[0-9]{1,2}.{1}[0-9]{1,10})'
		get_website = r'http(s{0,1}):\/\/\w{0,25}.{0,1}\w{2,25}[^(2gis)|(w3)|vk.].ru'
		# http://glavnoehvost.ru
		get_time_list = [
			r'(Ежедневно с [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Сегодня [c|с] [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Откроется [завтра]{0,1} {0,1}в [А-ЯЁа-яё]{0,25}[в| ]{1,3}[0-9]{2}:[0-9]{2})',
		]

		i = 0

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
						continue

				# if self.email == '' and bool(re.search(r'(mailto:([.\w@-]{,50}){,2})', str(page))) \
				if bool(re.search(r'(mailto:([.\w@-]{,50}){,2})', str(page))) \
					and bool(re.search(get_mail, str(page))):
					self.email += re.search(r'(mailto:([.\w@-]{,50}){,2})', str(page)).group().lstrip("mailto").lstrip(":") + ", "


				# if self.phone == '' and re.search('tel:', str(page)) \
				if re.search('tel:', str(page)) \
					and bool(re.search(get_phone, str(page))):
					self.phone += (re.search(get_phone, str(page)).group()).lstrip("tel:") +", "
					print("self.phone:", self.phone)


				# if self.wa == '' and bool(re.search(get_WhatsApp, str(page))):
				if bool(re.search(get_WhatsApp, str(page))):
					self.wa += re.search(r'http(s){0,1}:\/\/wa.me\/[0-9]{1,20}', str(page)).group() + ", "


				# if self.ok == '' and bool(re.search(get_ok, str(page))):
				if bool(re.search(get_ok, str(page))):
					self.ok += re.search(get_ok, str(page)).group() + ", "


				# if self.tg == '' and bool(re.search(get_tg, str(page))):
				if bool(re.search(get_tg, str(page))):
					self.tg += re.search(rf'{get_tg}', str(page)).group().lstrip('href=').replace('"', "") + ", "


				# if self.vk == '' and bool(re.search(r'(http(s{0,1}):\/\/vk\.com\/\w{1,21})', str(page))):
				if bool(re.search(r'(http(s{0,1}):\/\/vk\.com\/\w{1,21})', str(page))):
					self.vk += re.search(r'(http(s{0,1}):\/\/vk\.com\/\w{1,21})', str(page)).group() + ", "

				# if self.website == "" and bool(re.search(get_website, str(page))):
				if bool(re.search(get_website, str(page))):
					self.website += re.search(get_website, str(page)).group() + ", "

				page_list.pop(0)

	def scraper_infoCommitPictures(self, url):
		"""There  down is we search the time mode for the works and
			self.phone,
		"""
		head = ScraperInnerPage.get_header(self)
		info_page = urls.request("get", url=url, decode_content=True)
		if info_page.status == 200:
			info_page = "{}".format(unquote(info_page.data), )
			soup = beauty(info_page, 'html.parser')
			response_text = soup.find(id="root").find(text="Контакты").find_parent("a").parent.parent.find_parents("div")[4].contents[1].contents[0].contents[0].select('div[data-divider="true"]')

			for i in range(len(response_text) - 1):
				tag_reg = r'((<a)[ \/\w="]+>)'
				tag_reg1 = r'(^ {0,1}|(<button class="\w{3,10}")|(<span class="\w{3,10}")+|<span]+){1,20}>'
				tag_reg2 = r'([<\/spanbuto]{3,15}>){1,20}'

				if i == 0:
					self.info = str(response_text[i].find(name="span")).replace("<br/>", " ").replace("•", "").replace(" ", "")

					if bool(re.search(tag_reg1, str(self.info))):
						tag = re.search(tag_reg1, str(self.info)).group()
						self.info = self.info.replace(tag, "")

					if bool(re.search(tag_reg2, str(self.info))):
						tag = re.search(tag_reg2, str(self.info)).group()
						self.info = self.info.replace(tag, "")
						del tag
					print("self.info: ", self.info)
				else:
					index = True

					text = response_text[i].find(name="span")
					if text != None:
						while index and i <= len(response_text) - 1 :
							print(i, " ===>> ", self.subcategory)
							if bool(re.search(tag_reg1, str(text))):
								tag = str(re.search(tag_reg1, str(text)).group())
								tag
								text = str(text).replace(tag, " ")
								text

							elif bool(re.search(tag_reg, str(text))):
								tag = str(re.search(tag_reg, str(text)).group())
								tag
								text = str(text).replace(tag, " ")
								text

							if bool(re.search(tag_reg2, str(text))):
								tag = str(re.search(tag_reg2, str(text)).group())
								tag
								text = str(text).replace(tag, "")
								text
							index = False if 'class' not in text \
								and 'button' not in text \
								and 'span' not in text \
								and 'div' not in text \
								and '<a ' not in text else True

						self.subcategory += text



				# 	del tag, text, index
				# del tag_reg1, tag_reg2