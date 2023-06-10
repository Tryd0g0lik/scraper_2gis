import pandas as pd
import numpy as np
import pprint
class BasicDataArray():
	def __init__(self):

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
		self.work_mode = '',
		self.vk = '',
		self.td = '',
		self.wa = '',
		self.ok = '',
		self.website = '',
		self.info = '',
		self.subcategory = '',
		self.snijgp = [],
		self.pictures = []

	def get_sorting_data(self):

		# print("XXX: ",
	  #   self.name,
		# 	self.type_name,  # тип - под названием
		# 	self.reiting,  # Рейтинг
		# 	self.count,  # кол-во
		# 	self.geometry_name,  # Адрес/местонахождения
		# 	self.lat, # широта
		# 	self.lon,  # долгота
		# 	self.phone
		# )
		one_object = pd.Series({
			'name': str(self.name),
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
			'pictures': list(self.pictures)
		})
		print(one_object)
