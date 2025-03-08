from django.test import TestCase, Client
from django.urls import reverse
import json
from authentication.views import *

class TestAuthViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')  # Remplacez par le nom de votre vue de connexion
        self.reset_password_url = reverse('change-password') # Remplacez par le nom de votre vue de réinitialisation de mot de passe
        self.user = User.objects.create_user(
            username='test.views',
            first_name='test',
            last_name='views',
            password='TestViews@3',
            quest_label='what is your favorite movie',
            sec_answ='the maze runner',
            email='djouadimohand&2@gmail.com',
        )
        self.userWithOtp = User.objects.create_user(
            username='test.otp',
            first_name='test',
            last_name='otp',
            password='TestOtp@3',
            quest_label='what is your favorite movie',
            sec_answ='the maze runner',
            email='testOtp@gmail.com'
        )
        self.userWithOtp.otp = '321245'
        self.userWithOtp.otp_expiry = timezone.now() + datetime.timedelta(minutes=20)
        print('userwithOtp', model_to_dict(self.userWithOtp))
    def test_signup_view(self):
        url = reverse('signup')
        methodNotAllRes = self.client.get(url)
        self.assertEqual(methodNotAllRes.status_code, 405)
        self.assertEqual(methodNotAllRes['Content-Type'], 'application/json')
        methodNotAllResCont = json.loads(methodNotAllRes.content)
        self.assertEqual(methodNotAllResCont, {'error': 'HTTP method not allowed'})
        signupExistUserRes = self.client.post(url, json.dumps({
            'username': 'test.views',
            'first_name': 'mohand',
            'last_name': 'djouadi',
            'email': 'mohand@gmail.com',
            'password': 'Mohand123$',
            'security_quest': 'what is your favorite movie',
            'security_answ': 'bleach'
        }), content_type='application/json')
        self.assertEqual(signupExistUserRes.status_code, 400)
        self.assertEqual(signupExistUserRes['Content-Type'], 'application/json')
        signupExistUserResCont = json.loads(signupExistUserRes.content)
        self.assertEqual(signupExistUserResCont, {'error': 'username or email already used'})
        signupRes = self.client.post(url, json.dumps({
            'username': 'djouadi.mohand',
            'first_name': 'mohand',
            'last_name': 'djouadi',
            'email': 'mohand@gmail.com',
            'password': 'Mohand123$',
            'security_quest': 'what is your favorite movie',
            'security_answ': 'bleach'
        }), content_type='application/json')
        self.assertEqual(signupRes.status_code, 200)
        self.assertEqual(signupRes['Content-Type'], 'application/json')
        signupResCont = json.loads(signupRes.content)
        self.assertIn('id', signupResCont)
        self.assertIn('first_name', signupResCont)
        self.assertIn('last_name', signupResCont)
        self.assertIn('password', signupResCont)
        self.assertIn('email', signupResCont)
        self.assertIn('username', signupResCont)
        self.assertIn('token', signupResCont)
        self.assertIn('security_quest', signupResCont)
        self.assertIn('security_answ', signupResCont)
        self.assertNotEqual(signupResCont['password'], 'Mohand123$')
    def test_login_view(self):
        url = reverse('login')
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(json.loads(self.client.get(url).content),  {'error': 'Méthode HTTP non autorisée'})
        loginReq = {
            'username': 'test.views',
            'password': 'TestViews@3'
        }
        loginRes = self.client.post(url, json.dumps(loginReq), content_type='application/json')
        self.assertEqual(loginRes.status_code, 200)
        loginResCont = json.loads(loginRes.content)
        self.assertIn('id', loginResCont)
        self.assertIn('first_name', loginResCont)
        self.assertIn('last_name', loginResCont)
        self.assertIn('email', loginResCont)
        self.assertIn('username', loginResCont)
        self.assertIn('token', loginResCont)
        self.assertIn('security_quest', loginResCont)
        loginWrPass = self.client.post(url, json.dumps({"username":"test.views", "password":"TESTviews23$"}), content_type='application/json')
        self.assertEqual(loginWrPass.status_code, 401)
        self.assertEqual(json.loads(loginWrPass.content), {'error': 'Nom d\'utilisateur ou mot de passe incorrect'})
    def test_get_otp(self):
        url = reverse('get-otp')
        postOtpRes = self.client.post(url)
        self.assertEqual(postOtpRes.status_code, 405)
        self.assertEqual(json.loads(postOtpRes.content), {'error':'HTTP method not allowed'})
        getOtpWrEmailRes = self.client.get(f'{url}?email=frdeswde')
        self.assertEqual(getOtpWrEmailRes.status_code, 404)
        self.assertEqual(json.loads(getOtpWrEmailRes.content), {'error': 'email not exist'})
        getOtpRes = self.client.get(url, query_params={'email':'djouadimohand&2@gmail.com'})
        self.assertEqual(getOtpRes.status_code, 200)
        self.assertEqual(json.loads(getOtpRes.content), {'message': 'OTP sent successfully'})
        self.assertFalse(self.user.otp, None)
        getOtpNotEmailRes = self.client.get(url)
        self.assertEqual(getOtpNotEmailRes.status_code, 400)
        self.assertEqual(json.loads(getOtpNotEmailRes.content), {'error':'email parameter is required'})
    def test_validate_otp(self):
        url = reverse('validate-otp')

        valOtpRes = self.client.post(url, json.dumps({'otp':'321245'}), content_type='application/json', query_params={'email':'testOtp@gmail.com'})
        print('res', json.loads(valOtpRes.content))
        self.assertEqual(valOtpRes.status_code, 200)
        self.assertEqual(json.loads(valOtpRes.content), {'message':'otp verified succesfully'})
        self.assertIsNone(self.user.otp)

        self.client.get(reverse('get-otp'), query_params={'email': 'djouadimohand&2@gmail.com'})
        print(self.user.username)
        valOtpReq = json.dumps({"otp": "324567"})
        valOtpRes = self.client.post(url, data=valOtpReq, content_type='application/json', query_params={'email': 'djouadimohand&2@gmail.com'})
        print(valOtpRes.content)
        self.assertEqual(valOtpRes.status_code, 400)
        self.assertEqual(json.loads(valOtpRes.content), {'error':'otp is not valide'})

        self.client.get(reverse('get-otp'), query_params={'email': 'djouadimohand&2@gmail.com'})
        otp = self.user.otp
        valOtpReq = { 'otp': '' }
        valOtpRes = self.client.post(url, data=valOtpReq, content_type='application/json', QUERY_PARAMS={'email': 'djouadimohand&2@gmail.com'})
        print('res', valOtpRes.content)
        self.assertEqual(valOtpRes.status_code, 404)
        self.assertEqual(json.loads(valOtpRes.content), {'error':'otp and email is required'})
    def test_forgot_password(self):
        pass
    def test_logout(self):
        loginRes = self.client.post(reverse('login'), json.dumps({
            'username': 'test.views',
            'password': 'TestViews@3'
        }), content_type='application/json')
        token = json.loads(loginRes.content).get('token', '')
        logoutRes = self.client.post(reverse('logout'),content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(logoutRes.status_code, 200)
        self.assertEqual(json.loads(logoutRes.content), {'message': 'user logged out'})
