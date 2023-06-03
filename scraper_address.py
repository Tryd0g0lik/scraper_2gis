from scraper_gis import Gis_page
from bs4 import BeautifulSoup as beauty
from threading import Timer
from urllib.parse import unquote, quote
import re
class ScraperEachAddress(Gis_page):
	"""
	TODO: viewing each address
	:properties: 'name' it's the name company;
	:properties: 'snijgp' it's the comments/reviews for a company
	:properties: 'geometry_name' it's  the companu's address
	:properties: 'phone' it's the company number phone
	:properties: 'email' it's the e-mail address
	:properties: 'work_mode' it's the time by which the company is working
	:properties: 'website' it's the URL of the site
	:properties: 'lat' it's the data coordinates about the width
	:properties: 'lon' it's the data coordinates about the long
	:properties: 'vk', tg', 'wa' it's the social network
	"""
	def __init__(self, city:str='', search_word:str = ''):
		super().__init__(city, search_word)
		ScraperEachAddress.start_working(self)
		self.name :str = ""
		self.type_name:str = '' # тип - под названием
		self.reiting:str = "" # Рейтинг
		self.count:str = "" # кол-во 
		self.address:str = "" # Адрес/местонахождения
		self.lat :str = '' # широта
		self.lon :str = ''  # долгота
		self.phone:str = ''
		self.email:str = ''
		self.work_mode:str = ''
		self.vk:str = '' # ВКонтакте
		self.tg:str = ''  # Telegram
		self.wa:str = '' # WhatsApp
		self.ok:str = '' # OK

		self.snijgp :str = '' #  краткое описание См. "описание.png"
		self.geometry_name :str = ''
		self.website :str = ''
		# t = Timer(30.0, ScraperEachAddress.scraper_companies(self, self.object_soup))
		# t.start()
		ScraperEachAddress.scraper_companies(self, self.object_soup)

	def scraper_companies(self, page):
		'''
		TODO: перебераем каждую найденую по запросу компанию
		:rpoperties: 'titleGisReference' getting the url for  a company. It's the URL from the primary common
		 column on the www-page.
		:return:
		'''

		reg_text = r'(<div><div class=[\'|\"]{1}_{1}[\w]{3,10}[\'|\"]{1}>)'
		strip_text = r'''(^<div class=[\'|\"]{1}_{1}[\w]{3,10}[\'|\"]{1})'''
		strip_text_separator = re.match(strip_text, str(page)).group()
		lstrip_text = rf'({strip_text_separator})'



		i = 0
		if len(str(page)) > 0:
			match_list = str(page).strip()
			print("page: ", )
			match_list = match_list.lstrip(lstrip_text).lstrip(">")
			reg_text_separator = re.match(reg_text, str(match_list)).group()

			match_list = match_list.replace(str(reg_text_separator), '_none_')
			match_list = (match_list.split("_none_"))[1:]

			for one_company in match_list:
				for one_separate in one_company.split("</div><div"):
					one_separate = one_separate.lstrip()

					reg_link_text = r'''(<a\sclass=[\"|\']_\w{3,10}[\"|\']\shref=[\"|\'][\/\w]*[\"|\']><span)'''
					reg_nameCompanyLingGis = r'''([\"|\']\/\w*\/?[\w\/]*\/?[\"|\']?)'''
					reg_name = r'''(<span class=[\"|\']_\w{3,10}[\"|\']>[\w|\W]{2,100}</span> ?[^(<!-)])'''
					reg_type_name = r'''(^ class=[\"|\']_\w{3,10}[\"|\']><span class=[\"|\']_\w{3,10}[\"|\']>[^(<!-)][\w|\W]{2,100}<\/span> ?)''' #[^(!--)]

					if bool(re.search(reg_link_text, str(one_separate))):
						'''
						We getting the link into inner company page from 'object_soup'  
						'''
						link_text = re.search(reg_link_text, str(one_separate)).group()
						self.nameCompanyLingGis = "https://2gis.ru{}".format((re.search(reg_nameCompanyLingGis, str(link_text)).group()).strip('"').strip("'"))


					if bool(re.search(reg_name, str(one_separate))):
						name = str(re.search(reg_name, str(one_separate)).group())
						self.name ="{}".format((name.lstrip(r'''(<span class=[\"|\']_\w{5,10}[\"|\']>)''').lstrip('f"><span>')).replace('</span>', ""))

					elif bool(re.search(reg_type_name, str(one_separate))):
						type_name = str(re.search(reg_type_name, str(one_separate)).group())
						type_name = re.search(r"([\w|\W]{3,100}<)", type_name).group().rstrip("<").strip()
						type_name_separator = re.search(r"""(^class=[\"|\']_\w{3,10}[\"|\']><span class=[\"|\']_\w{3,10}[\"|\']>)""", type_name).group().__str__()
						self.type_name = "{}".format(type_name.lstrip(str(type_name_separator)))


					elif bool(re.search(r'(^class=\"_\w{3,10}\">[0-5]{1,2}.?[0-9]{0,2}[^( \W)])', one_separate)):
						reiting_separator = re.search(r'(^class=\"_\w{3,10}\">[0-5]{1,2}.?[0-9]{0,2}[^( \W)])', one_separate).group()
						p = re.search(r'([[0-5]{1}.{0,1}[0-9]{0,2}$|[0-5]{1,2}$])', reiting_separator)
						if bool(p) and \
							float(p.group()) <= 5.0:
							self.reiting = "{}".format(re.search(r'([[0-5]{1}.{0,1}[0-9]{0,2}$|[0-5]{1,2}$])', reiting_separator).group())

					elif bool(re.search(r'(>([0-9]{0,2} [оценокблва]{0,10}))', one_separate)):
						self.count = "{}".format(re.search(r'(>([0-9]{0,2} [оценокблва]{0,10}))', one_separate).group().lstrip(">"))

					elif bool(re.search(r'(^[А-ЯЁ]{1}[а-яА-ЯёЁ]{3,50})', one_separate[71:])):
						'''
						TODO: Thi's a 
						'''
						group1 = r"(^[А-ЯЁ]{1}[а-яА-ЯёЁ]{3,50}[, | ]{1}[^(\&nbsp;)][а-яё ,0-9\/]{1,50})"
						group2 = r"([^(\&nbsp;)][[А-ЯЁа-яё .,0-9\/]|[^(\&nbsp;)][А-ЯЁа-яё .,0-9\/]{1,220}]{1,10}[^(\&nbsp;)])"
						group3 = r"([^(\&nbsp;)][[А-ЯЁа-яё .,0-9]{1,220}|[А-ЯЁа-яё .,0-9]{1,220}]{0,10}[^(\&nbsp;)]{0,2})"
						group4 = r"([^(\&nbsp;)][[А-ЯЁа-яё .,0-9]{1,220}|[^(\&nbsp;)|(\\xa0)]{0,1}[А-ЯЁа-яё .,0-9]{1,220}]{0,10}[^(\&nbsp;)|(\\xa0)]{0,1})"

						address_separator = re.search(
							rf'''({group1}{group2}{group3}{group4})''', one_separate[71:])
						if bool(address_separator):
							self.address = "{}".format(address_separator.group().rstrip("<"))

