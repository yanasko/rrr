from django.apps import AppConfig


class SignConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sign'


#class NewsConfig(AppConfig):
    #name = 'news'

    # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    #def ready(self):
        #import news.signals
