import unittest
import YelpCity

class TestYelp(unittest.TestCase):
    API_KEY = None
    def test_create(self):
        my_yelp = YelpCity.YelpRanking(self.API_KEY)
        

if __name__ == '__main__':
    TestYelp.API_KEY = input('Enter API key\n')
    unittest.main()
