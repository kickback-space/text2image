import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_text_to_image_get(self):
        response = self.app.get('/api/v1/text-to-image/')
        self.assertEqual(response.status_code, 405)

    @patch('app.pipe')
    def test_text_to_image_post_200(self, mock_pipe):
        mock_pipe_instance = MagicMock()
        mock_pipe.return_value = mock_pipe_instance
        mock_image = MagicMock()
        mock_image_instance = MagicMock()
        mock_image_instance.save = MagicMock()
        mock_image_instance.save.return_value = None
        mock_image.images = [mock_image_instance]
        mock_pipe_instance.return_value = mock_image

        data = {"prompt": "test!"}
        response = self.app.post('/api/v1/text-to-image/', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'image', response.data)

    @patch('app.pipe')
    def test_text_to_image_post_500(self, mock_pipe):
        mock_pipe_instance = None
        mock_pipe.return_value = mock_pipe_instance

        data = {"prompt": "test!"}
        response = self.app.post('/api/v1/text-to-image/', json=data)

        self.assertEqual(response.status_code, 500)
        self.assertIn(b'image', response.data)

if __name__ == '__main__':
    unittest.main()
