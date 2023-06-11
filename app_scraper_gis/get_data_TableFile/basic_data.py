import pandas as pd
pd.set_option('display.width', 98)
import numpy as np
import scv
import pprint
import os
import csv

from app_scraper_gis.scraper_basic import Basic_gis
PATH_img = str(os.path.dirname(os.path.abspath(__file__)))

class BasicDataArray():
	def __init__(self, total_table = None):

		'''
		self.name: str = ""
		self.type_name: str = ''  # тип - под названием
		self.reiting: str = ""  # Рейтинг
		self.count: str = ""  # кол-во
		self.geometry_name: str = ""  # Адрес/местонахождения
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

		self.snijgp: list = []  # Комментарий
		self.pictures: list = []  # фото из комментариев
		'''
		get_phone = r'([(\+7)|(8)|(\+8)]{1}[0-9]{5,12})'
		get_WhatsApp = r'(wa.me\/)'
		get_mail = r'(\w{1,15}@\w{3,15}.\w{2,3})'
		get_ok = r'(ok\.ru\/)'
		get_tg = r'(t\.me/")'
		get_vk = r'(vk\.com\/)'
		get_points = r'([0-9]{1,3}.[0-9]{1,10})|([0-9]{,3}.{1}[0-9]{1,10})'
		get_website = r'http(s{0,1}):\/\/\w{0,25}.{0,1}\w{2,25}[^(2gis)|(w3)|(vk.)|(ok.)].ru'
		get_time_list = [ #????????
			r'(Ежедневно с [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Сегодня [c|с] [0-9]{2}:[0-9]{2} до [0-9]{2}:[0-9]{2})',
			r'(Откроется [завтра]{0,1} {0,1}в [А-ЯЁа-яё]{0,25}[в| ]{1,3}[0-9]{2}:[0-9]{2})',
		]
		self.name = ''
		self.type_name = '',
		self.reiting = '',
		self.count = '',
		self.geometry_name = '',
		self.lat = '',
		self.lon = '',
		self.phone = '',
		self.email = '',
		self.work_mode = [],
		self.vk = '',
		self.td = '',
		self.wa = '',
		self.ok = '',
		self.website = '',
		self.info = '',
		self.subcategory = '',
		self.snijgp = [],
		self.pictures = []
		self.photo_comapny: list = []
		self.total_table = total_table

	def get_sorting_data(self):
		self.basic_company = pd.Series({
			'name':str(self.name),
			'type_name':str(self.type_name),
			'reiting': str(self.reiting),
			'count': str(self.count),
			'geometry_name': str(self.geometry_name),
			'lat': str(self.lat),
			'lon': str(self.lon),
			'phone':str(self.phone),
			'email': str(self.email),
			'work_mode':str(self.work_mode),
			'vk': str(self.vk),
			#'tg': str(self.td),
			'wa': str(self.wa),
			'ok': str(self.ok),
			'website': str(self.website),
			'info': str(self.info),
			'subcategory': str(self.subcategory),
			'snijgp': list(self.snijgp),
			'pictures': list(self.pictures),

		})
		# BasicDataArray.creted_tabale_onCompany(self)
		name_comany = self.basic_company[0]
		data_company_keys = list(self.basic_company[1:].keys())
		data_company_values = list(self.basic_company[1:].values)

		new_table = pd.DataFrame({
			name_comany: data_company_values
		}, index=data_company_keys)
		print(new_table)

		# file = "./test_csv.csv"
		file = None
		if os.path.isdir(PATH_img) \
			and os.path.isfile(PATH_img + "\\test_csv.csv") == False:
			with open(PATH_img + "\\test_csv.csv", 'w', encoding='utf-8') as file: file.close()

		if os.stat(PATH_img + "\\test_csv.csv").st_size == 0:
			# with open(PATH_img + "\\test_csv.csv", 'w', encoding='utf-8') as file:  # file.close()
			#file = PATH_img + "\\test_csv.csv"
			# file = pd.read_csv(PATH_img + "\\test_csv.csv", sep=',', encoding="utf-8")
			file = open(PATH_img + "\\test_csv.csv", 'w', encoding='utf-8')
			print("my_file: ", file.encoding)
			df = pd.DataFrame(
				data= new_table.values,
				columns=list(new_table.columns),
				index=new_table.index,

			)
			df.to_csv(PATH_img + "\\test_csv.csv", mode="w",
			          encoding="cp1251",
			          sep=';'
			          )

		else:
			file = open(PATH_img + "\\test_csv.csv", 'w', encoding='utf-8')
			df = pd.read_csv(file,
			                 # encoding="cp1251",
			                 sep=';'
			                 )
			print("my_file_2: ", df.encoding)
			print("str(new_table.columns[0]): ", str(new_table.columns[0]))
			df[str(new_table.columns[0])] = new_table.values

			df.to_csv(PATH_img + "\\test_csv.csv", mode="w",
			          encoding="cp1251",
								sep=';'
			          )
	def creted_tabale_onCompany(self):
		self.name_comany = self.basic_company[0]
		data_company_keys = list(self.basic_company[1:].keys())
		data_company_values = list(self.basic_company[1:].values)

		new_table = pd.DataFrame({
			self.name_comany:data_company_values
		}, index=data_company_keys)
		print(new_table)
		# BasicDataArray.creted_tabale_total(self, new_table)
		total_table = pd.DataFrame().loc[:new_table.columns[0]] = new_table[1:].values
	def creted_tabale_total(self, table):

		total_table = pd.DataFrame().loc[:table.columns[0]] = table.values
		print(total_table)
