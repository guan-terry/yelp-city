from pyzipcode import ZipCodeDatabase
import json
import requests
import pandas as pd

class YelpRanking(object):
    """

    """
    

    def __init__(self, key, city = 'San Francisco'):
        api_host = 'https://api.yelp.com'
        search_path = '/v3/businesses/search'
        business_path = '/v3/businesses/'
        zcdb = ZipCodeDatabase()
        self.api_key = key
        url = api_host + search_path
        headers = {
            'Authorization' : 'Bearer %s' % key,
        }
        self.business_id_set = set()
        self.business_list = []
        for city_zip in zcdb.find_zip(city = city):
            param = {
                'location': str(city_zip.zip),
                'limit': 1,
                'offset': 0,
                'term': 'restaurants',
                'sort_by': 'best_match'
            }
            response = requests.request('GET', url = url, headers = headers, params = param)
            if response.status_code != 200: continue
            print(response)
            total = response.json()['total']
            print(city_zip.zip,total)
            #if city_zip.zip != '94124': continue
            total = min(total, 1000)
            self.get_businesses(0, total-total%50, city_zip.zip, url, headers)
            self.get_businesses(total- total%50, total, city_zip.zip, url, headers)

            # create dataframe to put response.text in it
            print(len(self.business_list))

    def get_businesses(self, start, ending, location, url, headers):
        for offset in range(start, ending + 1, 50):
            param = {
                    'location' : location,
                    'limit' : min(50, ending - start),
                    'offset': offset,
                    'term': 'restaurants',
                    'sort_by' : 'best_match'
            }
            response = requests.request('GET', url = url, headers = headers, params = param)
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
                self.business_list.append(new_dict)
