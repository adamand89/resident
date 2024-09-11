import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def download_data(url):    
  # Skicka en GET-förfrågan till URL:en
  response = requests.get(url)
  response.raise_for_status()  # Kontrollera att förfrågan lyckades
  
  # Skapa en BeautifulSoup-objekt
  soup = BeautifulSoup(response.content, 'html.parser')
  
  prices = soup.find_all('span', class_='object-card__price')
  object = soup.find_all('span', class_='object-card__preamble')
  meta = soup.find_all(class_='object-card__data-list')
  date = soup.find_all('span', class_='object-card__date')
  street_adress = soup.find_all(class_="object-card__heading")


  street_adress = [str(tag) for tag in street_adress]
  date_strings = [str(tag) for tag in date]
  object_strings = [str(tag) for tag in object]
  meta_strings = [str(tag) for tag in meta]
  prices_strings = [str(tag) for tag in prices]
  
  return street_adress, prices_strings, meta_strings, object_strings, date_strings


def clean_prices(prices_strings):
  df = pd.DataFrame(prices_strings, columns=['raw_price'])
  df['Price'] = df['raw_price'].str.extract(r'>([\d\xa0]+)')[0].str.replace('\xa0', '').astype(int)
  df = df.drop(columns=['raw_price'])
  return df

def clean_adresses(street_adress):
  cleaned_adresses = []
  
  for i in range(0,len(adresses)):
      txt = adresses[i]
      txt = re.sub(r'^.+">', "", txt)
      txt = re.sub(r'<.+', "", txt)
      cleaned_adresses.append(txt)
  df = pd.DataFrame(cleaned_adresses, columns=['addresses'])
  return df

def clean_preambles(object_strings):
  df = pd.DataFrame(object_strings, columns=['raw_preamble'])
  df['Preamble'] = df['raw_preamble'].str.extract(r'preamble">(.*?)</span>')[0]
  df[['Type', 'Area', 'City']] = df['Preamble'].str.split(' · ', expand=True)
  df = df.drop(columns=['raw_preamble', 'Preamble'])
  return df

def clean_dates(date_strings):
  df = pd.DataFrame(date_strings, columns=['raw_date'])
  df['Date'] = df['raw_date'].str.extract(r'date">(.*?)</span>')[0]
  df['Date'] = pd.to_datetime(df['Date'])
  df = df.drop(columns=['raw_date'])
  return df

def clean_meta(meta_strings):
  def extract_data(html_string):
      soup = BeautifulSoup(html_string, 'html.parser')
      li_tags = soup.find_all('li')
      m2 = rum = van = kr_per_m2 = None
      for li in li_tags:
          text = li.get_text()
          if 'm²' in text:
              m2 = text.strip()
          elif 'rum' in text:
              rum = text.strip()
          elif 'vån' in text:
              van = text.strip()
      return m2, rum, van

  data_extracted = [extract_data(item) for item in meta_strings]
  df = pd.DataFrame(data_extracted, columns=['m²', 'rum', 'vån'])
  df['m²'] = df['m²'].str.replace('½', '.5').str.extract(r'(\d+\.?\d*)').fillna(0).astype(float).astype(int)
  df['rum'] = df['rum'].str.extract(r'(\d+)').fillna(0).astype(int)
  df['vån'] = df['vån'].str.extract(r'(\d+)').fillna(0).astype(int)
  return df



def extract_and_combine_data(street_adress,prices_strings, meta_strings, object_strings, date_strings):
  prices_df = clean_prices(prices_strings)
  preambles_df = clean_preambles(object_strings)
  dates_df = clean_dates(date_strings)
  meta_df = clean_meta(meta_strings)
  adress_df = clean_adresses(street_adress)
  
  combined_df = prices_df.join(preambles_df).join(dates_df).join(meta_df).join(adress_df)
  
  return combined_df

def generate_links(base_url, num_links):
    links = [base_url]
    for i in range(2, num_links + 1):
        links.append(f"{base_url}&page={i}")
    return links
