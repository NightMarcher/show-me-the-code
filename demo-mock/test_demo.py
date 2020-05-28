'''
type `pytest -sv` to run test
'''
from unittest import TestCase
from unittest.mock import patch

from demo import func


class TestDemo(TestCase):

    def setUp(self):
        '''
        init before every test method
        '''

    def test_wrong_input(self):
        res = func(None)
        assert res[0] == False
        assert res[1] == 'please check your input params'

    # @patch('defines.get_host_ip')  # wrong mock (where defines)
    @patch('demo.get_host_ip')  # mock where you import and use
    def test_socket_error(self, mock_get_host_ip):
        print(f'### {__name__}: id(mock_get_host_ip): {id(mock_get_host_ip)}')
        mock_get_host_ip.side_effect = Exception('Error Msg')
        res = func('Hello World')
        assert res[0] == False
        assert res[1] == 'Error Msg'

    @patch('demo.get_host_ip')
    @patch('demo.get_now_str')
    def test_success(self, mock_get_now_str, mock_get_host_ip):
        print(f'### {__name__}: id(mock_get_host_ip): {id(mock_get_host_ip)}')
        mock_get_host_ip.return_value = '8.8.8.8'
        mock_get_now_str.return_value = 'now_str'
        res = func('Hello World')
        assert res[0] == True
        assert res[1] == {'name': 'Hello World',
                          'ip': '8.8.8.8', 'now': 'now_str'}

    def tearDown(self):
        '''
        do something after every test method
        '''
