import common
import unittest

class TestHandlerCase(unittest.TestCase):

    def test_email_required(self):
        print("testing returns erver error message")
        message = "bad day"
        result = common.return_server_error(message)
        print(result)
        self.assertEqual(result['statusCode'], 500)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn(message, result['body'])

if __name__ == '__main__':
    unittest.main()
