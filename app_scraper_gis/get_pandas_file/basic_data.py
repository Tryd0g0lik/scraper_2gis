import pandas as pd
pd.set_option('display.width', 98)
import numpy as np
import scv
import pprint
import os
import datetime
import csv

PATH_img = str(os.path.dirname(os.path.abspath(__file__)))

class BasicDataArray():
	def __init__(self,):

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
		self.pictures_feedback: list = []  # фото из комментариев
		'''

		self.name = ''
		self.type_name = '',
		self.reiting = '',
		self.count = '',
		self.geometry_name = '',
		self.lat = '',
		self.lon = '',
		self.phone = '',
		# self.search_word = ''
		self.email = '',
		self.work_mode = [],
		self.vk = '',
		self.tg = '',
		self.wa = '',
		self.ok = '',
		self.website = '',
		self.info = '',
		self.subcategory = '',
		self.snijgp = [],
		self.src_img_feedback = []
		self.src_img_company: list = []#
		self.city:str = ''
		

	def get_basic_data(self, filename:str, csv_file:bool = False, **kwargs):
		date_ = str(datetime.date.today())
		filename = date_+ "_" + kwargs['Населенный пункт'] + '_' + filename

		self.basic_series = pd.Series(kwargs)
		'''
		:param csv_file: It's a bool value. It's a properties has the False value by default.
			 True - create the CSV-file
		:param filename: file name from the return file

		:return:
		'''
		df =  pd.DataFrame({
			self.basic_series[0]: list(self.basic_series[1:].values)
		}, index=list(self.basic_series[1:].keys()))
		# df =  pd.DataFrame({
		# 			self.basic_series[0]: list(self.basic_series[1:].values)
		# 		}, index=list(self.basic_series[1:].keys()))

		if csv_file == True and len(filename) > 0:
			BasicDataArray.create_csv(self, filename=filename, df_data=df)

	def create_csv(self, df_data, filename:str, encoding:str="cp1251"):
		'''
		:param df_data: it's DataFrame data
		:param encoding: it's properties show encoding. default=cp1251
		:return:
		'''
		if os.path.isdir(PATH_img) \
			and os.path.isfile(PATH_img + "\\..\\..\\" + filename + ".csv") == False:
			with open(PATH_img + "\\..\\..\\" + filename + ".csv", 'w', encoding=encoding) as file: file.close()

		if os.stat(PATH_img + "\\..\\..\\" + filename + ".csv").st_size == 0:
			file = open(PATH_img + "\\..\\..\\" + filename + ".csv", 'w', encoding=encoding)
			file.close()

			df = pd.DataFrame(
				data= df_data.values,
				columns=list(df_data.columns),
				index=df_data.index,

			)
			df.to_csv(PATH_img + "\\..\\..\\" + filename + ".csv", mode="w",
			          encoding=encoding,
			          sep=';',
			          )


		else:
			df = pd.read_csv(PATH_img + "\\..\\..\\" + filename + ".csv",
			                 sep=';',
			                 encoding="cp1251",
			                 index_col=0
			                 )

			print("str(new_table.columns[0]): ", str(df_data.columns[0]))
			df[str(df_data.columns[0])] = df_data[0:]

			try:
				df.to_csv(PATH_img + "\\..\\..\\" + filename + ".csv", mode="w",
				          encoding=encoding,
				          sep=';',

				          )
			except PermissionError:

				err = 'PermissionError: Кажется файл, в который должен записаться результат - открыт. Закройте. Метод  "create_csv"'
				print(err)
				return
	# def creted_tabale_onCompany(self):
	# 	self.name_comany = self.basic_series[0]
	# 	data_company_keys = list(self.basic_series[1:].keys())
	# 	data_company_values = list(self.basic_series[1:].values)
	#
	# 	new_table = pd.DataFrame({
	# 		self.name_comany:data_company_values
	# 	}, index=data_company_keys)
	# 	print(new_table)
	# 	# BasicDataArray.creted_tabale_total(self, new_table)
	# 	total_table = pd.DataFrame().loc[:new_table.columns[0]] = new_table[1:].values
	# def creted_tabale_total(self, table):
	#
	# 	total_table = pd.DataFrame().loc[:table.columns[0]] = table.values
	# 	print(total_table)
