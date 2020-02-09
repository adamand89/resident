city = input('What Swedish city do you wish to get data from? ')
number = int(input('How many objects are you looking for? '))

dict_of_cities = {
    "stockholm": 'https://www.booli.se/slutpriser/innanfor+tullarna/883816/?page=',
    'göteborg': 'https://www.booli.se/slutpriser/goteborg/22/?page=',
    'malmö': 'https://www.booli.se/slutpriser/malmo/78/?page='}


# Get city url from dict
if city == 'malmö':
    city_url = dict_of_cities.get('malmö')
elif city == 'stockholm':
    city_url = dict_of_cities.get('stockholm')
elif city == 'göteborg':
    city_url = dict_of_cities.get('göteborg')


# Get latest n objects
list_of_city_urls = []
list_of_city_urls.append(city_url[:-6])

for i in range(2, 3):
    list_of_city_urls.append(city_url + str(i))

list_of_city_urls
