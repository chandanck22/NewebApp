from django.urls import path
from . import views

app_name = 'blogApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.articles, name='articles'),
    # path('article/', views.article, name='article'),
    path('<slug:article>/', views.article, name='article'),


]