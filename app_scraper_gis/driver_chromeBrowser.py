from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, InvalidSelectorException

import time
from app_scraper_gis.scraper_oneCompany import PATH
path_chrome: str = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

class ActionDriverChrome:
	def __init__(self, url: str, scroll:bool = False, click: bool = False, selector: str = '', ):
		'''
			If we want make the click-action, means the XPATH format-SELECTOR inserting
			:param url: data-source
			:param path_chrom: path to the Chrome.exe (from is the Program files folder)
			:param selector: it's the path with the html-element for will be work with the JavaScript
			:return: page-html
		'''
		self.url = url
		self.selector = selector
		self.scroll = scroll
		self.click = click
		self.start_working(self)


	def __page_loadeing(self):
		browser = Options()
		browser.binary_location = path_chrome
		self.driver = webdriver.Chrome(
			executable_path=str(PATH),
			chrome_options=browser
		)
		self.driver.get(str(self.url))
		time.sleep(3)
	
	def __action_acroll(self):
		if self.selector != '':

			'''
				JS  - scrolling the browser's window
			'''

			js_elem = "document.querySelector('" + (self.selector).strip() + "')"
			self.driver = self.page_loadeing(self)
			self.driver.execute_script(
				js_elem + '.scrollBy({top:' + js_elem + '.scrollHeight' + ', left: 0, behavior: "smooth"});')
			del js_elem

	def __action_click(self):
		if self.self.selector != '':
			'''
				Finding the html element and
				create the click-action for an element   
			'''

			# Определяем формат селектора
			by_format = None
			try:
				'''
					Проверка формата self.selector  на By.XPATH  
				'''
				self.driver = self.page_loadeing(self)
				element = self.driver.find_element(By.XPATH, self.selector)
				ActionChains(self.driver).click(element).perform()

			except (NoSuchElementException, InvalidArgumentException, InvalidSelectorException):
				'''
					Реализовать проверку на определение формата selector
					NAME = "name"
					TAG_NAME = "tag name"
					CLASS_NAME = "class name"
					CSS_SELECTOR = "css selector"
				'''
				print('Для реализации клика на странице Selector не найден или Selector в формате - XPATH' )
				print('Проблема в  getHtmlOfDriverChrome() из scraper_oneCompany.py')

			time.sleep(5)

	def start_working(self):
		self.__page_loadeing(self)
		if self.scroll: self.__action_acroll(self)
		if self.click: self.__action_click(self)
		html = self.driver.page_source
		self.driver.close()

		return html
