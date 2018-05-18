import json

import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = giphy_client.DefaultApi()
api_key = 'dc6zaTOxFJmzC' # str | Giphy API Key.
q = 'cheeseburgers' # str | Search query term or prhase.
limit = 5 # int | The maximum number of records to return. (optional) (default to 25)
offset = 0 # int | An optional results offset. Defaults to 0. (optional) (default to 0)
rating = 'g' # str | Filters results by specified rating. (optional)
lang = 'en' # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

try:
    # Search Endpoint
    api_response = api_instance.gifs_search_get(api_key, q, limit=limit, offset=offset, rating=rating, lang=lang, fmt=fmt)
    print("#'#########################'")
    #pprint(api_response)
    print("#'#########################'")
    # response_dict = json.loads(str(api_response))
    # pprint(type(response_dict))

    # data = api_response.data
    # print(data[0]['url'])

    #x = formatted_response['data'][0]['url']
    #print(x)

    # y = formatted_response[10:13]
    # pprint(y['data'][0]['url'])
    # pprint(y)


except ApiException as e:
    print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)


def data_pull():
    x = api_response.data
    y = x[0]
    gif_url = y.url
    some = y.slug
    print(gif_url)
    print(some)

data_pull()
