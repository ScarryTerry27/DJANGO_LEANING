from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('addpage/', views.addpage, name='addpage'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', views.show_category, name='category')
]
