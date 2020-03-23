from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('addUser/', views.add_user_view, name='addUser'),
    url(r'^portafolioFiltroPublico/$', views.portafolioFiltroPublico, name='portafolioFiltroPublico'),
    path('login/', views.login_view),
    path('editImages/', views.edit_images_view),
]
