import unittest
import YelpCity

class TestYelp(unittest.TestCase):
    API_KEY = None
        my_yelp = YelpCity.FindBusinesses(self.API_KEY)
    def test_create(self):
        

if __name__ == '__main__':
    TestYelp.API_KEY = input('Enter API key\n')
    unittest.main()
