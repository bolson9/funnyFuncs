import subscribe
import unittest

class TestHandlerCase(unittest.TestCase):

    def test_email_required(self):
        print("testing email is required")
        event = {'body': '{"message": "Hello World"}'}
        result = subscribe.handler(event, None)
        print(result)
        self.assertEqual(result['statusCode'], 500)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn('Email field is required', result['body'])

    def test_category_list(self):
        print("testing category must be in joke, quote, fact")
        event = {'body': '{"email": "test@test.com", "category": "notacategory"}'}
        result = subscribe.handler(event, None)
        print(result)
        self.assertEqual(result['statusCode'], 500)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn('is invalid. Must be one of', result['body'])


if __name__ == '__main__':
    unittest.main()
