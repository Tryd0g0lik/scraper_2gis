import datetime
import re
from app_scraper_gis.get_pandas_file.scrapr_pandas import PandasWork
from app_scraper_gis.scraper_сompany import Company


class ScraperCompanies(Company, PandasWork):
	"""
		TODO: viewing each geometry_name
		:param 'name' it's the name company;
		:param search_word: it's the word or phrases for the search categories
		:param 'lat' it's the data coordinates about the width
		:param 'lon' it's the data coordinates about the long
		:param title_link_company: reference on the 2gis's column company from the title
		:param start_page: this's the start-page of the paginator's lit
	"""

	def __init__(self, filename:str, city: str = '', search_word: str = '', references = [], start_page: int = 0):
		super().__init__(city, search_word, references, start_page)
		ScraperCompanies.start_working(self)
		self.filename = (filename).strip()

	def scraper_companies(self, page, ):
		'''
		TODO: перебераем каждую найденую по запросу компанию
		:rpoperties: 'titleGisReference' getting the url for  a company. It's the URL from the primary common
		 column on the www-page.
		:return:
		'''
		self.geometry_name = ''
		self.reiting = ''
		self.count = ''
		self.type_name = ''
		self.lat = ''
		self.lon = ''
		self.name = ''
		for ind in range(len(page.contents) -1):
			if self.name != '':
				ScraperCompanies.get_sortedata(self, filename=self.filename, csv_file=True)

			if bool(page.contents[ind].find('a')) \
					and 'redirect.2gis' not in str(page.contents[ind].find('a')['href']) : # 'Реклама' not in str(page.contents[ind].find('a').parent.parent)
				self.title_link_company = "https://2gis.ru" + page.contents[ind].find('a')['href']
				self.name = page.contents[ind].find('span').text


				resp = page.contents[ind].find('a').parent.parent.contents
				if len(resp) > 1 :
					# if resp[len(resp)-1].name == 'div' or resp[len(resp)-1].name == 'span' \
					if bool(resp[-1].contents[0].name) \
						and 'Реклама' not in str(resp[-1]) \
						and 'Закр' not in resp[-1].text and 'Откр' not in resp[-1].text \
						and 'Скор' not in resp[-1].text and bool(resp[-1].contents[0].name) \
						and '<a' not in str(resp[-1]):
					  self.geometry_name = resp[-1].text

					elif bool(resp[-2].contents[0].name) \
						and 'Реклама' not in str(resp[-2]) \
						and 'Закр' not in resp[-2].text and 'Откр' not in resp[-2].text \
						and 'Скор' not in resp[-2].text\
						and '<a' not in str(resp[-2]):
					  self.geometry_name = resp[-2].text
					else:
					  self.geometry_name = resp[-3].text

				if len(resp) >= 2 \
					and len(resp[1]) == 1 \
					and resp[1].contents[0].name == 'span' \
					and len(resp[1].contents[0].contents[0].text) > 3:
					self.type_name = resp[1].contents[0].contents[0].text


				# resp = page.contents[ind].find('a').parent.parent.contents
				if len(resp) >= 3 \
					and len(resp[2].contents) >= 1:
					if len(resp) == 3 and bool(re.search(r'[оценкиа]{5,}', str(resp[1].contents))):
						self.reiting = '_' + resp[1].contents[len(resp[1].contents) - 2].text
						self.count = '_' + resp[1].contents[len(resp[1].contents) - 1].text

					elif bool(re.search(r'[оценкиа]{5,}', str(resp[2].contents))):
						self.reiting = '_' + resp[2].contents[0].contents[1].text
						self.count = '_' + resp[2].contents[0].contents[2].text

				Company.scrap_page_company(self, self.title_link_company)


	def get_sortedata(self, filename:str, csv_file = False):
		if bool(filename):
			# Задача! Разнести наполнение словоря по функциям. Базовую функцию вынести в шапку
			data_to_File = {
				'Название': re.sub('\xa0', '', str(self.name)),
				'№': self.title_link_company.encode('cp1251', errors='replace').decode('cp1251'),
				'Дата Добавления': datetime.date.today(),
				'Ключевое слово': str(self.search_word).encode('cp1251', errors='replace').decode('cp1251'),
				'Населенный пункт': str(self.сity_name).encode('cp1251', errors='replace').decode('cp1251'),
				'Рубрика': str(self.type_name).encode('cp1251', errors='replace').decode('cp1251'),
				'Подраздел': self.subcategory.encode('cp1251', errors='replace').decode('cp1251').lstrip('?').lstrip(' // '),
				'Рейтинг': str(self.reiting),
				'Количество отзывов': str(self.count),
				'Адрес': str(self.geometry_name).encode('cp1251', errors='replace').decode('cp1251'),
				'X-lat': str(self.lat),
				'Y-lon': str(self.lon),
				'Время Работы': str(self.work_mode),
				'Телефоны': str(self.phone),
				'Email': str(self.email),
				'Telegram': str(self.tg),
				'WatsApp': str(self.wa),
				'Viber': str(self.vib),
				'ВКонтакте': str(self.vk),
				'Однокласники': str(self.ok),
				'Сайт': str(self.website).lstrip('>'),
				'Информация': str(self.info),
				'Фото': str(self.src_img_company),
				'Комментарии': str(self.comment).encode('cp1251', errors='replace').decode('cp1251'),

			}

			ScraperCompanies.get_data(self, filename, csv_file=csv_file, **data_to_File)
			'''
				Zero out data
			'''
			self.name = ''
			self.type_name = ''
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
			self.work_mode = []
			self.comment = []
			self.src_img_feedback = []
			self.src_img_company = []





