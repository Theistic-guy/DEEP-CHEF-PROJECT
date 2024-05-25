from django.urls import path
from . import views
from django.conf.urls.static import static 
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns=[
    path('',views.home,name="home_page"),
    #path('home/',views.home_page,name="redirected"),
    #path('home',views.home,name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()