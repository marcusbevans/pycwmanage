"""Tests for the CWManage API client"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from pycwmanage import CWManage
from pycwmanage.cwmanage import join_url


class TestCWManageBasic:
    """Basic tests that don't require API connection"""
    
    def test_join_url(self):
        """Test the join_url utility function"""
        assert join_url('https://test.com', 'subfolder', 'subsubfolder') == 'https://test.com/subfolder/subsubfolder'
        assert join_url('https://test.com') == 'https://test.com'
        assert join_url('https://test.com', '/api', 'endpoint') == 'https://test.com/api/endpoint'
    
    @patch('pycwmanage.cwmanage.requests.get')
    def test_cw_manage_init(self, mock_get):
        """Test CWManage initialization and authorization header generation"""
        # Mock the company info response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'Codebase': 'v2024_1/',
            'SiteUrl': 'api-na.myconnectwise.net'
        }
        mock_get.return_value = mock_response
        
        api = CWManage(
            connectwise_site='na.myconnectwise.net',
            company_id='company',
            public_key='public',
            private_key='private',
            client_id='client',
        )
        
        # Test authorization header generation
        assert api._authorization() == {
            'Authorization': 'Basic Y29tcGFueStwdWJsaWM6cHJpdmF0ZQ==',
            'clientId': 'client',
        }
        
        # Test URL construction
        assert api._url == 'https://api-na.myconnectwise.net/v2024_1/apis/3.0'


class TestReturnResponseFeature:
    """Tests for the new return_response functionality"""
    
    @patch('pycwmanage.cwmanage.requests.get')
    def test_get_with_return_response_false(self, mock_get):
        """Test get method with return_response=False (default behavior)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'id': 1, 'name': 'Test'}]
        mock_get.return_value = mock_response
        
        # Setup API client with mocked initialization
        with patch.object(CWManage, '__post_init__', return_value=None):
            api = CWManage(
                connectwise_site='test.com',
                company_id='test',
                public_key='test',
                private_key='test',
                client_id='test'
            )
            # Use object.__setattr__ to set frozen field
            object.__setattr__(api, '_url', 'https://test.com/api')
            
            # Test default behavior (return_response=False)
            result = api.get('/test')
            assert result == [{'id': 1, 'name': 'Test'}]
            assert isinstance(result, list)
    
    @patch('pycwmanage.cwmanage.requests.get')
    def test_get_with_return_response_true(self, mock_get):
        """Test get method with return_response=True"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'id': 1, 'name': 'Test'}]
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_get.return_value = mock_response
        
        # Setup API client with mocked initialization
        with patch.object(CWManage, '__post_init__', return_value=None):
            api = CWManage(
                connectwise_site='test.com',
                company_id='test',
                public_key='test',
                private_key='test',
                client_id='test'
            )
            # Use object.__setattr__ to set frozen field
            object.__setattr__(api, '_url', 'https://test.com/api')
            
            # Test new behavior (return_response=True)
            result = api.get('/test', return_response=True)
            assert result == mock_response
            assert result.status_code == 200
            assert result.headers == {'Content-Type': 'application/json'}
    
    @patch('pycwmanage.cwmanage.requests.post')
    def test_post_with_return_response(self, mock_post):
        """Test post method with return_response parameter"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 1, 'created': True}
        mock_response.headers = {'Location': '/resource/1'}
        mock_post.return_value = mock_response
        
        # Setup API client with mocked initialization
        with patch.object(CWManage, '__post_init__', return_value=None):
            api = CWManage(
                connectwise_site='test.com',
                company_id='test',
                public_key='test',
                private_key='test',
                client_id='test'
            )
            # Use object.__setattr__ to set frozen field
            object.__setattr__(api, '_url', 'https://test.com/api')
            
            test_data = {'name': 'Test Resource'}
            
            # Test default behavior
            result = api.post('/test', test_data)
            assert result == {'id': 1, 'created': True}
            
            # Test with return_response=True
            result = api.post('/test', test_data, return_response=True)
            assert result == mock_response
            assert result.headers == {'Location': '/resource/1'}
    
    @patch('pycwmanage.cwmanage.requests.delete')
    def test_delete_with_return_response(self, mock_delete):
        """Test delete method with return_response parameter"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.headers = {'X-Deleted': 'true'}
        mock_delete.return_value = mock_response
        
        # Setup API client with mocked initialization
        with patch.object(CWManage, '__post_init__', return_value=None):
            api = CWManage(
                connectwise_site='test.com',
                company_id='test',
                public_key='test',
                private_key='test',
                client_id='test'
            )
            # Use object.__setattr__ to set frozen field
            object.__setattr__(api, '_url', 'https://test.com/api')
            
            # Test default behavior
            result = api.delete('/test/1')
            assert result is True
            
            # Test with return_response=True
            result = api.delete('/test/1', return_response=True)
            assert result == mock_response
            assert result.status_code == 204


class TestIntegration:
    """Integration tests that require actual API credentials (loaded from .env)"""
    
    @pytest.mark.skipif(
        not os.getenv('CW_COMPANY_ID'),
        reason="API credentials not available in environment"
    )
    def test_real_api_connection(self):
        """Test actual API connection if credentials are available"""
        api = CWManage(
            connectwise_site=os.getenv('CW_API_URL', 'na.myconnectwise.net'),
            company_id=os.getenv('CW_COMPANY_ID'),
            public_key=os.getenv('CW_PUBLIC_KEY'),
            private_key=os.getenv('CW_PRIVATE_KEY'),
            client_id=os.getenv('CW_CLIENT_ID')
        )
        
        # Test a simple GET request
        response = api.get('/company/companies?pageSize=1', return_response=True)
        
        # Verify we got a response object
        assert hasattr(response, 'status_code')
        assert hasattr(response, 'headers')
        assert hasattr(response, 'json')
        
        # If successful, verify we can get JSON data
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)