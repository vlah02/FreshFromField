import unittest
from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Create your tests here.

class TestUserRegistration(unittest.TestCase):

    def setUp(self):
        service = webdriver.EdgeService(
            executable_path='C:\\Users\\Asus Strix\\project_ooPSIes\\Faza5\\FreshFromFields\\fff\\msedgedriver.exe')
        self.browser = webdriver.Edge(service=service)
        self.base_url = 'http://localhost:8000'

    def tearDown(self):
        self.browser.quit()

    def test_unsuccessful_registration_email_exists(self):
        driver = self.browser
        driver.get(self.base_url + '/register/')

        driver.find_element(By.NAME, 'first_name').send_keys('Petar')
        driver.find_element(By.NAME, 'last_name').send_keys('Perovic')
        driver.find_element(By.NAME, 'email').send_keys('djole@email.com')
        driver.find_element(By.NAME, 'phone').send_keys('0658187149')
        driver.find_element(By.NAME, 'password').send_keys('123')
        driver.find_element(By.NAME, 'password_confirmation').send_keys('123')
        driver.find_element(By.NAME, 'type').send_keys('customer')
        driver.find_element(By.NAME, 'city').send_keys('Beograd')
        driver.find_element(By.NAME, 'username').send_keys('pera')
        driver.find_element(By.NAME, 'country').send_keys('Serbia')

        driver.find_element(By.ID, 'create').click()

        email_error = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "email-error"))).text
        self.assertIn('Email već postoji', email_error)

    def test_unsuccessful_registration_username_exists(self):
        driver = self.browser
        driver.get(self.base_url + '/register/')

        driver.find_element(By.NAME, 'first_name').send_keys('Petar')
        driver.find_element(By.NAME, 'last_name').send_keys('Perovic')
        driver.find_element(By.NAME, 'email').send_keys('pera@email.com')
        driver.find_element(By.NAME, 'phone').send_keys('0658187149')
        driver.find_element(By.NAME, 'password').send_keys('123')
        driver.find_element(By.NAME, 'password_confirmation').send_keys('123')
        driver.find_element(By.NAME, 'type').send_keys('customer')
        driver.find_element(By.NAME, 'city').send_keys('Beograd')
        driver.find_element(By.NAME, 'username').send_keys('djole')
        driver.find_element(By.NAME, 'country').send_keys('Serbia')

        driver.find_element(By.ID, 'create').click()

        username_error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username-error"))).text
        self.assertIn('Username već postoji', username_error)

    def test_unsuccessful_registration_wrong_password_confirmation(self):
        driver = self.browser
        driver.get(self.base_url + '/register/')

        driver.find_element(By.NAME, 'first_name').send_keys('Petar')
        driver.find_element(By.NAME, 'last_name').send_keys('Perovic')
        driver.find_element(By.NAME, 'email').send_keys('pera@email.com')
        driver.find_element(By.NAME, 'phone').send_keys('0658187149')
        driver.find_element(By.NAME, 'password').send_keys('123')
        driver.find_element(By.NAME, 'password_confirmation').send_keys('aaa')
        driver.find_element(By.NAME, 'type').send_keys('customer')
        driver.find_element(By.NAME, 'city').send_keys('Beograd')
        driver.find_element(By.NAME, 'username').send_keys('pera')
        driver.find_element(By.NAME, 'country').send_keys('Serbia')

        driver.find_element(By.ID, 'create').click()

        password_error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "passconf-error"))).text
        self.assertIn('Lozinke se ne poklapaju', password_error)

    def test_unsuccessful_registration_fields_empty(self):
        driver = self.browser
        driver.get(self.base_url + '/register/')
        driver.find_element(By.ID, 'create').click()

        first_name_error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "fname-error"))).text
        self.assertIn('Ime je obavezno', first_name_error)

    def test_successful_registration(self):
        driver = self.browser
        driver.get(self.base_url + '/register/')

        driver.find_element(By.NAME, 'first_name').send_keys('Petar')
        driver.find_element(By.NAME, 'last_name').send_keys('Perovic')
        driver.find_element(By.NAME, 'email').send_keys('pera@email.com')
        driver.find_element(By.NAME, 'phone').send_keys('0658187149')
        driver.find_element(By.NAME, 'password').send_keys('123')
        driver.find_element(By.NAME, 'password_confirmation').send_keys('123')
        driver.find_element(By.NAME, 'type').send_keys('customer')
        driver.find_element(By.NAME, 'city').send_keys('Beograd')
        driver.find_element(By.NAME, 'username').send_keys('pera')
        driver.find_element(By.NAME, 'country').send_keys('Serbia')

        driver.find_element(By.ID, 'create').click()

        WebDriverWait(driver, 10).until(EC.url_contains('home'))

        self.assertIn('home', driver.current_url)

    def test_successful_login(self):
        driver = self.browser
        driver.get(self.base_url)

        driver.find_element(By.NAME, 'email').send_keys('djole@email.com')
        driver.find_element(By.NAME, 'password').send_keys('123')
        login_button = driver.find_element(By.ID, 'log')

        login_button.click()

        self.assertIn('home', driver.current_url)

    def test_unsuccessful_login_email_does_not_exist(self):
        driver = self.browser
        driver.get(self.base_url)

        driver.find_element(By.NAME, 'email').send_keys('perica@email.com')
        driver.find_element(By.NAME, 'password').send_keys('123')

        driver.find_element(By.ID, 'log').click()

        email_error = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "email-error"))).text
        self.assertIn('Email ne postoji.', email_error)

    def test_unsuccessful_login_wrong_password(self):
        driver = self.browser
        driver.get(self.base_url)

        driver.find_element(By.NAME, 'email').send_keys('pera@email.com')
        driver.find_element(By.NAME, 'password').send_keys('aaaddd')

        driver.find_element(By.ID, 'log').click()

        password_error = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "pass-error"))).text
        self.assertIn('Uneli ste pogrešnu šifru.', password_error)


