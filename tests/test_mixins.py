import sys
import unittest
from mock import patch, MagicMock

from cmd_line_tools.mixins import *


class SimpleCommandLineParserMixinTestCase(unittest.TestCase):
    def test_with_arguments(self):
        testargs = ["my_script", "username=johndoe", "password=123"]
        with patch.object(sys, 'argv', testargs):
            m = SimpleCommandLineParserMixin()
            m.parse_arguments()
            self.assertEqual(m._arguments['username'], 'johndoe')
            self.assertEqual(m._arguments['password'], '123')

    def test_with_no_arguments(self):
        testargs = ["my_script"]
        with patch.object(sys, 'argv', testargs):
            m = SimpleCommandLineParserMixin()
            m.parse_arguments()
            self.assertEqual(len(m._arguments), 0)

class InputTestCase(unittest.TestCase):
    def test_with_simple_arguments_request(self):
        mixin = InputRequestMixin()
        # Patch Username
        with patch('six.moves.input', return_value='johndoe') as m:
            value = mixin.request_input_data('username')
            m.assert_called_once_with("Please provide username: ")
            self.assertEqual(value, 'johndoe')

        # Patch Password
        with patch('six.moves.input', return_value='PW123') as m:
            value = mixin.request_input_data('password')
            m.assert_called_once_with("Please provide password: ")
            self.assertEqual(value, 'PW123')


# See test_commands.py for an explanation of this test
def test_calculator_with_user_input(capsys):
    class DummyTestingClass(StdoutOutputMixin):
        def main(self):
            self.write("Hello World")
            self.write("Goodbye World")

    DummyTestingClass().main()
    out, err = capsys.readouterr()
    assert out == 'Hello World\nGoodbye World\n'


class AuthenticationMixinsTestCase(unittest.TestCase):

    def test_authenticate_user(self):
        authenticated_mock = MagicMock(return_value={
            'username': 'johndoe',
            'password': 'password'
        })

        class DummyLoginCommand(LoginMixin):
            def request_input_data(self, data):
                if data == 'username':
                    return 'johndoe'
                elif data == 'password':
                    return 'PWD$123'

            authenticate = authenticated_mock

        obj = DummyLoginCommand()
        user = obj.login()

        self.assertEqual(user, {
            'username': 'johndoe',
            'password': 'password'
        })
        self.assertEqual(user, obj.user)

        obj.authenticate.assert_called_once_with('johndoe', 'PWD$123')
        self.assertTrue(obj.is_authenticated)

    def test_invalid_user(self):
        authenticated_mock = MagicMock(return_value=None)

        class DummyLoginCommand(LoginMixin):
            def request_input_data(self, data):
                if data == 'username':
                    return 'no-user'
                elif data == 'password':
                    return 'no-pass'

            authenticate = authenticated_mock

        obj = DummyLoginCommand()
        user = obj.login()

        self.assertIsNone(user)
        obj.authenticate.assert_called_once_with('no-user', 'no-pass')
        self.assertFalse(obj.is_authenticated)
        self.assertIsNone(obj.user)
    
    def test_authenticate_db_user(self):
        authenticated_mock = MagicMock(return_value={
            'username': 'johndoe',
            'password': 'password'
        })

        class DummyLoginCommand(LoginMixin,DbAuthenticationMixin):
            def request_input_data(self, data):
                if data == 'username':
                    return 'johndoe'
                elif data == 'password':
                    return 'PWD$123'

            authenticate = authenticated_mock

        obj = DummyLoginCommand()
        user = obj.login()

        self.assertEqual(user, {
            'username': 'johndoe',
            'password': 'password'
        })
        self.assertEqual(user, obj.user)

        obj.authenticate.assert_called_once_with('johndoe', 'PWD$123')
        self.assertTrue(obj.is_authenticated)
