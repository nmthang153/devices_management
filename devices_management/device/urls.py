from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('listdevices/', views.listdevices, name='listdevices'),
    path('add/', views.add, name='add'),
    path('bookAdmin/<int:id>', views.bookAdmin, name='bookAdmin'),
    path('book/<int:id>', views.book, name='book'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('search/', views.search, name='search'),
    path('orderlists/', views.orderlists, name='order'),
    path('mydevices/', views.mydevices, name='mydevices'),
    path('myorders/', views.myorders, name='myorders'),
    path('addsup/', views.addsup, name='addsup'),
    path('supplistadmin/', views.supplistadmin, name='supplistadmin'),
    path('mysupps/', views.mysupps, name='mysupps'),
    path('addprj/', views.addprj, name='addprj'),

]
