from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import	Group, Item 
import json
from pathlib import Path
from project import settings
from threading import Thread
from django.contrib.auth.decorators import login_required
import ast
import logging
from scripts import set_proxy, profile, spam_text, spam_photo, check, spam_chat, like, confirm_email
# Create your views here.

name_project = "Disqus"
color_header = "#2d9fff"
icon = "icondisqus.png"
log = "disqus.log"

logger = logging.getLogger('server_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('logs/{}'.format(log))
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

@login_required(login_url='/')
def homepage(request):
	context = {}
	context['name_project'] = name_project	
	context['color_header'] = color_header
	context['icon'] = icon
	context['campaigns'] = Group.objects.all()
	context['groups'] = Group.objects.all()
	context['data'] = Item.objects.all()
	return render(	request=request,
					template_name='main/base.html',
					context=context
					)


@login_required(login_url='/')
def get_list(request):
	context = {}
	context['name_project'] = name_project	
	context['color_header'] = color_header
	context['icon'] = icon
	context['groups'] = Group.objects.all()
	context['data'] = Item.objects.all()
	return render(	request=request,
					template_name='main/list.html',
					context=context
					)


@login_required(login_url='/')
def add_group(request):
	if request.is_ajax():
		data = json.loads(request.body.decode('utf-8'))
		group = data['group']
		Group(name=group).save()
	return HttpResponse('/project/list/')


@login_required(login_url='/')
def add_items(request):
	if request.is_ajax():
		data = json.loads(request.body.decode('utf-8'))
		group = data['group']
		group = Group.objects.get(name=group)
		items = data['items'].split('\n')
		for i in items:
			item = ast.literal_eval(i)
			try:
				Item(name=item['login'],
					 group=group,
					 login=item['login'],
					 password=item['password'],
					 email=item['email'],
					 cookie=item['cookie'],
					 user_agent=item['user_agent']).save()
			except Exception as error:
				logger.warning(str(error))
	return HttpResponse('/project/list/')


@login_required(login_url='/')
def read_log(request):
	if request.is_ajax():
		with open(str(Path(f'logs/{log}'))) as f:
			_log = f.read()
	return JsonResponse({'data': _log})


@login_required(login_url='/')
def remove_log(request):
	if request.is_ajax():
		with open(str(Path(f'logs/{log}')), 'w') as f:
			f.write('')
	return JsonResponse({})


@login_required(login_url='/')
def action(request):
	output = ''
	if request.is_ajax():
		data = json.loads(request.body.decode('utf-8'))
		if data['command'] == 'delete':
			def start(data):
				for id in data['list']:
					Item.objects.get(id=int(id)).delete()			
			t = Thread(target=start, args=(data, ))	
			t.daemon = True
			t.start()
		elif data['command'] == 'set_proxy':
			def start(data):
				set_proxy.set_proxy(data, logger)
			t = Thread(target=start, args=(data, ))	
			t.daemon = True
			t.start()
		elif data['command'] == 'profile':
			def start(data):
				profile.start(data, logger)
			t = Thread(target=start, args=(data, ))	
			t.daemon = True
			t.start()
		elif data['command'] == 'spam_text':
			def start(data):
				spam_text.start(data, logger)
			t = Thread(target=start, args=(data, ))	
			t.daemon = True
			t.start()
		elif data['command'] == 'spam_photo':
			def start(data):
				spam_photo.start(data, logger)
			t = Thread(target=start, args=(data, ))	
			t.daemon = True
			t.start()
		elif data['command'] == 'check':
			def start(data):
				check.start(data, logger)
			t = Thread(target=start, args=(data, ))	
			t.daemon = True
			t.start()
		elif data['command'] == 'confirm_email':
			def start(data):
				confirm_email.start(data, logger)
			t = Thread(target=start, args=(data, ))	
			t.daemon = True
			t.start()
		elif data['command'] == 'spam_chat':
			def start(data):
				spam_chat.start(data, logger)
			t = Thread(target=start, args=(data, ))	
			t.daemon = True
			t.start()
		elif data['command'] == 'like':
			def start(data):
				like.start(data, logger)
			t = Thread(target=start, args=(data, ))	
			t.daemon = True
			t.start()
		elif data['command'] == 'gp':
				"""
				Here I am going to get posts ids 
				"""
				list_gp = []
				for id in data['list']:
					if id != '\n':
						item = Item.objects.get(id=int(id))			
						list_gp.append(item.storage_post)
				output = "\n".join(list_gp)
		elif data['command'] == 'ga':
				"""
				Here I wanna get acc info. Kind of password and login	
				"""
				list_ga = []
				for id in data['list']:
					if id != '\n':
						item = Item.objects.get(id=int(id))			
						list_ga.append(item.login + ':' + item.password)
				output = "\n".join(list_ga)
		elif data['command'] == 'get_storage':
				"""
				If spam doesn't work I can get posts here
				"""
				list_ga = []
				for id in data['list']:
					if id != '\n':
						item = Item.objects.get(id=int(id))			
						list_ga.append(item.storage_base)
				output = "\n".join(list_ga)
	return JsonResponse({'o': output})
