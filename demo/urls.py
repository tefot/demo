from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from demo.comments import views

router = routers.DefaultRouter()
router.register(r'comments', views.CommentViewSet, 'comments')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^settings/', include('dbsettings.urls')),
]
