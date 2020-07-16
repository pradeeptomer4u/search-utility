from django.conf.urls import url
from django.urls import path
from search.views import ListRCEntryView

app_name = 'search'
urlpatterns = [
    url(r'^product/$', ListRCEntryView.as_view(), name="product_home"),
url(r'^product/(?P<page>[0-9]+)/$', ListRCEntryView.as_view(), name="product_home_page"),

]
