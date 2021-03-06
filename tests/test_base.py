from http import client
from flask_testing import TestCase
from app import auth
from main import app
from flask import current_app,url_for

class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True #Para que Flask sepa que está en modo de pruebas
        app.config['WTF_CSRF_ENABLED'] = False #Desactivar el Cross-Site Request Forgery
        return app


    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response,url_for('home'))

    def test_hello_get(self):
        response = self.client.get(url_for('home'))
        self.assert200(response)

    def test_hello_post(self):
        response = self.client.post(url_for('home'))
        self.assertTrue(response.status_code, 405)


    def test_auth_blueprint_exists(self):
        self.assertIn('auth',self.app.blueprints)

    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')

    def test_auth_login_post(self):
        fake_form = {
            'username':'santiago',
            'password':'santiago'
        }
        response = self.client.post(url_for('auth.login'),data=fake_form)
        self.assertRedirects(response,url_for('index'))