# res_word = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in word) - unicode

# Кодирование не ASCII символов в URL-адресе
# from urllib.parse import unquote, quote - url кодирование

# Unicod в строке - удалить
	# result = "тут_строка".encode('cp1251', 'ignore').decode('cp1251')
	# или через регулярки


# encode() и decode()
# Источник: https://pythononline.ru/osnovy/encode-decode
# https://www.tutorialspoint.com/python/string_decode.htm