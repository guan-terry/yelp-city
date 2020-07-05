# YelpCity

YelpCity is a Python library for obtaining search queries of more than 1000 limited by the Yelp Fusion API.

### Prerequisites

What things you need to install the software and how to install them
```bash
pip install pyzipcode
```
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
N/A
```

## Usage

```python
import YelpCity

my_yelp = YelpCity.FindBusinesses(YelpApiKey, City = 'San Francisco')
my_yelp.to_json() # returns yelp format of all restaurants in San Francisco
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
