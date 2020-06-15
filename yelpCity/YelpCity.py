from pyzipcode import ZipCodeDatabase
import json
import requests
import pandas as pd
from multiprocessing import Pool

class YelpRanking(object):
    """

    """
    

    def __init__(self, key, city = 'San Francisco'):
        api_host = 'https://api.yelp.com'
        search_path = '/v3/businesses/search'
        business_path = '/v3/businesses/'
        zcdb = ZipCodeDatabase()
        #self.api_key = key
        self.url = api_host + search_path
        self.headers = {
            'Authorization' : 'Bearer %s' % key,
        }
        self.business_id_set = set()
        self.business_list = []
        with Pool(4) as p:
            lst = p.map(self.business_zip, zcdb.find_zip(city = city))

        lst = [item for sublist in lst if sublist is not None for item in sublist]
        '''
        for city_zip in zcdb.find_zip(city = city):
            param = {
                'location': str(city_zip.zip),
                'limit': 1,
                'offset': 0,
                'term': 'restaurants',
                'sort_by': 'best_match'
            }
            response = requests.get(url = url, headers = headers, params = param)
            print(city_zip.zip, response.status_code)
            if response.status_code != 200: continue
            if int(city_zip.zip) != 94124: continue
            #total = response.json()['total']
            #total = min(total, 1000)
            #self.get_businesses(0, total-total%50, city_zip.zip, url, headers)
            #self.get_businesses(total- total%50, total, city_zip.zip, url, headers)

            # create dataframe to put response.text in it
            #print(len(self.business_list))
        '''
        print(len(lst))

    def business_zip(self, zip_code):
        param = {
                'location': str(zip_code.zip),
                'limit' : 1,
                'offset' : 0,
                'term' : 'restaurants',
                'sort_by': 'best_match'
        }
        response = requests.get(url = self.url, headers = self.headers, params = param)
        print(zip_code.zip, response.status_code)
        while response.status_code == 429: 
            response = requests.get(url = self.url, headers = self.headers, params = param)
        if response.status_code != 200:
            print('ran Through')
            return
        if int(zip_code.zip) != 94124: return
        print('ran through code')
        total = response.json()['total']
        total = min(total, 1000)
        lst =  self.get_businesses(0, total - total % 50, zip_code.zip, self.url, self.headers)
        lst += self.get_businesses(total - total%50, total, zip_code.zip, self.url, self.headers)
        return lst

    def get_businesses(self, start, ending, location, url, headers):
        lst = []
        for offset in range(start, ending + 1, 50):
            param = {
                    'location' : location,
                    'limit' : min(50, ending - start),
                    'offset': offset,
                    'term': 'restaurants',
                    'sort_by' : 'best_match'
            }
            response = requests.request('GET', url = url, headers = headers, params = param)
            while response.status_code == 429: 
                response = requests.get(url = url, headers = headers, params = param)
            if response.status_code != 200: continue
            for business in response.json()['businesses']:
                new_dict = {}
                price = business['price'] if 'price' in business else None
                categories = [categories['alias'] for categories in business['categories']]
                new_dict['id'] = business['id']
                new_dict['name'] = business['name']
                new_dict['categories'] = categories
                new_dict['price'] = price
                new_dict['rating'] = business['rating']
                new_dict['review_count'] = business['review_count']
                lst.append(new_dict)
        return lst
