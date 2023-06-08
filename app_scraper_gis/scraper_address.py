import re

import time

from app_scraper_gis.scraper_oneCompany import ScraperInnerPage


class ScraperEachAddress(ScraperInnerPage):
	"""
		TODO: viewing each address
		:param 'name' it's the name company;

		:param 'lat' it's the data coordinates about the width
		:param 'lon' it's the data coordinates about the long
	"""

	def __init__(self, city: str = '', search_word: str = '', page_list = []):
		super().__init__(city, search_word, page_list)
		ScraperEachAddress.start_working(self)
		self.name: str = ""
		self.type_name: str = ''  # тип - под названием
		self.reiting: str = ""  # Рейтинг
		self.count: str = ""  # кол-во
		self.address: str = ""  # Адрес/местонахождения
		self.subcategory: str = "" # (подкатегория

		self.snijgp: list = []  # (Комментарий)
		self.geometry_name: str = ''

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

		if len(str(page)) > 0:
			match_list = str(page).strip()
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
					reg_type_name = r'''(^ class=[\"|\']_\w{3,10}[\"|\']><span class=[\"|\']_\w{3,10}[\"|\']>[^(<!-)][\w|\W]{2,100}<\/span> ?)'''  # [^(!--)]

					if bool(re.search(reg_link_text, str(one_separate))):
						'''
						We getting the link/url into inner company's page from 'object_soup'  
						'''
						link_text = re.search(reg_link_text, str(one_separate)).group()
						self.nameCompanyLingGis = "https://2gis.ru{}".format(
							(re.search(reg_nameCompanyLingGis, str(link_text)).group()).strip('"').strip("'"))

					if bool(re.search(reg_name, str(one_separate))):
						name = str(re.search(reg_name, str(one_separate)).group())
						self.name = "{}".format(
							(name.lstrip(r'''(<span class=[\"|\']_\w{5,10}[\"|\']>)''').lstrip('f"><span>')).replace('</span>', ""))
						# print("self.name: ", self.name)

					if bool(re.search(reg_type_name, str(one_separate))):
						type_name = str(re.search(reg_type_name, str(one_separate)).group())
						type_name = re.search(r"([\w|\W]{3,100}<)", type_name).group().rstrip("<").strip()
						type_name_separator = re.search(
							r"""(^class=[\"|\']_\w{3,10}[\"|\']><span class=[\"|\']_\w{3,10}[\"|\']>)""", type_name).group().__str__()
						self.type_name = "{}".format(type_name.lstrip(str(type_name_separator)))

					if bool(re.search(r'(^class=\"_\w{3,10}\">[0-5]{1,2}.?[0-9]{0,2}[^( \W)])', str(one_separate))):
						reiting_separator = re.search(r'(^class=\"_\w{3,10}\">[0-5]{1}.?[0-9]{0,2}[^( \W)])', one_separate).group()
						p = 0.0
						if bool(re.search(r'([0-5].{0,1}[0-9]{0,2}$)', str(reiting_separator))):
							p = float(re.search(r'([0-5].{0,1}[0-9]{0,2}$)', str(reiting_separator)).group())
							if p <= 5.0:
								self.reiting = "{}".format(p)
								p = 0.0

					if bool(re.search(r'(>([0-9]{0,4} [оценокиблва]{0,10}))', str(one_separate))):
						self.count = "{}".format(
							re.search(r'(>([0-9]{0,4} [оценокблва]{0,10}))', str(one_separate)).group().lstrip(">"))

					if bool(re.search(r'(^[А-ЯЁ]{1}[а-яА-ЯёЁ]{3,50})', str(one_separate[71:]))):
						ScraperInnerPage.scrap_gis_inner(self, self.nameCompanyLingGis)

						'''
						TODO: Thi's a 
						'''
						get_address = r"(([0-9]{0,2}[-а-яё ]{0,4})?[а-яА-ЯёЁ -( )]{3,50}[, | ][а-яё ,( )0-9\/]{1,50}){1,}"
						if bool(re.search(rf'''{get_address}''', str(one_separate))):
							index_1 = re.search(rf'''{get_address}''', str(one_separate)).span()[0]
							address_separator = re.search(rf'''{get_address}''', str(one_separate[index_1:]))

							self.address = "{}".format(address_separator.group().rstrip("<"))
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
								self.ok,
								self.info,
								self.info,
								self.subcategory, # подкатегория

								self.snijgp,
								self.pictures

							)
							self.name: str = ""
							self.type_name: str = ''  # тип - под названием
							self.reiting: str = ""  # Рейтинг
							self.count: str = ""  # кол-во
							self.address: str = ""  # Адрес/местонахождения
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
							self.subcategory: str = "" # подкатегория

							self.snijgp: list = []  # Комментарий
							self.pictures: list = []  # фото из комментариев

							self.geometry_name: str = ''

							# print("примет мир")
							# time.sleep(1)
							# print("примет мир - 5")



