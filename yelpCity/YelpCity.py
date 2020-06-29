from pyzipcode import ZipCodeDatabase
import json
import requests
import pandas as pd
from multiprocessing import Pool


class YelpRanking(object):
    """
    This class is for getting all search results of a yelp search
    for a given city.

    ...

    Attributes
    ----------
    key : str
        The yelp API key needed to call Yelp Fusion API.
    city : str
        The city to search over.

    Methods
    -------
    find_businesses(zip_code):
        Find the search terms for a given pyzipcode.ZipCode object
    get_businesses(start, ending, location, url, headers):
        
    """
    
    def __init__(self, key, city = 'San Francisco'):
        """
        The construct for the YelpCity class.

        Parameters
        ----------
            key : str
                The yelp API key needed to call Yelp Fusion API.
            city : str
                The city to search over.
        """

        api_host = 'https://api.yelp.com'
        search_path = '/v3/businesses/search'
        business_path = '/v3/businesses/'
        zcdb = ZipCodeDatabase()
        self.url = api_host + search_path
        self.headers = {
            'Authorization' : 'Bearer %s' % key,
        }
        self.business_id_set = set()
        selfget_businesses(self, start, ending, location, url, headers).business_list = []
        for zip_obj in zcdb.find_zip(city = city):
            self.business_list += self.find_businesses(zip_obj)

    def find_businesses(self, zip_code):
        """
        The function to find all the search terms for the given city.

        Parameters
        ----------
        zip_code : pyzipcode.ZipCode
            The pyzipcode object assciated with the zip code.

        Returns
        -------
        lst : List
            List of Dictionary objects that hold the information of 
            the businesses given by the yelp fusion API of the given
            zip code object
        """
        
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
        """
        Returns the business information from the start offset to 
        the end offset with a total of 50 businesses.

        Parameters
        ----------
        start : int
            The starting offset to start searching from
        ending : int 
            The endpoint of the search
        location : int
            The location to search for
        url : str
            The url to pass the request to
        headers: dict
            The headers to pass in the request

        Retruns
        -------
        lst : List
            List of Dictionary objects that hold the information of 
            the businesses given by the yelp fusion API of the given
            location. There will be a maximum of 50 object inside
            the lst.
        """
        
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
        """
        Returns a json format of self.business_list
        
        Parameters
        ----------
        None

        Returns
        -------
        Json format of self.business_list
        """
        
        return json.dumps(self.business_list)
