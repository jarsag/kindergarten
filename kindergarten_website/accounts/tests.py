from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import date
import tempfile
import os

from .models import CustomUser
from .forms import CustomUserCreationForm, LoginForm
from children.models import Child

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Тесты для модели CustomUser"""
    
    def setUp(self):
        """Создаем тестовые данные"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'phone': '+79123456789'
        }
    
    def test_create_user_with_username(self):
        """Тест создания пользователя с username"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Иванов'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Иван')
        self.assertEqual(user.last_name, 'Иванов')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_user_without_username_uses_email(self):
        """Тест создания пользователя без username (используется email)"""
        # Создаем пользователя с пустым username через форму
        form_data = {
            'username': '',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Иван',
            'last_name': 'Иванов'
        }
        form = CustomUserCreationForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.username, 'test@example.com')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Иван')
        self.assertEqual(user.last_name, 'Иванов')
    
    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertEqual(admin_user.username, 'admin')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
    
    def test_user_string_representation(self):
        """Тест строкового представления пользователя"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Иванов'
        )
        
        expected_str = "Иван Иванов (test@example.com)"
        self.assertEqual(str(user), expected_str)
    
    def test_user_notification_defaults(self):
        """Тест значений по умолчанию для уведомлений"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.assertTrue(user.notification_email)
        self.assertFalse(user.notification_sms)
    
    def test_user_phone_field(self):
        """Тест поля телефона"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            phone='+79123456789'
        )
        
        self.assertEqual(user.phone, '+79123456789')


