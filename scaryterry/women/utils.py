from django.db.models import Count

from .models import *


class DataMixin:
    paginate_by = 3
    menu = [
        {'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'addpage'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
    ]

    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = self.menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = Category.objects.annotate(Count('women'))
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context