import unittest
from unittest.mock import Mock, patch
import azure.functions as func
import sys
import os

# src配下のモジュールをインポートできるようにパスを追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from function_app import multiply, divide, validate_params, create_html_response


class TestValidateParams(unittest.TestCase):
    """パラメータ検証関数のテスト"""
    
    def test_valid_params(self):
        """正常なパラメータの場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '10.5', 'B': '2.5'}.get(key)
        
        a, b, error = validate_params(req)
        
        self.assertEqual(a, 10.5)
        self.assertEqual(b, 2.5)
        self.assertIsNone(error)
    
    def test_missing_params(self):
        """パラメータが未指定の場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: None
        
        a, b, error = validate_params(req)
        
        self.assertIsNone(a)
        self.assertIsNone(b)
        self.assertEqual(error, 'パラメータAとBを指定してください')
    
    def test_missing_param_a(self):
        """パラメータAが未指定の場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'B': '5'}.get(key)
        
        a, b, error = validate_params(req)
        
        self.assertIsNone(a)
        self.assertIsNone(b)
        self.assertEqual(error, 'パラメータAとBを指定してください')
    
    def test_invalid_number_format(self):
        """数値以外が指定された場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': 'abc', 'B': '5'}.get(key)
        
        a, b, error = validate_params(req)
        
        self.assertIsNone(a)
        self.assertIsNone(b)
        self.assertEqual(error, 'AとBは数値で指定してください')
    
    def test_negative_number(self):
        """負の数が指定された場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '-5', 'B': '10'}.get(key)
        
        a, b, error = validate_params(req)
        
        self.assertIsNone(a)
        self.assertIsNone(b)
        self.assertEqual(error, 'AとBは正の数を指定してください')
    
    def test_zero_value(self):
        """ゼロが指定された場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '0', 'B': '10'}.get(key)
        
        a, b, error = validate_params(req)
        
        self.assertIsNone(a)
        self.assertIsNone(b)
        self.assertEqual(error, 'AとBは正の数を指定してください')
    
    def test_very_small_positive_number(self):
        """非常に小さい正の数の場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '0.0001', 'B': '0.0002'}.get(key)
        
        a, b, error = validate_params(req)
        
        self.assertEqual(a, 0.0001)
        self.assertEqual(b, 0.0002)
        self.assertIsNone(error)
    
    def test_very_large_number(self):
        """非常に大きい数の場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '1000000', 'B': '9999999'}.get(key)
        
        a, b, error = validate_params(req)
        
        self.assertEqual(a, 1000000)
        self.assertEqual(b, 9999999)
        self.assertIsNone(error)


