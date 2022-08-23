from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from NurseryApp.models import Pet, UserProfile


class RegisterPageTest(TestCase):

    def test_register_page(self):
        """Тест что используется нужный шаблон, код ответа 200"""
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'NurseryApp/register.html')


class AllPetsPageView(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='testuser1', password='12345')
        test_user.save()
        test_user_profile = UserProfile.objects.create(user=test_user, shelter='Приют1', address='Некий адрес')
        test_user_profile.save()
        pet1 = Pet.objects.create(nickname='John', age='12', weight='22', growth='35', shelter=test_user)
        pet1.save()

    def test_logged_in_uses_correct_template(self):
        """Тест на залогиненного пользователя, используется нужный шаблон, количество записей отображается верно"""
        self.client.login(username='testuser1', password='12345')
        url = reverse('all_pets')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'NurseryApp/pets.html')
        self.assertTrue(len(response.context['pets']) == 1)


class AddPetPage(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='testuser1', password='12345')
        test_user.save()
        test_user_profile = UserProfile.objects.create(user=test_user, shelter='Приют1', address='Некий адрес')
        test_user_profile.save()

    def test_add_pet(self):
        """Тест что создание питомца проходит успешно и сохраняется в БД"""
        self.client.login(username='testuser1', password='12345')
        url = reverse('add_pet')
        self.client.post(url, {'nickname': 'John',
                               'age': '12',
                               'weight': '22',
                               'growth': '35',
                               })
        response = self.client.get('/pets')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['pets']) == 1)


class EditPetPage(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='testuser1', password='12345')
        test_user.save()
        test_user_profile = UserProfile.objects.create(user=test_user, shelter='Приют1', address='Некий адрес')
        test_user_profile.save()
        pet1 = Pet.objects.create(nickname='John', age='12', weight='22', growth='35', shelter=test_user)
        pet1.save()

    def test_edit_pet(self):
        """Тест что изменение питомца проходит успешно и сохраняется в бд"""
        self.client.login(username='testuser1', password='12345')
        pet = Pet.objects.get(id=1)
        url = reverse('edit_pet', args=[pet.id])
        self.client.post(url, {'nickname': 'Barsik',
                               'age': '12',
                               'weight': '22',
                               'growth': '35',
                               })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        pet_edited = Pet.objects.get(id=1)
        self.assertTrue(pet_edited.nickname == 'Barsik')


class DeletePage(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='testuser1', password='12345')
        test_user.save()
        test_user_profile = UserProfile.objects.create(user=test_user, shelter='Приют1', address='Некий адрес')
        test_user_profile.save()
        pet1 = Pet.objects.create(nickname='John', age='12', weight='22', growth='35', shelter=test_user)
        pet1.save()

    def test_delete_pag_not_login(self):
        """Тест что удаление питомца не залогиненым(другим) пользователем невозможно"""
        response = self.client.get('/pets')
        self.assertTrue(len(response.context['pets']) == 1)
        pet = Pet.objects.get(id=1)
        url = reverse('delete', args=[pet.id])
        self.client.get(url)
        response = self.client.get('/pets')
        self.assertTrue(len(response.context['pets']) == 1)

    def test_delete_pag_loggedin(self):
        """Тест что удаление питомца успешно"""
        self.client.login(username='testuser1', password='12345')
        response = self.client.get('/pets')
        self.assertTrue(len(response.context['pets']) == 1)
        pet = Pet.objects.get(id=1)
        url = reverse('delete', args=[pet.id])
        self.client.get(url)
        response = self.client.get('/pets')
        self.assertTrue(len(response.context['pets']) == 0)
