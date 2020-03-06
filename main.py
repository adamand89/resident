from load_urls import decide_city
from get_data import create_df

def list_of_objects(city, n):
    list_urls = decide_city(city=city, n=n)
    df = create_df(city_urls=list_urls)
    return df



aa = decide_city('falköping',2)
create_df(aa)

# list_of_objects(city='falköping', n=3)



