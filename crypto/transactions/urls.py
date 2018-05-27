from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from transactions import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/balance$', views.get_balance),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^transactions/$', views.TransactionList.as_view()),
    url(r'^transactions/(?P<pk>[0-9]+)/$', views.TransactionDetail.as_view()),
    url(r'^make-transaction/$', views.make_transaction),
]

urlpatterns = format_suffix_patterns(urlpatterns)