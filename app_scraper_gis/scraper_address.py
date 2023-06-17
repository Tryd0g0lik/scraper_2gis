import datetime
import re

from app_scraper_gis.get_pandas_file.basic_data import BasicDataArray
from app_scraper_gis.scraper_oneCompany import ScraperInnerPage
import pandas as pd
import numpy as np


class ScraperEachAddress(ScraperInnerPage, BasicDataArray):
	"""
		TODO: viewing each geometry_name
		:param 'name' it's the name company;
		:param search_word: it's the word or phrases for the search categories
		:param 'lat' it's the data coordinates about the width
		:param 'lon' it's the data coordinates about the long
		:param title_link_company: reference on the 2gis's column company from the title
	"""

	def __init__(self, filename:str, city: str = '', search_word: str = '', references = []):
		super().__init__(city, search_word, references)
		ScraperEachAddress.start_working(self)
		self.name: str = ""
		self.type_name: str = ''  # тип - под названием
		self.reiting: str = ""  # Рейтинг
		self.count: str = ""  # кол-во
		self.geometry_name: str = ""  # Адрес/местонахождения
		self.subcategory: str = "" # (подкатегория
		#search_word Слово, фраза для поиска рубрики/категории
		self.snijgp: list = []  # (Комментарий)

		self.geometry_name: str = ''
		self.title_link_company: str = ''  # ссылка на страницу кмпании
		self.filename = (filename).strip()

	def scraper_companies(self, page, ):
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
			match_list = str(page).strip() \
				.lstrip(lstrip_text).lstrip(">")
			reg_text_separator = re.match(reg_text, str(match_list)).group()
			match_list = ((re.sub(str(reg_text_separator), '_none_', str(match_list))) \
			              .split("_none_"))[1:]

			for one_company in match_list:
				for one_separate in one_company.split("</div><div"):
					one_separate = one_separate.lstrip()

					reg_link_text = r'''(<a\sclass=[\"|\']_\w{3,10}[\"|\']\shref=[\"|\'][\/\w]*[\"|\']><span)'''
					reg_nameCompanys2Gis = r'''([\"|\']\/\w*\/?[\w\/]*\/?[\"|\']?)'''
					reg_name = r'''(<span class=[\"|\']_\w{3,10}[\"|\']>[\w|\W]{2,100}</span> ?[^(<!-)])'''
					reg_type_name = r'''(^ ?class=[\"|\']_\w{3,10}[\"|\']><span class=[\"|\']_\w{3,10}[\"|\']>[^(<!-)][\w|\W]{2,100}<\/span> ?)'''  # [^(!--)]

					if bool(re.search(reg_link_text, str(one_separate))):
						'''
						We getting the link/url into inner company's page from 'object_soup'  
						'''
						link_text = re.search(reg_link_text, str(one_separate)).group()
						self.title_link_company = "https://2gis.ru{}".format(
							(re.search(reg_nameCompanys2Gis, str(link_text)).group()).strip('"').strip("'"))

					if bool(re.search(reg_name, str(one_separate))):
						'''
							Name company
						'''
						name = str(re.search(reg_name, str(one_separate)).group())
						self.name = "{}".format(
							(name.lstrip(r'''(<span class=[\"|\']_\w{5,10}[\"|\']>)''') \
							 .lstrip('f"><span>')).replace('</span>', ""))
						print(self.name, 'Старт')
					if bool(re.search(reg_type_name, str(one_separate))):
						'''
							:param self.type_name: searching data by the type-function/business
						'''
						try:
							type_name = str(re.search(reg_type_name, str(one_separate)).group())
							type_name = re.search(r"([\w|\W]{3,100}<)", type_name).group().rstrip("<").strip()
							type_name_separator = re.search(
								r"""(^class=[\"|\']_\w{3,10}[\"|\']><span class=[\"|\']_\w{3,10}[\"|\']>)""", type_name).group().__str__()
							self.type_name = "{}".format(type_name.lstrip(str(type_name_separator)))
						except AttributeError:
							break
					if bool(re.search(r'(class=\"_\w{3,10}\">[0-5]{1,2}.?[0-9]{0,2}[^ оценокиблва<\W]*)', str(one_separate))):
						'''
							:param self.type_name: searching data by the rating 
						'''
						#if bool(re.search(r'(^class=\"_\w{3,10}\">[0-5]{1}.?[0-9]{0,2}[^( \W)])', one_separate)):
						reiting_separator = re.search(r'(^class=\"_\w{3,10}\">[0-5]{1}.?[0-9]{0,2}[^ оценокиблва<\W]*)', one_separate).group() \

						p = 0.0
						if bool(re.search(r'([0-5][.|,]?[0-9]{0,2}$)', str(reiting_separator))):
							p = float(re.search(r'([0-5][.|,]?[0-9]{0,2}$)', str(reiting_separator)).group())
							if p <= 5.0:
								self.reiting = "_{}".format(p)
						p = 0.0

					if bool(re.search(r'(>([0-9]{0,4} [оценокиблва]{0,10}))', str(one_separate))):
						'''
							:param self.count: how many people to leave your voice   
						'''
						self.count = "{}".format(
							re.search(r'(>([0-9]{0,4} [оценокблва]{0,10}))', str(one_separate)).group().lstrip(">"))

					'''page-data from the comnon column. It's has a many links.
					 Everyone links referencing into the page company. This's the page has the description only
						single company'''
					if bool(re.search(r'(^[А-ЯЁ]{1}[а-яА-ЯёЁ]{3,50})', str(one_separate[71:]))):
						get_geometry_name = r"(([0-9]{0,2}[-а-яё ]{0,4})?[а-яА-ЯёЁ -( )]{3,50}[, | ][а-яё ,( )0-9\/]{1,50}){1,}"
						if bool(re.search(rf'''{get_geometry_name}''', str(one_separate))):
							'''
								:param self.geometry_name: it's the simply address location 
							'''
							index_1 = re.search(rf'''{get_geometry_name}''', str(one_separate)).span()[0]
							geometry_name_separator = re.search(rf'''{get_geometry_name}''', str(one_separate[index_1:]))

							self.geometry_name = "{}".format(geometry_name_separator.group().rstrip("<"))
				ScraperInnerPage.scrap_gis_inner(self, self.title_link_company)
				ScraperEachAddress.get_sortedata(self, filename=self.filename, csv_file=True)
				'''
					Zero out data
				'''
				self.name = ''
				self.type_name=''
				self.reiting = ''
				self.count = ''
				self.geometry_name = ''
				self.lat = ''
				self.lon = ''
				self.phone = []
				self.email = ''
				self.vk = ''
				self.tg = ''
				self.wa = ''
				self.vib = ''
				self.ok = ''
				self.website = ''
				self.info = ''
				self.subcategory = ''
				self.work_mode=[]
				self.snijgp=[]
				self.src_img_feedback=[]
				self.src_img_company = []
			print('Страница обработана, должна быть запись')
	def get_sortedata(self, filename:str, csv_file = False):
		if bool(filename):
			search_word = ScraperEachAddress.get_search_word(self)
			city_name = ScraperEachAddress.get_city_name(self)
			data_to_File = {
				'Название': re.sub('\xa0', '', str(self.name)),
				'№': self.title_link_company,
				'Дата Добавления': datetime.date.today(),
				'Ключевое слово': str(search_word),  # ОБАВИТЬ на страницы - слова для поиска
				'Населенный пункт': str(city_name),
				'Рубрика': str(self.type_name),
				'Подраздел': self.subcategory,
				'Рейтинг': str(self.reiting),
				'Количество отзывов': str(self.count),
				'Адрес': str(self.geometry_name),
				'X-lat': str(self.lat),
				'Y-lon': str(self.lon),
				'Время Работы': str(self.work_mode),
				'Телефоны': str(self.phone),
				'Email': str(self.email),
				'Vk.com': str(self.vk),
				'Telegram': str(self.tg),
				'WatsApp': str(self.wa),
				'Viber': str(self.vib),
				'ВКонтакте': str(self.vk),
				'Ok': str(self.ok),
				'Сайт': str(self.website),
				'Информация': str(self.info),
				'Фото': str(self.src_img_company),
				'Комментарии': str(self.snijgp),
				'Фото-комментарии': str(self.src_img_feedback)
			}
			len(data_to_File)
			ScraperEachAddress.get_basic_data(self, filename, csv_file=csv_file, **data_to_File)





