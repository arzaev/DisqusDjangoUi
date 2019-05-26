from django.db import models
from django.utils import timezone
# Create your models here.


class Group(models.Model):
	name = models.CharField(max_length=255)
	infomation = models.TextField(default='-')
	date = models.DateTimeField(default=timezone.now) 
	
	def __str__(self):
		return self.name 


class Item(models.Model):
	name = models.CharField(max_length=255)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)

	login = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	cookie = models.TextField(default='-')
	user_agent = models.TextField(default='-')

	proxy = models.CharField(max_length=255)
	type_proxy = models.CharField(max_length=255)

	profile = models.BooleanField(default=False)

	base_all = models.IntegerField(default=0)
	base_get = models.IntegerField(default=0)

	status = models.CharField(max_length=255)
	target = models.CharField(max_length=255)

	notification = models.IntegerField(default=0)
	upvotes = models.IntegerField(default=0)
	removed = models.IntegerField(default=0)
	
	storage_base = models.TextField()
	storage_post = models.TextField()

	def __str__(self):
		return self.name
	
