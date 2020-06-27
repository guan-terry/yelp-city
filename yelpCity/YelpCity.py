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
        self.url = api_host + search_path
        self.headers = {
            'Authorization' : 'Bearer %s' % key,
        }
        self.business_id_set = set()
        self.business_list = []
        for zip_obj in zcdb.find_zip(city = city):
            self.business_list += self.business_zip(zip_obj)


        print(len(self.business_list))

    def business_zip(self, zip_code):
        param = {
                'location' : str(zip_code.zip),
                'limit' : 1,
                'offset' : 0,
                'term' : 'restaurants',
                'sort_by' : 'best_match',
        }
        response = requests.get(url = self.url, headers = self.headers, params = param)
        while response.status_code == 429: 
            response = requests.get(url = self.url, headers = self.headers, params = param)
        if not response.ok: 
            return []
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
                    'offset' : offset,
                    'term' : 'restaurants',
                    'sort_by' : 'best_match',
            }
            response = requests.request('GET', url = url, headers = headers, params = param)
            while response.status_code == 429: 
                response = requests.get(url = url, headers = headers, params = param)
            if not response.ok: continue

            for business in response.json()['businesses']:
                if business['id'] in self.business_id_set:
                    continue
                self.business_id_set.add(business['id'])

                curr_business_dict = {}

                for section in business:
                    curr_business_dict[section] = business[section]
                lst.append(curr_business_dict)
        return lst

    def to_json(self):
        return json.dumps(self.business_list)
