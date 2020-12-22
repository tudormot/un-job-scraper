import json  as j
import requests
import pprint
pp = pprint.PrettyPrinter(indent=1)

r = requests.get('https://internationalcareerfinder.com/wp-json/')
#r.json()
# print(r.json()) #.json returns a dict
# pp.pprint(r.json())

json_object = j.dumps(r.json(), indent = 2)
print(json_object)