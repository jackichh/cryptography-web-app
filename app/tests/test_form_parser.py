import unittest
from io import BytesIO
from app.utils.form_parser import parse_form

class TestFormParser(unittest.TestCase):
    def test_empty_form(self):
        """Test parsing empty form data"""
        environ = {
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': 'application/x-www-form-urlencoded',
            'CONTENT_LENGTH': '0',
            'wsgi.input': BytesIO(b'')
        }
        result = parse_form(environ)
        self.assertEqual(result, {})

    def test_urlencoded_form(self):
        """Test parsing URL-encoded form data"""
        form_data = b'name=John&age=30&city=New+York'
        environ = {
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': 'application/x-www-form-urlencoded',
            'CONTENT_LENGTH': str(len(form_data)),
            'wsgi.input': BytesIO(form_data)
        }
        result = parse_form(environ)
        self.assertEqual(result, {
            'name': 'John',
            'age': '30',
            'city': 'New York'
        })

    def test_multipart_form(self):
        """Test parsing multipart form data"""
        # Create a simple multipart form with a text field and a file
        boundary = b'boundary123'
        form_data = (
            b'--' + boundary + b'\r\n'
            b'Content-Disposition: form-data; name="text"\r\n\r\n'
            b'Hello World\r\n'
            b'--' + boundary + b'\r\n'
            b'Content-Disposition: form-data; name="file"; filename="test.txt"\r\n'
            b'Content-Type: text/plain\r\n\r\n'
            b'File content\r\n'
            b'--' + boundary + b'--\r\n'
        )
        
        environ = {
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': f'multipart/form-data; boundary={boundary.decode()}',
            'CONTENT_LENGTH': str(len(form_data)),
            'wsgi.input': BytesIO(form_data)
        }
        
        result = parse_form(environ)
        
        # Check text field
        self.assertEqual(result['text'], 'Hello World')
        
        # Check file upload
        self.assertIn('file', result)
        self.assertEqual(result['file']['filename'], 'test.txt')

    def test_invalid_content_type(self):
        """Test handling of the invalid content type"""
        environ = {
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': 'invalid/type',
            'CONTENT_LENGTH': '0',
            'wsgi.input': BytesIO(b'')
        }
        result = parse_form(environ)
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main() 