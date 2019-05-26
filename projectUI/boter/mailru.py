# coding: utf-8

from requests import Session
import time
from urllib.parse import quote_plus, unquote_plus


class MailRu:
	def __init__(self, **kwargs):
		self.proxy = kwargs['proxy']
		if kwargs['type_proxy'] == 'socks5':
			self.proxies = {
				'http': 'socks5://{}'.format(kwargs['proxy']),
				'https': 'socks5://{}'.format(kwargs['proxy'])
			}
		else:
			if '@' in kwargs['proxy']:
				self.proxies = {'http': 'http://{}'.format(kwargs['proxy']),
								'https': 'https://{}'.format(kwargs['proxy'])}
			else:
				self.proxies = {'http': kwargs['proxy'], 'https': kwargs['proxy']}
		self.user_agent = kwargs['user_agent']
		self.email_login = kwargs['email_login']
		self.email_password = kwargs['email_password']
		self.session = Session()

	def get_main_page(self):
		url = 'https://mail.ru/'
		headers = {'Host': 'mail.ru',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		self.csrf_token = r.text.split('CSRF:"')[1].split('"')[0]

	def js_api_auth(self):
		timer = str(time.time()).split('.')[0]
		url = 'https://auth.mail.ru/jsapi/auth'
		data = 'login={login}' \
			   '&password={password}' \
			   '&saveauth=1&token={csrf_token}' \
			   '&project=e.mail.ru&_={timer}'.format(login=quote_plus(self.email_login),
													 password=self.email_password,
													 csrf_token=self.csrf_token,
													 timer=timer
													 )
		headers = {'Host': 'auth.mail.ru',
				   'User-Agent': self.user_agent,
				   'Accept': '*/*',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': 'https://mail.ru/',
				   'Content-type': 'application/x-www-form-urlencoded',
				   'Content-Length': str(len(data)),
				   'Origin': 'https://mail.ru',
				   'Connection': 'close',
				   }
		self.session.post(url, headers=headers, data=data, proxies=self.proxies, verify=False, allow_redirects=False)

	def cgi_bin(self):
		login = str(self.email_login).split('@')[0]
		url = 'https://auth.mail.ru/cgi-bin/auth?from=splash'
		data = 'Login={login}' \
			   '&Domain=mail.ru&Password={password}' \
			   '&saveauth=1&FromAccount=0&token={csrf_token}'.format(login=login,
																	 password=self.email_password,
																	 csrf_token=self.csrf_token
																	 )
		headers = {'Host': 'auth.mail.ru',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': 'https://mail.ru/',
				   'Content-Type': 'application/x-www-form-urlencoded',
				   'Content-Length': str(len(data)),
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		self.session.post(url, headers=headers, data=data, proxies=self.proxies, verify=False, allow_redirects=False)

	def messages_inbox_back1(self):
		url = 'https://e.mail.ru/messages/inbox/?back=1'
		headers = {'Host': 'e.mail.ru',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': 'https://mail.ru/',
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)

	def auth_mail_ru_sdc(self):
		url = 'https://auth.mail.ru/sdc?from=https%3A%2F%2Fe.mail.ru%2Fmessages%2Finbox%2F%3Fback%3D1'
		headers = {'Host': 'auth.mail.ru',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': 'https://mail.ru/',
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		self.next_link = r.headers['location']

	def sdc_token(self):
		url = self.next_link
		headers = {'Host': 'e.mail.ru',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': 'https://mail.ru/',
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)

	def messages_inbox_back1_2(self):
		url = 'https://e.mail.ru/messages/inbox/?back=1'
		headers = {'Host': 'e.mail.ru',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': 'https://mail.ru/',
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		tarball = r.text.split("(window.patron, '")[1].split("'")[0]
		tab_time = r.text.split('code_no-js:1&rnd=')[1].split('&vid=')[0]
		token = quote_plus(r.text.split('patron.updateToken("')[1].split('");')[0])
		self.next_link = 'https://e.mail.ru/api/v1/golang/messages/status?ajax_call=1&x-email={x_email}' \
						'&tarball={tarball}' \
						'&tab-time={tab_time}' \
						'&email={x_email}' \
						'&sort=%7B%22type%22%3A%22date%22%2C%22order%22%3A%22desc%22%7D' \
						'&offset=0&limit=26&folder=0&htmlencoded=false&last_modified=1&filters=%7B%7D&nolog=0&sortby=D' \
						'&rnd=0.2883183591092989&api=1' \
						'&token={token}'.format(x_email=quote_plus(self.email_login),
													tarball=tarball,
													  tab_time=tab_time,
													token=token

								  )

	def api_v1_golang(self, mess):
		url = self.next_link
		headers = {'Host': 'e.mail.ru',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/plain, */*; q=0.01',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': 'https://e.mail.ru/messages/inbox/?back=1',
				 #  'X-Request-Id': '18c75ad5-6db3-8ea5-d8f3-ed5c1dcd81c5',
				   'X-Requested-With': 'XMLHttpRequest',
				   'Connection': 'close',
				   }
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		item = r.text.split(mess)[1].split('"subject"')[0]
		self.id = item.split('"id":"')[1].split('"')[0]

	def get_message_page(self):
		url = 'https://e.mail.ru/message/' + self.id + '/'
		headers = {'Host': 'e.mail.ru',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': 'https://mail.ru/',
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		self.tarball = r.text.split("window.patron, '")[1].split("'")[0]
		self.tabtime = r.text.split("CurrentTimestamp:		'")[1].split("'")[0]
		self.token = r.text.split('patron.updateToken("')[1].split('"')[0]

	def last_message(self):
		url = 'https://e.mail.ru/api/v1/messages/message?ajax_call=1&x-email={email}&tarball={tarball}&tab-time={tab_time}&o_ss=&o_v=&email={email}&htmlencoded=false&multi_msg_prev=0&multi_msg_past=0&sortby=&NewAttachViewer=1&AvStatusBar=1&let_body_type=let_body_plain&log=1&folder=0&wrap_body=0&id={id}&read={id}&sm=0&NoMSG=true&mark_read=true&api=1&token={token}'.format(email=quote_plus(self.email_login), tarball=self.tarball, tab_time=self.tabtime, id=self.id, token=quote_plus(self.token))
		headers = {'Host': 'e.mail.ru',
						'User-Agent': self.user_agent,
						'Accept': 'text/plain, */*; q=0.01',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Referer': 'https://e.mail.ru/message/{}/'.format(self.id),
					#	'X-Request-Id': 'f2491230-f0d7-1b19-f5a0-6862b997f28',
						'X-Requested-With': 'XMLHttpRequest',
						'Connection': 'close',
						}
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		return r.text




	def start(self, mess):
		self.get_main_page()
		self.js_api_auth()
		self.cgi_bin()
		self.messages_inbox_back1()
		self.auth_mail_ru_sdc()
		self.sdc_token()
		self.messages_inbox_back1_2()
		self.api_v1_golang(mess)
		self.get_message_page()
		mail = self.last_message()
		return mail
#		return self.link

#alexa.wesley.98@mail.ru:afywou378FHnVi:Alexa:Wesley:0:26.08.1998


#mail = MailRu(proxy='192.168.0.100:8080',
#					type_proxy='http',
#					email_login='alexa.wesley.98@mail.ru',
#					email_password='afywou378FHnVi',
#					user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
#					)
#mess = mail.start('"noreply@xhamster.com"')
#mess = mess.split('xhamster.com%252Fconfirm%253Fvcode%253D')[1].split('%26c%3Dswm%2')[0]
#print(mess)
# mail.get_main_page()
# mail.js_api_auth()
# mail.cgi_bin()
# mail.messages_inbox_back1()
# mail.auth_mail_ru_sdc()
# mail.sdc_token()
# mail.messages_inbox_back1_2()
# mail.api_v1_golang()
# mail.get_message_page()

