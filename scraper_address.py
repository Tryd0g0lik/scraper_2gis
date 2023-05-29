from scraper_gis import Gis_page
from threading import Timer
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
	def __init__(self, sity:str='', search_word:str = ''):
		super().__init__(sity, search_word)
		ScraperEachAddress.start_working(self)
		self.name :str = ""
		self.type_name:str = '' # тип - под названием
		self.reiting:str = "" # Рейтинг
		self.count:str = "" # кол-во 
		self.address:str = "" # Адрес/местонахождения

		self.snijgp :str = '' #  краткое описание См. "описание.png"
		self.geometry_name :str = ''
		self.phone :str = ''
		self.email :str = ''
		self.work_mode :str = ''
		self.website :str = ''
		self.lat :str = '' # широта
		self.lon :str = ''  # долгота
		self.vk :str = '' # ВКонтакте
		self.tg :str = ''  # Telegram
		self.wa :str = '' # WhatsApp
		# t = Timer(30.0, ScraperEachAddress.iterating_over_company(self, self.object_soup))
		# t.start()
		ScraperEachAddress.iterating_over_company(self, self.object_soup)

	def iterating_over_company(self, page):
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


			# print("match: ", (match_list))

			while i <= 2:
				for one_company in match_list:
					for one_separate in one_company.split("</div><div"):
						print(f"index {i}: ", one_company)
						one_separate = one_separate.lstrip()

						reg_link_text = r'''(<a\sclass=[\"|\']_\w{3,10}[\"|\']\shref=[\"|\'][\/\w]*[\"|\']><span)'''
						reg_titleGisReference = r'''([\"|\']\/\w*\/?[\w\/]*\/?[\"|\']?)'''

						# reg_name = r'''(<span class=[\"|\']_\w{3,10}[\"|\'])'''
						reg_name = r'''(<span class=[\"|\']_\w{3,10}[\"|\']>[\w|\W]{2,100}</span> ?[^(<!-)])'''

						reg_type_name = r'''(^ class=[\"|\']_\w{3,10}[\"|\']><span class=[\"|\']_\w{3,10}[\"|\']>[^(<!-)][\w|\W]{2,100}<\/span> ?)''' #[^(!--)]
						# print("one_separate: ", one_separate)
						if bool(re.search(reg_link_text, str(one_separate))):
							# print("one_separate: ", one_separate)
							link_text = re.search(reg_link_text, str(one_separate)).group()
							titleGisReference = "https://2gis.ru{}".format((re.search(reg_titleGisReference, str(link_text)).group()).strip('"').strip("'"))
							print("titleGisReference: ", titleGisReference)

						if bool(re.search(reg_name, str(one_separate))):
							# print("one_separate: ", one_separate)
							name = str(re.search(reg_name, str(one_separate)).group())
							# print("name: ", name)
							self.name ="{}".format((name.lstrip(r'''(<span class=[\"|\']_\w{5,10}[\"|\']>)''').lstrip('f"><span>')).replace('</span>', ""))
							print("self.name: ",self.name)

						elif bool(re.search(reg_type_name, str(one_separate))):
							# print("one_separate: ", one_separate.lstrip())

							type_name = str(re.search(reg_type_name, str(one_separate)).group())
							type_name = re.search(r"([\w|\W]{3,100}<)", type_name).group().rstrip("<").strip()
							type_name_separator = re.search(r"""(^class=[\"|\']_\w{3,10}[\"|\']><span class=[\"|\']_\w{3,10}[\"|\']>)""", type_name).group().__str__()
							self.type_name = "{}".format(type_name.lstrip(str(type_name_separator)))
							print("type_name:",self.type_name)
						# print("reg_type_name: ", re.search(reg_type_name, str(one_separate)))

						# elif bool(re.search(r'(^class=\"_\w{3,10}\">[0-5]{1,2}.?[0-9]{0,2}[^( \W)])', one_separate)):
						elif bool(re.search(r'(^class=\"_\w{3,10}\">[0-5]{1,2}.?[0-9]{0,2}[^( \W)])', one_separate)):
							# print("one_separate: ", one_separate)
							reiting_separator = re.search(r'(^class=\"_\w{3,10}\">[0-5]{1,2}.?[0-9]{0,2}[^( \W)])', one_separate).group()
							self.reiting = "{}".format(re.search(r'([[0-5]{1,2}.{0,1}[0-9]{0,2}$|[0-5]{1,2}$])', reiting_separator).group())

							print("self.reiting: ", self.reiting)


						# elif bool(re.search(r'(^class=\"_\w{3,10}\">[0-9]{1,2})', one_separate)):
						elif bool(re.search(r'(>([0-9]{0,2} [оценокблва]{0,10}))', one_separate)):
							self.count = "{}".format(re.search(r'(>([0-9]{0,2} [оценокблва]{0,10}))', one_separate).group().lstrip(">"))

							print("self.count: ", self.count)

						elif bool(re.search(r'(^[А-ЯЁ]{1}[а-яА-ЯёЁ]{3,50})', one_separate[71:])):
							group1 = r"(^[А-ЯЁ]{1}[а-яА-ЯёЁ]{3,50}[, | ]{1}[^(\&nbsp;)][а-яё ,0-9\/]{1,50})"
							group2 = r"([^(\&nbsp;)][[А-ЯЁа-яё .,0-9\/]|[^(\&nbsp;)][А-ЯЁа-яё .,0-9\/]{1,220}]{1,10}[^(\&nbsp;)])"
							group3 = r"([^(\&nbsp;)][[А-ЯЁа-яё .,0-9]{1,220}|[А-ЯЁа-яё .,0-9]{1,220}]{0,10}[^(\&nbsp;)]{0,2})"
							group4 = r"([^(\&nbsp;)][[А-ЯЁа-яё .,0-9]{1,220}|[А-ЯЁа-яё .,0-9]{1,220}]{0,10}[^(\&nbsp;)])"
							address_separator = re.search(
								rf'''({group1}{group2}{group3}{group4})''', one_separate[71:]).group().rstrip("<")
							self.address = "{}".format(address_separator)
							print("self.address: ", self.address)

						# print("count: ", one_separate)

					i +=1


	def search_inner_company(self, data):

		return ScraperEachAddress.search_church()
	def get_inner_data_company(self):
		pass
