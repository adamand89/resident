from load_urls import decide_city
from bs4 import BeautifulSoup
import requests
import numpy as np
import datetime as dt
import pandas as pd
import re


def create_df(city_urls):


    adress = []
    sq_m = []
    rooms = []
    type_ = []
    price = []
    price_sq = []
    date = []
    bid_percent = []
    latitude = []
    longitude = []

    for list_of_objects in city_urls:
        page_response = requests.get(list_of_objects, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        objekt = page_content.find_all(class_='search-list')[0]

        for object_info in range(0, 36):
            get_object = objekt.find_all(
                class_='search-list__item')[object_info]
            

            obj_bid_percent = get_object.find_all(
                class_='search-list__column search-list__column--price-change')[0].text
            obj_bid_percent = obj_bid_percent[2:]
            

            object_info = get_object.find_all(
                class_='search-list__column search-list__column--info-1')[0]
            object_info_sales = get_object.find_all(
                class_='search-list__column search-list__column--info-2')[0]

            # obj_lat = float(obj_lat)
            lat = get_object.find_all(
                class_='search-list__link')
            lat = str(lat)
            obj_lat = re.search(r'latitude="\d+\.\d+', lat)
            obj_lat = obj_lat.group()
            obj_lat = re.search(r'\d+\.\d+', obj_lat)
            obj_lat = obj_lat.group()
            obj_lat = float(obj_lat)

            # obj_lng = float(obj_lng)
            lng = get_object.find_all(
                class_='search-list__link')
            lng = str(lng)
            obj_lng = re.search(r'longitude="\d+\.\d+', lng)
            obj_lng = obj_lng.group()
            obj_lng = re.search(r'\d+\.\d+', obj_lng)
            obj_lng = obj_lng.group()
            obj_lng = float(obj_lng)

            obj_adress = object_info.find_all(
                class_='search-list__row')[0].text
            obj_type_ = object_info.find_all(
                class_='search-list__row')[2].text
            obj_date = object_info_sales.find_all(
                class_='search-list__row')[2].text

            # rooms
            if len(object_info.find_all(class_='search-list__row')[1].text) == 1:
                break
            obj_rooms = object_info.find_all(class_='search-list__row')[1].text
            obj_rooms = re.search(r'^\d+', obj_rooms)
            obj_rooms = obj_rooms.group()
            obj_rooms = int(obj_rooms)

            # square meters
            obj_sq = object_info.find_all(class_='search-list__row')[1].text
            obj_sq = re.search(r'\d+\sm²', obj_sq)
            obj_sq = obj_sq.group()
            obj_sq = re.search(r'\d+', obj_sq)
            obj_sq = obj_sq.group()
            obj_sq = int(obj_sq)

            # price data
            obj_price = object_info_sales.find_all(
                class_='search-list__row')[0].text
            obj_price = obj_price.replace(' ', '')
            obj_price = re.search(r'\d+', obj_price)
            obj_price = obj_price.group()
            obj_price = int(obj_price)

            # price_sq data
            obj_price_sq = object_info_sales.find_all(
                class_='search-list__row')[1].text
            obj_price_sq = obj_price_sq.replace(' ', '')
            obj_price_sq = re.search(r'\d+', obj_price_sq)
            obj_price_sq = obj_price_sq.group()
            obj_price_sq = int(obj_price_sq)

            adress.append(obj_adress)
            sq_m.append(obj_sq)
            rooms.append(obj_rooms)
            type_.append(obj_type_)
            price.append(obj_price)
            price_sq.append(obj_price_sq)
            date.append(obj_date)
            bid_percent.append(obj_bid_percent)
            latitude.append(obj_lat)
            longitude.append(obj_lng)


    df = pd.DataFrame({'adress': adress,
                    'sq_m': sq_m,
                    'rooms': rooms,
                    'type_': type_,
                    'price': price,
                    'price_sq': price_sq,
                    'date': date,
                    'bid_percent': bid_percent,
                    'latitude': latitude,
                    'longitude': longitude})

    df['increase_price'] = np.where(df['bid_percent'].str.contains(r'^\-',regex=True), False, True)
    df['sq_m_rounded_small'] = 5*round(df['sq_m']/5)
    df['sq_m_rounded_large'] = 10*round(df['sq_m']/10)
    df['type'] = df['type_'].str.extract(r'(^\w+)')
    df['area'] = df['type_'].str.extract(r'(\w+$)')
    df['year'] = df['date'].str.extract(r'(\d{4}$)')
    df['month'] = df['date'].str.extract(r'(\D+)')
    df['day'] = df['date'].str.extract(r'(^\d{1,2})')

    df.drop('type_', axis=1, inplace=True)
    return df


city_urls = decide_city('stockholm', n=5)
df = create_df(city_urls = city_urls)

df
