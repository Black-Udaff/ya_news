from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

# Импортируем из файла с формами список стоп-слов и предупреждение формы.
# Загляните в news/forms.py, разберитесь с их назначением.
from news.forms import BAD_WORDS, WARNING
from news.models import Comment, News

User = get_user_model()


class TestCommentCreation(TestCase):
    # Текст комментария понадобится в нескольких местах кода, 
    # поэтому запишем его в атрибуты класса.
    COMMENT_TEXT = 'Текст комментария'

    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(title='Заголовок', text='Текст')
        # Адрес страницы с новостью.
        cls.url = reverse('news:detail', args=(cls.news.id,))
        # Создаём пользователя и клиент, логинимся в клиенте.
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        # Данные для POST-запроса при создании комментария.
        cls.form_data = {'text': cls.COMMENT_TEXT} 


    def test_anonymous_user_cant_create_comment(self):
        # Совершаем запрос от анонимного клиента, в POST-запросе отправляем
        # предварительно подготовленные данные формы с текстом комментария.     
        self.client.post(self.url, data=self.form_data)
        # Считаем количество комментариев.
        comments_count = Comment.objects.count()
        # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
        self.assertEqual(comments_count, 0) 
    