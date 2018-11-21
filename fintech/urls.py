from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'accounts/(?P<pk>.+)/balance', views.GetAccountBalance.as_view())
]