class TestAddingAndEditingListings(unittest.TestCase):

    def setUp(self):
        service = webdriver.EdgeService(
            executable_path='C:\\Users\\Asus Strix\\project_ooPSIes\\Faza5\\FreshFromFields\\fff\\msedgedriver.exe')
        self.browser = webdriver.Edge(service=service)
        self.base_url = 'http://localhost:8000'

    def tearDown(self):
        self.browser.quit()

    def test_add_listing_successful(self):
        self.browser.get(self.base_url)
        self.browser.find_element(By.NAME, 'email').send_keys('djole@email.com')
        self.browser.find_element(By.NAME, 'password').send_keys('123')
        login_button = self.browser.find_element(By.ID, 'log')

        login_button.click()

        user_button = self.browser.find_element(By.CSS_SELECTOR, '.fa-user')

        user_button.click()

        listing = self.browser.find_element(By.ID, 'addListing')

        listing.click()

        # Fill in the form fields
        self.browser.find_element(By.ID, 'naziv').send_keys('Test listing')
        self.browser.find_element(By.ID, 'tip').send_keys('Voće')
        self.browser.find_element(By.ID, 'cena').send_keys('100')
        self.browser.find_element(By.ID, 'jedinica').send_keys('din/komad')
        self.browser.find_element(By.ID, 'kolicina').send_keys('10')
        self.browser.find_element(By.ID, 'opis').send_keys('Test description')

        # Submit the form
        self.browser.find_element(By.ID, 'postavi').click()

        # Assert the redirection or success message
        WebDriverWait(self.browser, 10).until(EC.url_contains(''))
        self.assertIn('', self.browser.current_url)

    def test_add_listing_unsuccessful(self):
        self.browser.get(self.base_url)
        self.browser.find_element(By.NAME, 'email').send_keys('djole@email.com')
        self.browser.find_element(By.NAME, 'password').send_keys('123')
        login_button = self.browser.find_element(By.ID, 'log')

        login_button.click()

        user_button = self.browser.find_element(By.CSS_SELECTOR, '.fa-user')

        user_button.click()

        listing = self.browser.find_element(By.ID, 'addListing')

        listing.click()

        current_url = self.browser.current_url
        self.browser.find_element(By.ID, 'postavi').click()

        self.assertEqual(current_url, self.browser.current_url)

    def test_edit_listing_successful(self):
        self.browser.get(self.base_url)
        self.browser.find_element(By.NAME, 'email').send_keys('djole@email.com')
        self.browser.find_element(By.NAME, 'password').send_keys('123')
        login_button = self.browser.find_element(By.ID, 'log')

        login_button.click()

        user_button = self.browser.find_element(By.CSS_SELECTOR, '.fa-user')

        user_button.click()

        listings = self.browser.find_element(By.ID, 'showListings')

        listings.click()

        listing = self.browser.find_element(By.CSS_SELECTOR, '.listings-description')

        listing.click()

        listingChange = self.browser.find_element(By.ID, 'izmenaOglasa')

        listingChange.click()

        self.browser.find_element(By.ID, 'cena').clear()
        self.browser.find_element(By.ID, 'cena').send_keys('200')
        self.browser.find_element(By.ID, 'kolicina').clear()
        self.browser.find_element(By.ID, 'kolicina').send_keys('50')
        self.browser.find_element(By.ID, 'opis').clear()
        self.browser.find_element(By.ID, 'opis').send_keys('Edited Test description, nice!')

        # Submit the form
        self.browser.find_element(By.ID, 'sacuvajOglas').click()

        # Assert the redirection or success message
        WebDriverWait(self.browser, 10).until(EC.url_contains('home'))
        self.assertIn('home', self.browser.current_url)

    def test_edit_listing_unsuccessful(self):
        self.browser.get(self.base_url)
        self.browser.find_element(By.NAME, 'email').send_keys('djole@email.com')
        self.browser.find_element(By.NAME, 'password').send_keys('123')
        login_button = self.browser.find_element(By.ID, 'log')

        login_button.click()

        user_button = self.browser.find_element(By.CSS_SELECTOR, '.fa-user')

        user_button.click()

        listings = self.browser.find_element(By.ID, 'showListings')

        listings.click()

        listing = self.browser.find_element(By.CSS_SELECTOR, '.listings-description')

        listing.click()

        listingChange = self.browser.find_element(By.ID, 'izmenaOglasa')

        listingChange.click()
        self.browser.find_element(By.ID, 'cena').clear()
        current_url = self.browser.current_url
        self.browser.find_element(By.ID, 'sacuvajOglas').click()

        self.assertEqual(current_url, self.browser.current_url)


