def decide_city(city, n):

    dict_of_cities = {
        "stockholm": 'https://www.booli.se/slutpriser/innanfor+tullarna/883816/?page=',
        'göteborg': 'https://www.booli.se/slutpriser/goteborg/22/?page=',
        'malmö': 'https://www.booli.se/slutpriser/malmo/78/?page=',
        'falköping': 'https://www.booli.se/slutpriser/falkoping/1678/?page='}


    # Get city url from dict
    if city == 'malmö':
        city_url = dict_of_cities.get('malmö')
    elif city == 'stockholm':
        city_url = dict_of_cities.get('stockholm')
    elif city == 'göteborg':
        city_url = dict_of_cities.get('göteborg')


    # Get latest n objects
    city_urls = []
    city_urls.append(city_url[:-6])

    for i in range(2, n+1):
        city_urls.append(city_url + str(i))

    return city_urls