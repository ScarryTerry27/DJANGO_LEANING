from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category')
]