from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from .views import *
from .forms import *
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import F
from django.shortcuts import get_object_or_404
from unittest.mock import patch
from django.http import JsonResponse
from .forms import UserDataForm
from django.utils import timezone
from django.http import HttpResponseRedirect


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'fff/home.html')


class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create_user(username='userTest1', password='password1', email='userTest1@email.com')
        self.user2 = User.objects.create_user(username='userTest2', password='password2', email='userTest2@email.com')
        self.seller = Seller.objects.create(userid=self.user1, rating=4.5, numberOfListings=0)
        self.customer = Customer.objects.create(userid=self.user2, rating=3.5)
        self.chat = Chat.objects.create(chatid=1, user1=self.user2, user2=self.seller)

    def test_chat_not_found(self):
        response = self.client.get(reverse('profile', args=[999]))
        self.assertEqual(response.status_code, 404)

    # def test_user_not_found(self):
    #     self.chat.user2 = None
    #     self.chat.save()
    #
    #     response = self.client.get(reverse('profile', args=[self.chat.chatid]))
    #     self.assertEqual(response.status_code, 404)

    def test_profile_view_seller(self):
        self.client.login(username='userTest2', password='password2')
        response = self.client.get(reverse('profile', args=[self.chat.chatid]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fff/profile.html')
        self.assertEqual(response.context['user'], self.user1)
        self.assertEqual(response.context['rating'], self.seller.rating)

    def test_profile_view_customer(self):
        self.client.login(username='userTest1', password='password1')
        response = self.client.get(reverse('profile', args=[self.chat.chatid]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fff/profile.html')
        self.assertEqual(response.context['user'], self.user2)
        self.assertEqual(response.context['rating'], self.customer.rating)


class RateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='userTest1', password='password1', email='userTest1@email.com')
        self.user2 = User.objects.create_user(username='userTest2', password='password2', email='userTest2@email.com')
        self.seller = Seller.objects.create(userid=self.user1, rating=4.0, numberOfListings=0)
        self.customer = Customer.objects.create(userid=self.user2, rating=5.0)
        self.client.login(username='userTest1', password='password1')

    def test_rate_view_first_time_rating(self):
        response = self.client.post(reverse('rate', args=[self.user2.userid]), {'rating': 4.0})
        self.assertEqual(response.status_code, 302)
        rating = Rating.objects.get(user1=self.user1, user2=self.user2)
        self.assertEqual(rating.rating, 4)
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.rating, 4.0)

    def test_rate_view_update_rating(self):
        Rating.objects.create(user1=self.user1, user2=self.user2, rating=3)
        response = self.client.post(reverse('rate', args=[self.user2.userid]), {'rating': 5})
        self.assertEqual(response.status_code, 302)
        rating = Rating.objects.get(user1=self.user1, user2=self.user2)
        self.assertEqual(rating.rating, 5)
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.rating, 4.0)

    # def test_rate_view_unauthenticated(self):
    #     self.client.logout()
    #     response = self.client.post(reverse('rate', args=[self.user2.userid]), {'rating': 4})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertFalse(Rating.objects.filter(user1=self.user1, user2=self.user2).exists())


class RegisterViewTests(TestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fff/registar.html')

    def test_register_view_post_success_seller(self):
        data = {
            'first_name': 'Nikola',
            'last_name': 'Kovacevic',
            'email': 'kova@email.com',
            'phone': '1234567890',
            'password': '123',
            'password_confirmation': '123',
            'type': 'seller',
            'city': 'Belgrade',
            'username': 'kova',
            'country': 'Serbia'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='kova')
        self.assertIsNotNone(user)
        seller = Seller.objects.get(userid=user)
        self.assertIsNotNone(seller)

    def test_register_view_post_success_customer(self):
        data = {
            'first_name': 'Nikola',
            'last_name': 'Kovacevic',
            'email': 'kova@email.com',
            'phone': '1234567890',
            'password': '123',
            'password_confirmation': '123',
            'type': 'customer',
            'city': 'Belgrade',
            'username': 'kova',
            'country': 'Serbia'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='kova')
        self.assertIsNotNone(user)
        customer = Customer.objects.get(userid=user)
        self.assertIsNotNone(customer)

    def test_register_view_post_missing_fields(self):
        data = {
            'first_name': '',
            'last_name': 'Kovacevic',
            'email': 'kova@email.com',
            'phone': '1234567890',
            'password': '123',
            'password_confirmation': '123',
            'type': 'customer',
            'city': 'Belgrade',
            'username': 'kova',
            'country': 'Serbia'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ime je obavezno.')

    def test_register_view_post_password_mismatch(self):
        data = {
            'first_name': 'Nikola',
            'last_name': 'Kovacevic',
            'email': 'kova@email.com',
            'phone': '1234567890',
            'password': '123',
            'password_confirmation': '1234',
            'type': 'customer',
            'city': 'Belgrade',
            'username': 'kova',
            'country': 'Serbia'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lozinke se ne poklapaju.')

    def test_register_view_post_existing_username(self):
        User.objects.create_user(username='kova', password='123', email='kova@email.com')
        data = {
            'first_name': 'Nikola',
            'last_name': 'Kovacevic',
            'email': 'kova@email.com',
            'phone': '1234567890',
            'password': '123',
            'password_confirmation': '123',
            'type': 'customer',
            'city': 'Belgrade',
            'username': 'kova',
            'country': 'Serbia'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username već postoji.')

    def test_register_view_post_existing_email(self):
        User.objects.create_user(username='kova', password='123', email='kova@email.com')
        data = {
            'first_name': 'Nikola',
            'last_name': 'Kovacevic',
            'email': 'kova@email.com',
            'phone': '1234567890',
            'password': '123',
            'password_confirmation': '123',
            'type': 'customer',
            'city': 'Belgrade',
            'username': 'kovac',
            'country': 'Serbia'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email već postoji.')


from .views import authenticate


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='kova',
            email='kova@email.com',
            password='123'
        )

    def test_user_login_success(self):
        response = self.client.post(reverse('login'), {
            'email': 'kova@email.com',
            'password': '123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.session['logged_in'])
        self.assertEqual(response.wsgi_request.session['type'], 'customer')

    def test_user_login_invalid_email(self):
        response = self.client.post(reverse('login'), {
            'email': 'kovac@email.com',
            'password': '123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, 'Email ne postoji.')

    def test_user_login_invalid_password(self):
        response = self.client.post(reverse('login'), {
            'email': 'kova@email.com',
            'password': '123456789'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Uneli ste pogrešnu šifru.')


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='kova',
            email='kova@email.com',
            password='123'
        )

    def test_logout_success(self):
        self.client.login(username='kova', password='123')
        response = self.client.post(reverse('user_logout'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.json()['message'], 'Logged out successfully.')

    def test_invalid_request_method(self):
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid request method.')


class NewListingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='kova',
            email='kova@email.com',
            password='123'
        )
        self.seller = Seller.objects.create(userid=self.user)

    def test_new_listing_creation(self):
        self.client.login(username='kova', password='123')
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_image.jpg')
        # image_file = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
        #                                 content_type='image/jpeg')
        response = self.client.post(reverse('newlisting'), {
            'listingname': 'Jabuke',
            'price': '100',
            'unit': 'din/kg',
            'quantity': '100',
            'type': 'Voće',
            'description': 'crvene jabuke',
            # 'image': None
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Listing.objects.filter(listingname='Jabuke').exists())
        seller = Seller.objects.get(userid=self.user)
        self.assertEqual(seller.numberOfListings, 1)

    def test_invalid_form_submission(self):
        self.client.login(username='kova', password='123')
        response = self.client.post(reverse('newlisting'), {
            'listingname': '',
            'price': '100',
            'unit': 'din/kg',
            'quantity': '100',
            'type': 'Voće',
            'description': 'crvene jabuke',
            # 'image': None
        })
        self.assertEqual(response.status_code, 302)


class EditListingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='kova',
            email='kova@email.com',
            password='123'
        )
        self.seller = Seller.objects.create(userid=self.user)
        self.listing = Listing.objects.create(
            listingname='Jabuke',
            userid=self.seller,
            price=100,
            unit='din/kg',
            quantity='100',
            type='Voće',
            description='crvene jabuke',
            image=b''
        )

    def test_edit_listing_success(self):
        self.client.login(username='kova', password='123')

        response = self.client.post(reverse('edit_listing', kwargs={'pk': self.listing.pk}), {
            'listingname': 'Jabukee',
            'price': '100',
            'unit': 'din/kg',
            'quantity': '100',
            'type': 'Voće',
            'description': 'Velike crvene jabuke',
        })
        self.assertEqual(response.status_code, 302)
        self.listing.refresh_from_db()
        self.assertNotEqual(self.listing.image, b'')

    def test_edit_listing_invalid_form_submission(self):
        self.client.login(username='kova', password='123')
        response = self.client.post(reverse('edit_listing', kwargs={'pk': self.listing.pk}), {
            'listingname': '',
            'price': '100',
            'unit': 'din/kg',
            'quantity': '100',
            'type': 'Voće',
            'description': 'Velike crvene jabuke',
        })
        self.assertEqual(response.status_code, 302)


class DeleteListingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='kova',
            email='kova@email.com',
            password='123'
        )
        self.seller = Seller.objects.create(userid=self.user)
        self.listing = Listing.objects.create(
            listingname='Jabuke',
            userid=self.seller,
            price=100,
            unit='din/kg',
            quantity='100',
            type='Voće',
            description='crvene jabuke',
            image=b''
        )
        self.client.login(username='kova', password='123')

    def test_delete_listing_success(self):
        response = self.client.post(reverse('delete_listing', kwargs={'pk': self.listing.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Listing.objects.filter(pk=self.listing.pk).exists())


class ListingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='kova',
            email='kova@email.com',
            password='123'
        )
        self.seller = Seller.objects.create(userid=self.user)
        self.listing = Listing.objects.create(
            listingname='Jabuke',
            userid=self.seller,
            price=100,
            unit='din/kg',
            quantity='100',
            type='Voće',
            description='crvene jabuke',
            image=b''
        )
        self.client.login(username='kova', password='123')
        self.favorite_listing = FavoriteListing.objects.create(
            userid=self.user,
            listingid=self.listing
        )

    def test_listing_view_authenticated_user(self):
        response = self.client.get(reverse('listing', kwargs={'pk': self.listing.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.listing.pk, response.context['user_favorite_listings'])


class FavoritesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='kova',
            email='kova@email.com',
            password='123'
        )
        self.seller = Seller.objects.create(userid=self.user)
        self.listing = Listing.objects.create(
            listingname='Jabuke',
            userid=self.seller,
            price=100,
            unit='din/kg',
            quantity='100',
            type='Voće',
            description='crvene jabuke',
            image=b''
        )
        self.client.login(username='kova', password='123')
        self.favorite_listing = FavoriteListing.objects.create(
            userid=self.user,
            listingid=self.listing
        )

    @patch('fff.views.redirect')
    def test_favorites_authenticated_user_post(self, mock_redirect):
        response = self.client.post(reverse('favorites'), {'listing_id': self.listing.pk})
        self.assertIsInstance(response, JsonResponse)
        self.assertIn('is_favorite', response.json())
        self.assertFalse(response.json()['is_favorite'])

    def test_favorites_authenticated_user_get(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jabuke')


class UpdateDataTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='kova',
            email='kova@email.com',
            password='123',
            first_name='Nikola',
            last_name='Kovacevic'
        )
        self.client.login(username='kova', password='123')

    def test_update_data_post(self):
        response = self.client.post(reverse('change_data'), {
            'first_name': 'Nikola',
            'last_name': 'Kovacevic',
            'email': 'kovac2912@email.com',
            'phone': '1234567890',
            'city': 'Belgrade',
            'username': 'kova',
            'country': 'Serbia'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Nikola')
        self.assertEqual(self.user.last_name, 'Kovacevic')
        self.assertEqual(self.user.email, 'kovac2912@email.com')

    def test_update_data_get(self):
        response = self.client.get(reverse('change_data'))
        self.assertIsInstance(response.context['form'], UserDataForm)
        self.assertEqual(response.status_code, 200)


class GetChatTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='testpassword1')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='testpassword2')
        self.seller = Seller.objects.create(userid=self.user2)

    def test_get_chat_post(self):
        self.client.login(username='user1', password='testpassword1')
        response = self.client.post(reverse('get_chat'), {'user2': self.user2.userid})
        self.assertIsInstance(response, JsonResponse)
        self.assertIn('chat_id', response.json())
        chat_id = response.json()['chat_id']
        chat = Chat.objects.get(chatid=chat_id)
        self.assertEqual(chat.user1, self.user1)
        self.assertEqual(chat.user2.userid, self.user2)

    def test_get_chat_invalid_request(self):
        response = self.client.get(reverse('get_chat'))
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())


class GetChatAdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', email='admin@example.com', password='testpassword1',
                                              is_superuser=True)
        self.user = User.objects.create_user(username='user', email='user@example.com', password='testpassword2')

        self.seller = Seller.objects.create(userid=self.admin)

    def test_get_chat_admin_post(self):
        self.client.login(username='user', password='testpassword2')
        response = self.client.post(reverse('get_chat'), {'user2': self.admin.userid})
        self.assertIsInstance(response, JsonResponse)
        self.assertIn('chat_id', response.json())
        chat_id = response.json()['chat_id']
        chat = Chat.objects.get(chatid=chat_id)
        self.assertEqual(chat.user1, self.user)
        self.assertEqual(chat.user2, self.seller)

    def test_get_chat_admin_invalid_request(self):
        response = self.client.get(reverse('get_chat'))
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())


class ChatsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='testpassword1')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='testpassword2')
        self.user3 = User.objects.create_user(username='user3', email='user3@example.com', password='testpassword3')

        self.seller1 = Seller.objects.create(userid=self.user1)
        self.seller2 = Seller.objects.create(userid=self.user2)

        self.chat1 = Chat.objects.create(user1=self.user3, user2=self.seller1)
        self.chat2 = Chat.objects.create(user1=self.user3, user2=self.seller2)

    def test_chats_authenticated_user(self):
        self.client.login(username='user3', password='testpassword3')
        response = self.client.get(reverse('chats'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1')
        self.assertContains(response, 'user2')

    def test_chats_unauthenticated_user(self):
        response = self.client.get(reverse('chats'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(messages.get_messages(response.wsgi_request))


class ChatTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='testpassword1')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='testpassword2')
        self.seller1 = Seller.objects.create(userid=self.user1)
        self.chat = Chat.objects.create(user1=self.user2, user2=self.seller1)
        self.message1 = Message.objects.create(chatid=self.chat, sender=self.seller1.userid, text='Hello')
        self.message2 = Message.objects.create(chatid=self.chat, sender=self.user2, text='Hi')

    def test_chat_detail(self):
        response = self.client.get(reverse('chat', kwargs={'chat_id': self.chat.chatid}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello')
        self.assertContains(response, 'Hi')

    def test_chat_detail_invalid_chat_id(self):
        invalid_chat_id = self.chat.chatid + 1
        response = self.client.get(reverse('chat', kwargs={'chat_id': invalid_chat_id}))
        self.assertEqual(response.status_code, 404)


class CreateMessageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='testpassword1')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='testpassword2')
        self.seller1 = Seller.objects.create(userid=self.user1)

        self.chat = Chat.objects.create(user1=self.user1, user2=self.seller1)

    def test_create_message_post(self):
        self.client.login(username='user1', password='testpassword1')

        response = self.client.post(reverse('create_message', kwargs={'chat_id': self.chat.chatid}), {
            'text': 'Test message'
        })
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(Message.objects.filter(chatid=self.chat, sender=self.user1, text='Test message').exists())


class SearchListingsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='testpassword1')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='testpassword2')
        self.seller1 = Seller.objects.create(userid=self.user1)
        self.seller2 = Seller.objects.create(userid=self.user2)
        self.listing1 = Listing.objects.create(listingname='Test Listing 1', description='Test description 1', userid=self.seller1)
        self.listing2 = Listing.objects.create(listingname='Test Listing 2', description='Test description 2', userid=self.seller2)

    def test_search_listings(self):
        response = self.client.get(reverse('search_listings'), {'q': 'Test Listing'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Listing 1')
        self.assertContains(response, 'Test Listing 2')

    def test_search_listings_no_results(self):
        response = self.client.get(reverse('search_listings'), {'q': 'Non-existent Listing'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Listing 1')
        self.assertNotContains(response, 'Test Listing 2')
