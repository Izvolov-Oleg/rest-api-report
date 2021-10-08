import unittest
import report_rest_api


class TestFlaskRestapi(unittest.TestCase):

    def setUp(self):
        app = report_rest_api.app
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_01_status(self):
        """Test that the flask api server is running and reachable when format=json"""
        response = self.app.get('/api/v1/report/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_02_status(self):
        """Test that the flask api server is running and reachable when format=xml"""
        response = self.app.get('/api/v1/report/?format=xml')
        self.assertEqual(response.status_code, 200)

    def test_03_status(self):
        """Test that the flask api server isn't running and reachable when the wrong format"""
        response = self.app.get('/api/v1/report/?format=jso')
        self.assertEqual(response.status_code, 405)

    def test_04_content_json(self):
        """The content type test when format=json"""
        response = self.app.get('/api/v1/report/?format=json')
        self.assertEqual(response.content_type, "application/json")

    def test_05_content_xml(self):
        """The content type test when format=xml"""
        response = self.app.get('/api/v1/report/?format=xml')
        self.assertEqual(response.content_type, "text/xml")


if __name__ == '__main__':
    unittest.main()