class TestMultiplyFunction(unittest.TestCase):
    """掛け算API関数のテスト"""
    
    @patch('function_app.logging')
    def test_multiply_success(self, mock_logging):
        """正常な掛け算の計算"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '10', 'B': '5'}.get(key)
        req.method = 'GET'
        req.url = 'http://test.com/api/multiply?A=10&B=5'
        req.headers = {}
        
        response = multiply(req)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.mimetype)
        self.assertIn('50', response.get_body().decode('utf-8'))
        self.assertIn('10 × 5', response.get_body().decode('utf-8'))
    
    @patch('function_app.logging')
    def test_multiply_with_decimals(self, mock_logging):
        """小数の掛け算"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '2.5', 'B': '4.2'}.get(key)
        req.method = 'POST'
        req.url = 'http://test.com/api/multiply'
        req.headers = {}
        
        response = multiply(req)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('10.5', response.get_body().decode('utf-8'))
    
    @patch('function_app.logging')
    def test_multiply_missing_params(self, mock_logging):
        """パラメータ未指定の場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: None
        req.method = 'GET'
        req.url = 'http://test.com/api/multiply'
        req.headers = {}
        
        response = multiply(req)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('パラメータAとBを指定してください', response.get_body().decode('utf-8'))
    
    @patch('function_app.logging')
    def test_multiply_invalid_number(self, mock_logging):
        """数値以外が指定された場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': 'abc', 'B': '5'}.get(key)
        req.method = 'GET'
        req.url = 'http://test.com/api/multiply'
        req.headers = {}
        
        response = multiply(req)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('AとBは数値で指定してください', response.get_body().decode('utf-8'))
    
    @patch('function_app.logging')
    def test_multiply_negative_number(self, mock_logging):
        """負の数が指定された場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '-5', 'B': '10'}.get(key)
        req.method = 'GET'
        req.url = 'http://test.com/api/multiply'
        req.headers = {}
        
        response = multiply(req)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('AとBは正の数を指定してください', response.get_body().decode('utf-8'))


class TestDivideFunction(unittest.TestCase):
    """割り算API関数のテスト"""
    
    @patch('function_app.logging')
    def test_divide_success(self, mock_logging):
        """正常な割り算の計算"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '10', 'B': '5'}.get(key)
        req.method = 'GET'
        req.url = 'http://test.com/api/divide?A=10&B=5'
        req.headers = {}
        
        response = divide(req)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.mimetype)
        self.assertIn('2', response.get_body().decode('utf-8'))
        self.assertIn('10 ÷ 5', response.get_body().decode('utf-8'))
    
    @patch('function_app.logging')
    def test_divide_with_decimals(self, mock_logging):
        """小数の割り算"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '10.5', 'B': '2.5'}.get(key)
        req.method = 'POST'
        req.url = 'http://test.com/api/divide'
        req.headers = {}
        
        response = divide(req)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('4.2', response.get_body().decode('utf-8'))
    
    @patch('function_app.logging')
    def test_divide_missing_params(self, mock_logging):
        """パラメータ未指定の場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: None
        req.method = 'GET'
        req.url = 'http://test.com/api/divide'
        req.headers = {}
        
        response = divide(req)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('パラメータAとBを指定してください', response.get_body().decode('utf-8'))
    
    @patch('function_app.logging')
    def test_divide_invalid_number(self, mock_logging):
        """数値以外が指定された場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': 'xyz', 'B': '5'}.get(key)
        req.method = 'GET'
        req.url = 'http://test.com/api/divide'
        req.headers = {}
        
        response = divide(req)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('AとBは数値で指定してください', response.get_body().decode('utf-8'))
    
    @patch('function_app.logging')
    def test_divide_negative_number(self, mock_logging):
        """負の数が指定された場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '10', 'B': '-5'}.get(key)
        req.method = 'GET'
        req.url = 'http://test.com/api/divide'
        req.headers = {}
        
        response = divide(req)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('AとBは正の数を指定してください', response.get_body().decode('utf-8'))
    
    @patch('function_app.logging')
    def test_divide_by_zero_blocked_by_validation(self, mock_logging):
        """ゼロ除算がバリデーションでブロックされる場合"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.side_effect = lambda key: {'A': '10', 'B': '0'}.get(key)
        req.method = 'GET'
        req.url = 'http://test.com/api/divide'
        req.headers = {}
        
        response = divide(req)
        
        self.assertEqual(response.status_code, 400)
        # validate_paramsでゼロがブロックされるため
        self.assertIn('AとBは正の数を指定してください', response.get_body().decode('utf-8'))


class TestCreateHtmlResponse(unittest.TestCase):
    """HTMLレスポンス作成関数のテスト"""
    
    def test_create_html_response_success(self):
        """正常なHTMLレスポンスの作成"""
        content = '<h1>テスト</h1><p>内容</p>'
        response = create_html_response(content)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.mimetype)
        body = response.get_body().decode('utf-8')
        self.assertIn('<!DOCTYPE html>', body)
        self.assertIn('<h1>テスト</h1>', body)
    
    def test_create_html_response_with_status_code(self):
        """ステータスコード指定のHTMLレスポンスの作成"""
        content = '<h1>エラー</h1>'
        response = create_html_response(content, status_code=400)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('text/html', response.mimetype)


if __name__ == '__main__':
    unittest.main()
