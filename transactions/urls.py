from django.urls import re_path

from .views import category_view

urlpatterns = [
    # re_path(r'^$', home_view, name='home'),
    re_path(r'^logs/$', category_view, name='logs'),
    # re_path(r'^check/$', withdrawal_view, name='withdrawal'),
]

app_name = 'transactions'
