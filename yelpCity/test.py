import unittest
import YelpCity
import time

class TestYelp(unittest.TestCase):

    def test_create(self):
        my_yelp = YelpCity.YelpRanking('wSdDzLyKX11alfcYGWA1dFGdnteewC7v-zrgM1EjNvj2Rll-v7GEefpzNl-tE06nYNctrSszKusIMR1qrBe5hzCgBqQdJgV_aSuC5HokPdd10W0JfnsuO_rLT1uPXnYx')
        

if __name__ == '__main__':
    #unittest.main()
    start = time.time()
    YelpCity.YelpRanking('wSdDzLyKX11alfcYGWA1dFGdnteewC7v-zrgM1EjNvj2Rll-v7GEefpzNl-tE06nYNctrSszKusIMR1qrBe5hzCgBqQdJgV_aSuC5HokPdd10W0JfnsuO_rLT1uPXnYx')
    end = time.time()
    print(end - start)
