import requests

#endpoint = "https://httpbin.org/status/200/"#html
#endpoint = "https://httpbin.org/anything" #api
endpoint = "http://127.0.0.1:8000/api/" # my django endpoit


get_response = requests.get(endpoint, json={"product_id" : 123}) # eco back data


# Application programming interface -> API
# HTTP Request -> HTML
# REST API HTTP REQUEST -> JSON

#JavaScript Object Notation ~ Python Dict .JSON

#print(get_response.text) # print raw text response
print(get_response.json()) # as python dicts
#print(get_response.status_code) # status code
