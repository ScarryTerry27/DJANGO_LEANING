from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *

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
    cats = Category.objects.all()
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'cats': cats})


def pageNotFound(request, exception):
    # HttpRequest
    return HttpResponseNotFound(f"<h1 style='color:blue;'>Страница не найдена</h1>")


def addpage(request):
    cats = Category.objects.all()
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            try:
                Women.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()

    context = {
        'menu': menu,
        'title': 'Создать статью',
        'form': form,
        'cats': cats,
    }
    return render(request, 'women/addpage.html', context=context)


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
