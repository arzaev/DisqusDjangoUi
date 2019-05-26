# coding: utf-8

import requests
import urllib3
urllib3.disable_warnings()


class InitBot:
	def __init__(self, proxy=True, item_proxy='192.168.0.100:8080', type_proxy='https', user_agent='python3', verify=False, timeout=10):
		self.user_agent = user_agent
		self.session = requests.Session()
		self.item_proxy = item_proxy
		self.type_proxy = type_proxy
		if type_proxy == 'socks5':
			self.proxies = {
				'http': 'socks5://{}'.format(item_proxy),
				'https': 'socks5://{}'.format(item_proxy)
			}
		else:
			if '@' in item_proxy:
				self.proxies = {'http': 'http://{}'.format(item_proxy),
								'https': 'https://{}'.format(item_proxy)}
			else:
				self.proxies = {'http': item_proxy, 'https': item_proxy}
		self.verify = verify
		self.timeout = timeout
