from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
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
        wom_filter = cache.get('wom_filter')
        if not wom_filter:
            wom_filter = Women.objects.filter(is_published=True).select_related('cat')
            cache.set('wom_filter', wom_filter, 60)
        return wom_filter

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
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # пагинация внутри функции представления
    cats_count = cache.get('cats_count')
    if not cats_count:
        cats_count = Category.objects.annotate(Count('women'))
        cats_count = cache.set('cats_count', cats_count, 60)
    return render(request, 'women/about.html', {'page_obj': page_obj, 'title': 'О сайте', 'menu': DataMixin.menu, 'cats': cats_count, \
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


# def login(request):
#     return HttpResponse('Авторизация')


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
        wom_fil = cache.get('wom_fil')
        if not wom_fil:
            wom_fil = Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
            cache.set('wom_fil', wom_fil, 60)
        return wom_fil

    def get_context_data(self, *args, object_list=None, **kwargs):
        # здесь формируем что передаем в шаблон
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title=f"Категория {c.name}", cat_selected=c.pk)
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

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

