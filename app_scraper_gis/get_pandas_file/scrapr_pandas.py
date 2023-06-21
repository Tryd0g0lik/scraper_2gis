import pandas as pd
pd.set_option('display.width', 98)
import os, re
import datetime
#import numpy as np
#import scv
#import pprint
#import csv

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
		df_new = pd.DataFrame(data=kwargs, index=range(1), columns=list(kwargs.keys()) )

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

			df_data.to_csv(PATH_img + "\\..\\..\\" + filename + ".csv", mode="w",
			          encoding=encoding,
			          sep=';',
			          )
			print('Запись в новый файл')

		else:
			with open(PATH_img + "\\..\\..\\" + filename + ".csv", 'r', encoding=encoding) as f:
				df = pd.read_csv(f, sep=';', index_col=0)
				df.loc[len(list(df.index))] = df_data.iloc[0]

				try:
					print('Начало записи')
					df.fillna('NaN').to_csv(PATH_img + "\\..\\..\\" + filename + ".csv", mode="w",
												          encoding=encoding,
												          sep=';',
												          )
				except PermissionError:
					err = 'PermissionError: Кажется файл, в который должен записаться результат - открыт. Закройте. Метод  "create_csv"'
					print(err)
					return

			with open(PATH_img + "\\..\\..\\" + filename + ".csv", 'r') as f:
				df = pd.read_csv(f, sep=';', encoding=encoding, index_col=0)
				print('Запись прошла')

		print("END")
