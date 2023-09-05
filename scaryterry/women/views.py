from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from women.models import Women, Category

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'addpage'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'}
]


def index(request):
    posts = Women.objects.all()
    cats = Category.objects.all()

    context = {
        'title': "Главная страница",
        'cats': cats,
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})


def pageNotFound(request, exception):
    # HttpRequest
    return HttpResponseNotFound(f"<h1 style='color:blue;'>Страница не найдена</h1>")


def addpage(request):
    return HttpResponse('Добавить статью')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    cats = Category.objects.all()
    context = {
        'post': post,
        'menu': menu,
        'cats': cats,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'women/post.html', context=context)


def show_category(request, cat_slug):
    cat = get_object_or_404(Category, slug=cat_slug)
    posts = Women.objects.filter(cat_id=cat.pk)
    context = {
        'title': "Главная страница",
        'menu': menu,
        'cats': Category.objects.all(),
        'cat_selected': cat.pk,
        'posts': posts,
    }
    return render(request, 'women/index.html', context=context)
