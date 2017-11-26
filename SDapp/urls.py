from django.conf.urls import url
from SDapp import views
from api import *

urlpatterns = [
	url(r'^customers/$', CustomerList.as_view()),
	url(r'^customers/(?P<username>.+)/$', CustomerDetail.as_view()),
]