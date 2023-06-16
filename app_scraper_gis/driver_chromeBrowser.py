from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, InvalidSelectorException

import time, os
PATH = os.path.dirname(os.path.abspath(__file__)) + "\\chromedriver\\chromedriver.exe"
PATH_img = str(os.path.dirname(os.path.abspath(__file__))) + '\\file'
path_chrome: str = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

class ActionDriverChrome:
	def __init__(self, url: str, selector: str = '', ):
		'''
			TODO: Seleniume-Library If we want make the click-action or csoll, means the XPATH format-SELECTOR inserting


			:param url: data-source
			:param path_chrom: path to the Chrome.exe (from is the Program files folder)
			:param selector: it's the path with the html-element for will be work with the JavaScript
			:return: page-html
		'''
		self.url = url
		self.selector = selector


	def page_loading(self):
		'''
		:return:
		'''
		browser = Options()
		browser.binary_location = path_chrome
		self.driver = webdriver.Chrome(
			executable_path=str(PATH),
			chrome_options=browser
		)
		self.driver.get(str(self.url)) # open url

	def get_page(self):
		html = self.driver.page_source # get html-page

		pass
		time.sleep(3)
		return html
	
	def action_acroll(self, scroll:bool = False):
		'''
			TODO: JS  - scrolling the browser's window
			 Page_loading() - method  don't forget to run before the scrolling start
		'''
		if self.selector != '' \
			and scroll == True:
			js_elem = "document.querySelector('" + (self.selector).strip() + "')"
			# self.page_loadeing()

			self.driver.execute_script(
				js_elem + '.scrollBy({top:' + js_elem + '.scrollHeight' + ', left: 0, behavior: "smooth"});')
			del js_elem


	def action_click(self, click: bool = False):
		'''
			TODO: Finding the element-html and
			 make the click-action for an element
			 Page_loading() - method  don't forget to run before the scrolling start

		  :param click: this's False default
		'''
		if self.selector != '' \
			and click == True:
			try:
				'''
					Проверка формата self.selector  на By.XPATH  
				'''
				# self.page_loadeing()
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

	def closed_browser(self):
		self.driver.close()



