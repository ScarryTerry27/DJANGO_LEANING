from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from .models import *

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'addpage'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'}
]


class WomenHome(ListView):
    '''формируем класс для представления главной страницы'''
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *args, object_list=None, **kwargs):
        '''здесь формируем что передаем в шаблон'''
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['cat_selected'] = 0
        context['cats'] = Category.objects.all()
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        '''выбираем что отображать на странице'''
        return Women.objects.filter(is_published=True)

# # def index(request):
# '''функциональное представление класса WomenHome'''
# #     posts = Women.objects.all()
# #     cats = Category.objects.all()
# #
# #     context = {
# #         'title': "Главная страница",
# #         'cats': cats,
# #         'menu': menu,
# #         'posts': posts,
# #         'cat_selected': 0,
# #     }
# #     return render(request, 'women/index.html', context=context)


def about(request):
    cats = Category.objects.all()
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'cats': cats})


def pageNotFound(request, exception):
    # HttpRequest
    return HttpResponseNotFound(f"<h1 style='color:blue;'>Страница не найдена</h1>")


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, object_list=None, **kwargs):
        '''здесь формируем что передаем в шаблон'''
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['cat_selected'] = -1
        context['cats'] = Category.objects.all()
        context['title'] = 'Создать статью'
        return context

# def addpage(request):
#     cats = Category.objects.all()
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     context = {
#         'menu': menu,
#         'title': 'Создать статью',
#         'form': form,
#         'cats': cats,
#     }
#     return render(request, 'women/addpage.html', context=context)


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *args, object_list=None, **kwargs):
        '''здесь формируем что передаем в шаблон'''
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['post']
        context['cat_selected'] = context['object'].cat_id
        context['cats'] = Category.objects.all()
        return context

# def show_post(request, post_slug):
#     '''функциональное представление ShowPost'''
#     post = get_object_or_404(Women, slug=post_slug)
#     cats = Category.objects.all()
#     context = {
#         'post': post,
#         'menu': menu,
#         'cats': cats,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


class WomenCategory(WomenHome):
    '''класс для отображения статей по категориям'''
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *args, object_list=None, **kwargs):
        '''здесь формируем что передаем в шаблон'''
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = context['posts'][0].cat_id
        context['title'] = f"Категория {context['posts'][0].cat}"
        return context


# def show_category(request, cat_slug):
#     '''Функциональное представление класса WomenCategory'''
#     cat = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.objects.filter(cat_id=cat.pk)
#     context = {
#         'title': "Главная страница",
#         'menu': menu,
#         'cats': Category.objects.all(),
#         'cat_selected': cat.pk,
#         'posts': posts,
#     }
#     return render(request, 'women/index.html', context=context)