class ScraperInnerPage(ScraperEachAddress):
	def __init__(self, city, search_word):
		print("Э5555555555555555")
		super().__init__(city, search_word)
		self.tut()

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

	def __scrap_gis_inner(self):
		'''
		This's the analog the '__scrap_gis' only for a inner page company/. We got it's page when push
		title/name company from the 'object_soup'
		TODO: viewing the inner basis column for inner company's page
		:return: Datas about the one company
		'''
		print("__scrap_gis_inner")
		url = "{}".format(self.nameCompanyLingGis, )
		response_inner = ScraperInnerPage.open_inner_page_company(self, url)
		if response_inner.status == 200:
			ScraperInnerPage.pages = unquote(response_inner.data)

			if len(ScraperInnerPage.pages) > 0:
				response_text = "{}".format(ScraperInnerPage.pages)
				soup = beauty(response_text, features="html.parser")

				print("There is the Lon/lat attributes")
				# There is the Lon/lat attributes
				self.object_soup = ""
				self.object_soup = soup.find(id="root") \
				.contents[0].contents[0] \
				.contents[0].contents[0].contents[1].contents[0] \
				.contents[0].contents[1].contents[0].contents[0].find(name="a")

				page = ["{}".format(self.object_soup)]
				page = [page[0].replace("|", "")]

				ScraperInnerPage.scraper_continues_data_company(self, page)

				print("There is we search the time mode for the works")
				# There is we search the time mode for the works
				self.object_soup = ""
				self.object_soup = soup.find(id="root") \
				.contents[0].contents[0] \
				.contents[0].contents[0].contents[1].contents[0] \
				.contents[0].contents[1].contents[0].select("div[data-rack='true']")

				if bool(self.object_soup):

					test = self.object_soup[0].descendants
					page = []
					for elem in self.object_soup[0].descendants: page.append(elem)

					resp = ScraperInnerPage.scraper_continues_data_company(self, page)
					print(
						self.name,
					self.type_name,
					self.reiting,
					self.count,
					self.address,
					self.lat,
					self.lon,

					self.snijgp,
					self.geometry_name,
					self.phone,
					self.email,
					self.work_mode,
					self.website,
					self.vk,
					self.tg,
					self.wa,
					self.ok
					)
		else:
			print("t.data: ", ScraperInnerPage.pages.status)
			return

	def scraper_continues_data_company(self, page_list:list):
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
		get_website = r'(http(s{0,1})([^(mailto)]://\w{0,25}[^(w3)].{0,1}\w{0,25}).[a-z]{2,3})'

		get_time_list = [
			r'(Ежедневно с [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Сегодня [c|с] [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Откроется [завтра]{0,1} {0,1}в [А-ЯЁа-яё]{0,25}[в| ]{1,3}[0-9]{2}:[0-9]{2})',
			]

		i = 0

		for page in page_list:

			if len(str(page)) > 15:
				if bool(re.search(get_points, str(page))) and self.lat == "" \
					and 'points' in str(page):

					# page = page.replace("|", "")
					lonLat = (re.search(get_points, str(page)).group())
					lonLat = re.search(r'[0-9]{1,2}.{1}[0-9]{1,10},{0,1}[0-9]{1,2}.{1}[0-9]{1,10}', str(lonLat)).group().strip()\
					.split(",")
					self.lon = lonLat[1]
					self.lat = lonLat[0]
					lonLat = ('',)
					# return re.search(get_text, str(page)).group()
					continue

				for get_text in get_time_list:
					if bool(re.search(get_text,  str(page))): # \
						# or bool(re.search(get_time_list[1], str(page))) \
						# or bool(re.search(get_time_list[2], str(page))):

						new_string = re.search(rf'{get_text}', str(page)).group() + ", "
						if new_string not in str(self.work_mode):
							self.work_mode = self.work_mode + str(new_string)
						else: None
						continue

				if self.email == '' and bool(re.search( r'(mailto:\w{1,15}@\w{3,15}.\w{2,3})', str(page))) \
					and bool(re.search(get_mail, str(page))):
					self.email = re.search(r'(mailto:\w{1,25}@\w{3,25}.\w{2,3})',str(page)).group().lstrip("mailto").lstrip(":")


				elif self.phone == '' and re.search('tel:', str(page)) \
					and bool(re.search(get_phone, str(page))):
					self.phone = (re.search(get_phone, str(page)).group()).lstrip("tel:")


				elif self.wa == '' and bool(re.search(get_WhatsApp, str(page))):
					# self.wa = re.search(rf'{get_text}', str(page)).group()
					self.wa = re.search(r'href="http(s){0,1}:\/\/wa.me\/[0-9]{1,20}', str(page)).group()


				elif self.ok == '' and bool(re.search(get_ok, str(page))):
					self.ok = re.search(get_ok, str(page)).group()


				elif self.tg == '' and bool(re.search(get_tg, str(page))):
					self.tg = re.search(rf'{get_tg}', str(page)).group()


				elif self.vk == '' and bool(re.search(r'(http(s{0,1}):\/\/vk\.com\/\w{1,21})', str(page))):
					self.vk = re.search(r'(http(s{0,1}):\/\/vk\.com\/\w{1,21})', str(page)).group()




	def tut(self):

		ScraperInnerPage.__scrap_gis_inner(self)
		'''
		:properties: 'titleGisReference' - this's a link into the inner company's page
		:propertiies: 'ScraperEachAddress' - it's a method for works with the inner company's page 
		'''


