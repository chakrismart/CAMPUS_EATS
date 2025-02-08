from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.auth,name='auth'),
    path('home/',views.home,name='home'),
    path('category/<str:foo>/',views.category,name='category'),
    path('logout',views.logout_,name='logout'),
    path('search',views.search,name='search'),
]
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)