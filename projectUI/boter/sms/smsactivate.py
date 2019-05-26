# coding: utf-8

import requests

# services:
# twitter: tw


class SmsActivate:
	def __init__(self, id, service, api):
		self.id = id
		self.service = service
		self.api = api

	def get_number_of_numbers(self):
		"""
		Twitter
		:return:
		"""
		url = 'http://sms-activate.ru/stubs/handler_api.php?api_key=%s&action=getNumbersStatus&country=$country' % self.api
		r = requests.get(url)
		return int(r.json()[self.service + '_0'])

	def get_balance(self):
		"""
		Get Balance
		:return:
		"""
		url = 'http://sms-activate.ru/stubs/handler_api.php?api_key=%s&action=getBalance' % self.api
		r = requests.get(url)
		return int(float(r.text.split(':')[1]))

	def get_number(self):
		"""
		Get Number

		Twitter: tw
		:return:
		"""
		url = 'http://sms-activate.ru/stubs/handler_api.php?api_key=%r&action=getNumber&service=%r&'\
			  % (self.api, self.service)
		r = requests.get(url)
		self.id = r.text.split(':')[1]
		number = r.text.split(':')[2]
		return number

	def iam_ready(self):
		"""
		Post information in service about operation
		:return:
		"""
		url = 'http://sms-activate.ru/stubs/handler_api.php?api_key=%r&action=setStatus&status=1&id=%r' % (self.api, self.id)
		r = requests.get(url)
		return r.text

	def get_code(self):
		"""
		Here I get the pin-code
		:return:
		"""
		url = 'http://sms-activate.ru/stubs/handler_api.php?api_key=%r&action=getStatus&id=%r' % (self.api, self.id)
		r = requests.get(url)
		return r.text

	def end(self):
		"""
		End operation
		:return:
		"""
		url = 'http://sms-activate.ru/stubs/handler_api.php?api_key=%r&action=setStatus&status=6&id=%r' % (self.api, self.id)
		r = requests.get(url)
		return r.text

	def delete(self):
		"""
		End operation
		:return:
		"""
		url = 'http://sms-activate.ru/stubs/handler_api.php?api_key=%r&action=setStatus&status=8&id=%r' % (self.api, self.id)
		r = requests.get(url)
		return r.text
