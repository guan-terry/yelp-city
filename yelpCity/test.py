import unittest
import YelpCity

class TestYelp(unittest.TestCase):
    API_KEY = None
    def test_create(self):
        my_yelp = YelpCity.FindBusinesses(self.API_KEY)
        my_yelp.to_json()

if __name__ == '__main__':
    TestYelp.API_KEY = input('Enter API key\n')
    unittest.main()
