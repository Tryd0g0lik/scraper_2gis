import pandas as pd
pd.set_option('display.width', 98)
import numpy as np
import scv
import pprint
import os, re
import datetime
import csv

PATH_img = str(os.path.dirname(os.path.abspath(__file__)))

class PandasWork():
	def __init__(self,):

		'''

		self.name: str = ""
		self.type_name: str = 'NaN'  # тип - под названием
		self.reiting: str = ""  # Рейтинг
		self.count: str = ""  # кол-во
		self.geometry_name: str = ""  # Адрес/местонахождения
		self.lat: str = 'NaN'  # широта
		self.lon: str = 'NaN'  # долгота
		self.phone: str = 'NaN'
		self.email: str = 'NaN'
		self.work_mode: str = 'NaN'
		self.vk: str = 'NaN'  # ВКонтакте
		self.tg: str = 'NaN'  # Telegram
		self.wa: str = 'NaN'  # WhatsApp
		self.ok: str = 'NaN'  # OK
		self.website: str = 'NaN'
		self.info: str = ""
		self.subcategory: str = ""  # подкатегория

		self.snijgp: list = []  # Комментарий
		self.pictures_feedback: list = []  # фото из комментариев
		'''

	def get_data(self, filename:str, csv_file:bool = False, **kwargs):
		date_ = str(datetime.date.today())
		filename = date_+ "_" + kwargs['Населенный пункт'] + '_' + filename
		len(kwargs)
		'''
		:param csv_file: It's a bool value. It's a properties has the False value by default.
			 True - create the CSV-file
		:param filename: file name from the return file

		:return:
		'''
		# if kwargs['Время Работы'] == [[]]: kwargs['Время Работы'] = ''
		# if kwargs['Фото'] == [[]]: kwargs['Фото'] = 'NaN'
		# if kwargs['Комментарии'] == [[]]: kwargs['Комментарии'] = ''
		# if kwargs['Фото-комментарии'] == [[]]: kwargs['Фото-комментарии'] = ''
		len(kwargs)
		df_new = pd.DataFrame(data=kwargs,
		                  index=list(kwargs.values())[:1],
		                  columns=list(kwargs.keys())[1:])

		if csv_file == True and len(filename) > 0:
			PandasWork.create_csv(self, filename=filename, df_data=df_new)

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
			# file = open(PATH_img + "\\..\\..\\" + filename + ".csv", 'w', encoding=encoding)
			# file.close()
			# df_data['Информация'] = re.sub(u'u[0-9]\w{1,5}', ' ', df_data['Информация'])
			# df_data['Комментарии'] = re.sub(u'u[0-9]\w{1,5}', ' ', df_data['Комментарии'])

			df_data.to_csv(PATH_img + "\\..\\..\\" + filename + ".csv", mode="w",
			          encoding=encoding,
			          sep=';',
			          )

		else:
			df = pd.read_csv(PATH_img + "\\..\\..\\" + filename + ".csv", sep=';', encoding="cp1251", index_col=0)

			# print("str(new_table.columns[0]): ", str(df_data.columns[0]))
			df.loc[df_data.index[0]] = df_data.iloc[0]

			try:
				df.fillna('NaN').to_csv(PATH_img + "\\..\\..\\" + filename + ".csv", mode="w",
				          encoding=encoding,
				          sep=';',

				          )
			except PermissionError:

				err = 'PermissionError: Кажется файл, в который должен записаться результат - открыт. Закройте. Метод  "create_csv"'
				print(err)
				return
		print("END")
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
