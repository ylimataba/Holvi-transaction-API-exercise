from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'transactions', views.TransactionViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'accounts/(?P<pk>.+)/balance', views.GetAccountBalance.as_view())
]
