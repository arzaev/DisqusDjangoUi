# coding: utf-8

import time
import requests


class Recaptcha:

	def __init__(self, url, api_key, google_key):
		# self.user_proxy = user_proxy
		# self.password_proxy = password_proxy
		self.api_key = api_key
		self.session = requests.Session()
		self.url = url
#		self.proxy = proxy
		self.google_key = google_key 

	def decide_captcha(self):
		time.sleep(10)
		r = self.session.post("http://rucaptcha.com/in.php", data={
			'key': self.api_key,
			# 'login': self.user_proxy,
			# 'password': self.password_proxy,
			'method': 'userrecaptcha',
			'googlekey': self.google_key,
			'pageurl': self.url,
#			'proxy': self.proxy,
			'proxytype': 'HTTP'
		}, verify=False)
		id = r.content
		id = int(id[3:].decode())
		res = self._check_recaptcha(id)
		return res

	def _check_recaptcha(self, id):
		for i in range(12):
			print('wait')
			time.sleep(5)
			r2 = self.session.get("http://rucaptcha.com/res.php", params={
				'key': self.api_key,
				'action': 'get',
				'id': id

			}, verify=False)
			res = r2.content.decode().split("|")
			if res[0] == 'OK':
				return res[1]
		return ''
	
	def wait_time(self, t):
		for i in range(t):
			time.sleep(5)
			captcha = self.decide_captcha()
			if captcha != '':
				return captcha

	# def send_google_request(self, res, recaptcha_token):
	#	 result = self.session.post('https://www.google.com/recaptcha/api2/userverify?k=6LcU4gkTAAAAAM4SyYTmXlKvqwWLuaFLy-30rzBn', data={'bg': res, 'c': recaptcha_token})
	#	 print result.content

