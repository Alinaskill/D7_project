from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from django.contrib.auth.mixins import PermissionRequiredMixin

from .filters import NewFilter
from .forms import NewForm
from .models import New

from .models import Category
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import AnonymousUser

from django.utils.translation import gettext as _ # импортируем функцию для перевода

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from simpleapp.serializers import *
from simpleapp.models import *



class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = New
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context



class NewDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = New
    # Используем другой шаблон — post.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        category = self.get_object().category
        if not isinstance(self.request.user, AnonymousUser):
            context['is_subscriber'] = self.request.user.category_set.filter(pk=category.pk).exists()
        return context

#подписка на группу

@login_required
def add_subscribe(request, **kwargs):
    category_number = int(kwargs['pk'])
    Category.objects.get(pk=category_number).subscribers.add(request.user)
    return redirect('/news/')

#отписка на группу
@login_required
def delete_subscribe(request, **kwargs):
    category_number = int(kwargs['pk'])
    Category.objects.get(pk=category_number).subscribers.remove(request.user)
    return redirect('/news/')


# Добавляем новое представление для создания новостей.
class NewCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = NewForm
    # модель товаров
    model = New
    # и новый шаблон, в котором используется форма.
    template_name = 'new_edit.html'


class NewUpdate(UpdateView):
    form_class = NewForm
    model = New
    template_name = 'new_edit.html'

class NewDelete(DeleteView):
    model = New
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')

#Предоставление прав

class MyCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_new')

class MyUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_new')

class NewViewset(viewsets.ModelViewSet):
   queryset = New.objects.all()
   serializer_class = NewSerializer


class CategoryViewset(viewsets.ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer




