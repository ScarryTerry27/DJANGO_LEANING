from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from.utils import *


class WomenHome(DataMixin, ListView):
    # формируем класс для представления главной страницы
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *args, object_list=None, **kwargs):
        # здесь формируем что передаем в шаблон
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items())+list(c_def.items()))

    def get_queryset(self):
        # выбираем что отображать на странице
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


# @login_required  только зарег пользователей
def about(request):
    cats = Category.objects.annotate(Count('women'))
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': DataMixin.menu, 'cats': cats, \
                                                'cat_selected': -1})


def pageNotFound(request, exception):
    # HttpRequest
    return HttpResponseNotFound(f"<h1 style='color:blue;'>Страница не найдена</h1>")


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')  # перенапр.для незарег пользователей
    # raise_exception = True  ошибка 403 для незарег пользователей

    def get_context_data(self, *args, object_list=None, **kwargs):
        # здесь формируем что передаем в шаблон
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи', cat_selected=-1)
        return dict(list(context.items()) + list(c_def.items()))

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


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *args, object_list=None, **kwargs):
        # здесь формируем что передаем в шаблон
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

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


class WomenCategory(DataMixin, ListView):
    # класс для отображения статей по категориям
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *args, object_list=None, **kwargs):
        # здесь формируем что передаем в шаблон
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f"Категория {context['posts'][0].cat}", \
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


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
