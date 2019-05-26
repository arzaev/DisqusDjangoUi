from django.contrib import admin
from main.models import Group, Item

# Register your models here.


class GroupAdmin(admin.ModelAdmin):
	fieldsets = [
		("Name/date", {'fields': ['name', 'date']}),
		("Content", {'fields': ['infomation']})
	]


admin.site.register(Group, GroupAdmin)
admin.site.register(Item)
