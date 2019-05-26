from . import views
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = "main"


urlpatterns = [
	path(r"", views.homepage, name="homepage"),
	path(r"list/", views.get_list, name="list"),
	path(r"add_items/", views.add_items, name="add_items"),
	path(r"add_group/", views.add_group, name="add_group"),
	path(r"read_log/", views.read_log, name="read_log"),
	path(r"remove_log/", views.remove_log, name="remove_log"),
	path(r"action/", views.action, name="action"),
] + staticfiles_urlpatterns()





