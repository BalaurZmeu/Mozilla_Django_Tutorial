from catalog.models import Author
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorCreateViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            username='test_user',
            password='some_password',
        )
        
        test_user_no_perm = User.objects.create_user(
            username='no_perm',
            password='the_password',
        )
        
        content_typeAuthor = ContentType.objects.get_for_model(Author)
        permAddAuthor = Permission.objects.get(
            codename="add_author",
            content_type=content_typeAuthor,
        )
        
        test_user.user_permissions.add(permAddAuthor)
        test_user.save()
        test_user_no_perm.save()
        
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author-create'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/author/create/')
        
    def test_no_permission_user_403_forbidden(self):
        login = self.client.login(username='no_perm', password='the_password')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 403)
        
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='test_user', password='some_password')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(str(response.context['user']), 'test_user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_form.html')
        
