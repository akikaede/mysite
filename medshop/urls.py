from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^pay$', views.index, name='index'),
    url(r'^proxy_pay_result$', views.proxy_pay_result, name='proxy_pay_result'),
    url(r'^proxy_pay_callback$', views.proxy_pay_callback, name='proxy_pay_callback'),
#     url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
#     url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
#     url(r'^genres/$', views.show_genres),
]
