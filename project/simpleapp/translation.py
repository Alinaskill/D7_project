from .models import New
from modeltranslation.translator import register, TranslationOptions  # импортируем декоратор для перевода и класс настроек, от которого будем наследоваться


# регистрируем наши модели для перевода

@register(New)
class NewTranslationOptions(TranslationOptions):
    fields = ('name', 'description')  # указываем, какие именно поля надо переводить в виде кортежа