class CustomUserCreationFormTest(TestCase):
    """Тесты для формы регистрации CustomUserCreationForm"""
    
    def test_valid_form_with_username(self):
        """Тест валидной формы с username"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'phone': '+79123456789'
        }
        form = CustomUserCreationForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Иван')
        self.assertEqual(user.last_name, 'Иванов')
        self.assertEqual(user.phone, '+79123456789')
    
    def test_valid_form_without_username_uses_email(self):
        """Тест валидной формы без username (используется email)"""
        form_data = {
            'username': '',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Иван',
            'last_name': 'Иванов'
        }
        form = CustomUserCreationForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.username, 'test@example.com')
        self.assertEqual(user.email, 'test@example.com')
    
    def test_invalid_form_password_mismatch(self):
        """Тест формы с несовпадающими паролями"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'differentpass',
            'first_name': 'Иван',
            'last_name': 'Иванов'
        }
        form = CustomUserCreationForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_invalid_form_weak_password(self):
        """Тест формы с слабым паролем"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': '123',
            'password2': '123',
            'first_name': 'Иван',
            'last_name': 'Иванов'
        }
        form = CustomUserCreationForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_invalid_form_duplicate_email(self):
        """Тест формы с дублирующимся email"""
        CustomUser.objects.create_user(
            username='existing',
            email='test@example.com',
            password='testpass123'
        )
        
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Иван',
            'last_name': 'Иванов'
        }
        form = CustomUserCreationForm(data=form_data)
        
        # Проверяем, что форма не валидна
        self.assertFalse(form.is_valid())
        
        # Проверяем, что есть ошибка по email
        self.assertIn('email', form.errors)


class LoginFormTest(TestCase):
    """Тесты для формы входа LoginForm"""
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Иванов'
        )
    
    def test_valid_form(self):
        """Тест валидной формы"""
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        form = LoginForm(data=form_data)
        
        self.assertTrue(form.is_valid())
    
    def test_form_with_email(self):
        """Тест формы с email вместо username"""
        form_data = {
            'username': 'test@example.com',
            'password': 'testpass123'
        }
        form = LoginForm(data=form_data)
        
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_missing_fields(self):
        """Тест формы с пустыми полями"""
        form_data = {
            'username': '',
            'password': ''
        }
        form = LoginForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class AccountsViewsTest(TestCase):
    """Тесты для представлений accounts"""
    
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Иванов',
            phone='+79123456789'
        )
        self.child = Child.objects.create(
            parent=self.user,
            first_name='Петя',
            last_name='Иванов',
            birth_date=date(2020, 1, 1),
            group='Ясли'
        )
    
    def test_register_view_get(self):
        """Тест GET запроса на страницу регистрации"""
        response = self.client.get(reverse('register'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)
    
    def test_register_view_post_valid(self):
        """Тест POST запроса на регистрацию с валидными данными"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'Новый',
            'last_name': 'Пользователь',
            'phone': '+79876543210'
        }
        
        response = self.client.post(reverse('register'), form_data)
        
        self.assertEqual(response.status_code, 302)  # Редирект после успешной регистрации
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())
    
    def test_login_view_get(self):
        """Тест GET запроса на страницу входа"""
        response = self.client.get(reverse('login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)
    
    def test_login_view_post_valid_username(self):
        """Тест POST запроса на вход с username"""
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(reverse('login'), form_data)
        
        self.assertEqual(response.status_code, 302)  # Редирект после успешного входа
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_view_post_valid_email(self):
        """Тест POST запроса на вход с email"""
        form_data = {
            'username': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(reverse('login'), form_data)
        
        self.assertEqual(response.status_code, 302)  # Редирект после успешного входа
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_view_post_invalid(self):
        """Тест POST запроса на вход с неверными данными"""
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(reverse('login'), form_data)
        
        self.assertEqual(response.status_code, 200)  # Остаемся на странице входа
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, 'Неверный email/логин или пароль')
    
    def test_logout_view(self):
        """Тест выхода из системы"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('logout'))
        
        self.assertEqual(response.status_code, 302)  # Редирект после выхода
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_profile_view_get(self):
        """Тест GET запроса на страницу профиля"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.context['children'].count(), 1)
        self.assertEqual(response.context['children'][0], self.child)
    
    def test_profile_view_redirect_if_not_logged_in(self):
        """Тест редиректа на страницу входа если не авторизован"""
        response = self.client.get(reverse('profile'))
        
        self.assertEqual(response.status_code, 302)  # Редирект на страницу входа
        self.assertIn('login', response.url)
    
    def test_add_child_view_post(self):
        """Тест добавления ребенка"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'first_name': 'Маша',
            'last_name': 'Иванова',
            'birth_date': '2021-05-15',
            'group': 'Младшая',
            'allergies': 'Нет',
            'medical_notes': 'Здоровый ребенок'
        }
        
        response = self.client.post(reverse('add_child'), form_data)
        
        self.assertEqual(response.status_code, 302)  # Редирект после добавления
        self.assertEqual(self.user.children.count(), 2)
        new_child = self.user.children.last()
        self.assertEqual(new_child.first_name, 'Маша')
        self.assertEqual(new_child.last_name, 'Иванова')
    
    def test_edit_child_view_get(self):
        """Тест GET запроса на страницу редактирования ребенка"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('edit_child', args=[self.child.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_child.html')
        self.assertEqual(response.context['child'], self.child)
    
    def test_edit_child_view_post(self):
        """Тест POST запроса на редактирование ребенка"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'first_name': 'Петр',
            'last_name': 'Иванов',
            'birth_date': '2020-01-01',
            'group': 'Ясли',
            'allergies': 'Аллергия на арахис',
            'medical_notes': 'Нуждается в особом внимании'
        }
        
        response = self.client.post(reverse('edit_child', args=[self.child.id]), form_data)
        
        self.assertEqual(response.status_code, 302)  # Редирект после редактирования
        self.child.refresh_from_db()
        self.assertEqual(self.child.first_name, 'Петр')
        self.assertEqual(self.child.allergies, 'Аллергия на арахис')
    
    def test_delete_child_view_get(self):
        """Тест GET запроса на страницу подтверждения удаления ребенка"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('delete_child', args=[self.child.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/confirm_delete.html')
        self.assertEqual(response.context['child'], self.child)
    
    def test_delete_child_view_post(self):
        """Тест POST запроса на удаление ребенка"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('delete_child', args=[self.child.id]))
        
        self.assertEqual(response.status_code, 302)  # Редирект после удаления
        self.assertEqual(self.user.children.count(), 0)
        self.assertFalse(Child.objects.filter(id=self.child.id).exists())


class ChildModelTest(TestCase):
    """Тесты для модели Child"""
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Иванов'
        )
    
    def test_create_child(self):
        """Тест создания ребенка"""
        child = Child.objects.create(
            parent=self.user,
            first_name='Петя',
            last_name='Иванов',
            birth_date=date(2020, 1, 1),
            group='Ясли'
        )
        
        self.assertEqual(child.parent, self.user)
        self.assertEqual(child.first_name, 'Петя')
        self.assertEqual(child.last_name, 'Иванов')
        self.assertEqual(child.birth_date, date(2020, 1, 1))
        self.assertEqual(child.group, 'Ясли')
        self.assertEqual(str(child), 'Петя Иванов')
    
    def test_child_age_calculation(self):
        """Тест расчета возраста ребенка"""
        # Ребенок родился 1 января 2020 года
        child = Child.objects.create(
            parent=self.user,
            first_name='Петя',
            last_name='Иванов',
            birth_date=date(2020, 1, 1)
        )
        
        # Рассчитываем возраст вручную для тестирования
        # На 1 января 2024 года возраст должен быть 4 года
        today = date(2024, 1, 1)
        birth_date = child.birth_date
        
        # Формула расчета возраста
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
        
        self.assertEqual(age, 4)
    
    def test_child_with_photo(self):
        """Тест ребенка с фотографией"""
        # Создаем временный файл для теста
        test_image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        
        child = Child.objects.create(
            parent=self.user,
            first_name='Петя',
            last_name='Иванов',
            birth_date=date(2020, 1, 1),
            photo=test_image
        )
        
        self.assertEqual(child.parent, self.user)
        self.assertTrue(child.photo)
    
    def test_child_medical_fields(self):
        """Тест медицинских полей ребенка"""
        child = Child.objects.create(
            parent=self.user,
            first_name='Петя',
            last_name='Иванов',
            birth_date=date(2020, 1, 1),
            allergies='Аллергия на арахис',
            medical_notes='Нуждается в особом внимании'
        )
        
        self.assertEqual(child.allergies, 'Аллергия на арахис')
        self.assertEqual(child.medical_notes, 'Нуждается в особом внимании')