import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv("apikey")
if apikey is None:
    raise Exception("API KEY was not found.")

parent_platforms_PC=None
store_Steam=None
parent_platforms_base_url='https://api.rawg.io/api/platforms/lists/parents'
store_base_url='https://api.rawg.io/api/stores'
game_base_url='https://api.rawg.io/api/games'
max_attempts=3
timeout=30

def retrieve_data(base_url,params,timeout):
  attempt=0
  while attempt<=max_attempts:
    print(f'Run {attempt+1}, Retry Attempt {attempt}')
    try:
      response=requests.get(base_url,params=params,timeout=timeout)
    except requests.Timeout:
        time.sleep(2)
        attempt=attempt+1
        continue
    except requests.RequestException:
      attempt=attempt+1
      print('An error occurred')
      raise
    print('Data Retrieved Successfully')
    return response
  raise Exception ('The request timed out after all retry attempts failed')

def return_data_check(response,required_info):
    if response.status_code==200:
       response_dict=response.json()

       if required_info not in response_dict.keys():
          raise Exception ('Invalid return data format: required information is missing.')
       else:
          print('Return Data Check Passed')
          return response_dict
    else:
       raise Exception('Returned data is invalid')

def return_data_extract(response_dict,required_info,look_up_key,look_up_value,retrieve_value_key):
    result=None
    for item in response_dict[required_info]:
        if look_up_key not in item.keys() or retrieve_value_key not in item.keys():
           raise Exception (f'Invalid return data format: required information {look_up_key} or {retrieve_value_key} is missing.')
        else:
           if item[look_up_key]==look_up_value:
              result=item[retrieve_value_key]
              break
    if result is None:
       raise Exception(f'Value for {retrieve_value_key} is not available')
    else:
       print('Value is Good')
       return result

"""### Retriece the value for Parent platforms (PC)"""

params={'page':1,'key':apikey}

response=retrieve_data(parent_platforms_base_url,params,timeout)
response_dict=return_data_check(response,'results')
parent_platforms_PC=return_data_extract(response_dict,'results','name','PC','id')
parent_platforms_PC

"""### Retriece the value for Store (Steam)"""

params={'page':1,'key':apikey}

response=retrieve_data(store_base_url,params,timeout)
response_dict=return_data_check(response,'results')
store_Steam=return_data_extract(response_dict,'results','name','Steam','id')
store_Steam

"""### Getting total number of records"""

params={'key':apikey,'page':1,'parent_platforms':parent_platforms_PC,'stores':store_Steam,
        'dates':'2025-01-01,2025-12-31','page_size':1}

response=retrieve_data(game_base_url,params,timeout)
response_dict=return_data_check(response,'count')
total_count=response_dict['count']
total_count

### Retriece the value for Parent platforms (PC)
# attempt=0
# params={'page':1,'key':apikey}

# while attempt<=max_attempts:
#   print(f'Run {attempt+1}, Retry attempt {attempt}')
#   try:
#     parent_platforms_raw_response=requests.get(parent_platforms_base_url,params=params,timeout=timeout)
#   except requests.Timeout:
#       time.sleep(2)
#       attempt=attempt+1
#       continue
#   except requests.RequestException:
#     attempt=attempt+1
#     print('There is an Error')
#     raise

#   if parent_platforms_raw_response.status_code==200:
#     #print('This line runs')
#      parent_platforms_response=parent_platforms_raw_response.json()
#      try:
#         for item in parent_platforms_response['results']:
#             if item['name']=='PC':
#                 #print(item)
#                 #print(item['name'])
#                  parent_platforms_PC=item['id']
#                  break
#         if parent_platforms_PC is None:
#             raise Exception('ID for PC platform is not available')
#         else:
#           #print('Value is Good')
#           attempt=attempt+1
#           break
#      except KeyError:
#        raise Exception('Invalid Return Data Format')
#   else:
#     raise Exception('Return Data is not valid')

### Retriece the value for Store (Steam)
# attempt=0
# params={'key':apikey,'page':1}

# while attempt<=max_attempts:
#   print(f'Rum {attempt +1}, Retry attempt {attempt}')
#   try:
#     store_raw_response=requests.get(store_base_url,params=params,timeout=timeout)
#   except requests.Timeout:
#     print('Timeout')
#     time.sleep(2)
#     attempt=attempt+1
#     continue
#   except requests.RequestException:
#     attempt=attempt+1
#     print('There is an error')
#     raise

#   if store_raw_response.status_code==200:
#     store_response=store_raw_response.json()

#     try:
#       response_result=store_response['results']
#     except KeyError:
#       raise Exception('Invalid Return Data Format')

#     for item in response_result:
#       if 'name' not in item.keys() or 'id' not in item.keys() :
#         raise Exception ('Invalid return data format')
#       elif item['name']=='Steam':
#         #print(item)
#         store_Steam=item['id']
#         break
#     if store_Steam is None:
#       raise Exception('ID for Steam Store is not available')
#     else:
#       #print('Data is good ')
#       attempt=attempt+1
#       break
#   else:
#     raise Exception('Return Data is not valid')

### Getting total number of records
# attempt=0
# params={'key':apikey,'page':1,'parent_platforms':parent_platforms_PC,'stores':store_Steam,
#         'dates':'2025-01-01,2025-12-31','page_size':1}

# while attempt<=max_attempts:
#   print(f'Run {attempt+1}, Rerun attempt {attempt}')
#   try:
#     total_count_response=requests.get(game_base_url,params=params,timeout=timeout)
#   except requests.Timeout:
#     print('TimeOut')
#     time.sleep(2)
#     attempt=attempt+1
#     continue
#   except requests.RequestException:
#       attempt=attempt+1
#       print('There is an error')
#       raise
#   attempt=attempt+1
#   break

# if total_count_response.status_code==200:
#   total_count_dict=total_count_response.json()

#   if 'count' not in total_count_dict.keys():
#     raise Exception('Return Data is not valid')
#   else:
#     total_count=total_count_dict['count']
# else:
#   raise Exception('Return Data is not valid')

"""### Retrieve a list of games"""

next_url=None
return_data=[]
dates=['2025-01-01,2025-03-31','2025-04-01,2025-06-30','2025-07-01,2025-09-30','2025-10-01,2025-12-31']

for date in dates:
  params={'key':apikey,'page':1,'page_size':40,'parent_platforms':parent_platforms_PC,'stores':store_Steam,
          'dates':date}
  attempt=0
  get_first_page=False
  while attempt<=max_attempts:
    print(f'Getting first page data Run {attempt+1}, Rerun attempt {attempt}')
    try:
      list_of_games_raw_response=requests.get(game_base_url,params=params,timeout=timeout)
    except requests.Timeout:
      print('TimeOut')
      time.sleep(2)
      attempt=attempt+1
      continue
    except requests.RequestException:
      attempt=attempt+1
      print('There is an error')
      raise
    attempt=attempt+1
    get_first_page=True
    break

  if get_first_page==False:
     raise Exception ('Failed to retrieve first page data')
  else:
    if list_of_games_raw_response.status_code==200:
      list_of_games_response=list_of_games_raw_response.json()
    else:
      raise Exception('Return Data is not valid')

    if 'results' not in list_of_games_response.keys() or 'next' not in list_of_games_response.keys():
      raise Exception('Return Data is not valid')

    else:
      return_data.extend(list_of_games_response['results'])
      next_url=list_of_games_response['next']

    while next_url is not None:
      attempt=0
      get_next_page=False
      while attempt<=max_attempts:
        print(f'Retrieve next page data Run {attempt+1}, Rerun attempt {attempt}')
        try:
          response=requests.get(next_url,timeout=timeout)
        except requests.Timeout:
          print('TimeOut')
          time.sleep(2)
          attempt=attempt+1
          continue
        except requests.RequestException:
          attempt=attempt+1
          print('There is an error')
          raise
        attempt=attempt+1
        get_next_page=True
        break

      if get_next_page==False:
         raise Exception ('Failed to retrieve next page data')
      else:
        if response.status_code==200:
          response_dict=response.json()
        else:
          raise Exception('Return Data is not valid')
        if 'results' not in response_dict.keys() or 'next' not in response_dict.keys():
          raise Exception('Return Data is not valid')
        else:
          return_data.extend(response_dict['results'])
          next_url=response_dict['next']
          print(len(return_data))
          if len(return_data)<5000:
              time.sleep(4)
          elif len(return_data)==5000:
              time.sleep(60)
          elif len(return_data)<10000:
              time.sleep(8)
          elif len(return_data)==10000:
              time.sleep(60)
          elif len(return_data)<12500:
              time.sleep(12)
          elif len(return_data)==12500:
              time.sleep(120)
          elif len(return_data)<15000:
              time.sleep(16)
          elif len(return_data)==15000:
              time.sleep(120)
          else:
              time.sleep(20)

if total_count==len(return_data):
  print('Data is complete')
else:
  raise Exception('Data is incomplete')

"""## Drop irrelevant columns, change data type"""

df=pd.DataFrame(return_data)
#print(df.columns)
skip_columns=['community_rating','slug','platforms', 'stores','tba','background_image','ratings_count','reviews_text_count',
              'added','metacritic','suggestions_count','score', 'clip','tags','esrb_rating','user_game', 'reviews_count',
              'saturated_color','dominant_color','short_screenshots','parent_platforms']

data=df.drop(columns=skip_columns)
data.head()

#print(data.info())
data["released"] = pd.to_datetime(data["released"])
data["updated"] = pd.to_datetime(data["updated"])
#print(data.info())

"""## Prepare Data Frame

### Game
"""

game=data[['id','name','playtime','released','updated','rating','rating_top']]
#game

"""### Game_added_Status"""

columns=[]
for item in return_data:
  if item['added_by_status'] is not None:
    for i in item['added_by_status'].keys():
      columns.append(i)
    break
  else:
    continue
print(columns)

for item in return_data:
  if item['added_by_status'] is not None:
    #print(item['added_by_status'])
    for i in item['added_by_status'].keys():
      #print(i)
      if i not in columns:
        print(item['added_by_status'].keys())
        columns.append(i)
print('done')

empty_value=[]
count=1
while count<=len(columns):
  empty_value.append(None)
  count=count+1
rows=[]

for item in return_data:
  row=[]
  if item['added_by_status'] is None:
    #print(item['id'])
    row.append(item['id'])
    row.extend(empty_value)
    rows.append(row)
  else:
    #print('+++++++++++++++++++++++++')
    #print(item['added_by_status'])
    row.append(item['id'])
    for i in columns:
     try:
      #print(i)
      #print(item['added_by_status'][i])
      row.append(item['added_by_status'][i])
     except KeyError:
      #print('No key')
      row.append(None)
    rows.append(row)

game_added_status_column=['id']
game_added_status_column.extend(columns)
print(game_added_status_column)
game_added_status=pd.DataFrame(rows,columns=game_added_status_column)
#game_added_status

"""### rating Category"""

rating_category=[]
for item in return_data:
  if len(item['ratings'])>0:
   for i in item['ratings']:
    #print(i)
    #print(i['title'])
    if i['title'] not in rating_category:
      rating_category.append(i['title'])
    else:
      continue
print(rating_category)

rows=[]
empty_value={}
for i in rating_category:
  empty_value.update({i:None})

for item in return_data:
  if len(item['ratings'])==0:
    #print(item['id'])
     row=empty_value.copy()
     row.update({'id':item['id']})
     rows.append(row)
  else:
    row={}
    row.update({'id':item['id']})
    for i in item['ratings']:
      #print(i['title'],i['count'])
      row.update({i['title']:i['count']})
    for i in rating_category:
      if i not in row.keys():
        row.update({i:None})
    rows.append(row)

rating_category=pd.DataFrame(rows)
#rating_category

"""### Genres"""

genres=[]
for item in return_data:
  #print(item)
  if len(item['genres'])>0:
    for i in item['genres']:
      #print(i)
      #print(i['name'])
      if i['name'] not in genres:
        genres.append(i['name'])
      else:
        continue
  else:
    continue

print(genres)
rows=[]
empty_genres={}
for i in genres:
  empty_genres.update({i:None})

for item in return_data:
  if len(item['genres'])==0:
    row=empty_genres.copy()
    row.update({'id':item['id']})
    rows.append(row)
  else:
    row={}
    row.update({'id':item['id']})
    for i in (item['genres']):
      #print(i)
      row.update({i['name']:'Yes'})
    for i in genres:
      if i not in row.keys():
        row.update({i:None})
    rows.append(row)

game_genres=pd.DataFrame(rows)
#game_genres

"""## Merge All Data Frames,remove Duplicates, rename column name"""

result = (game
          .merge(game_added_status,on="id",how="inner")
          .merge(rating_category,on="id",how="inner")
          .merge(game_genres,on="id",how="inner")
          )

#print(result.info())
result.drop_duplicates(inplace=True)
#print(result.info())

result.rename(columns={'id':'game_id',
                       'yet':'added_by_status_yet',
                       'owned':'added_by_status_owned',
                       'beaten':'added_by_status_beaten',
                       'toplay':'added_by_status_toplay',
                       'dropped':'added_by_status_dropped',
                       'playing':'added_by_status_playing',
                       'exceptional':'rating_exceptional',
                       'recommended':'rating_recommended',
                       'skip':'rating_skip',
                       'meh':'rating_meh'},inplace=True)

"""### Create Game Table"""

game=result[['game_id','name','playtime','released','updated','rating','rating_top',
             'added_by_status_yet','added_by_status_owned','added_by_status_beaten','added_by_status_toplay','added_by_status_dropped',
             'added_by_status_playing','rating_exceptional','rating_recommended','rating_skip','rating_meh']]
game.to_csv('game.csv',index=False)

"""### Create Genre Table"""

genres=[]
genre_id=1
for i in game_genres.columns:
  value={}
  if i=='id':
    continue
  else:
    value.update({'genre_id':genre_id})
    value.update({'genre':i})
    genres.append(value)
    genre_id=genre_id+1

genres_table=pd.DataFrame(genres)
genres_table.to_csv('genres_table.csv',index=False)

"""### Create Game Genre Table"""

games_genres_list=[]
for i in game_genres.columns:
  if i=='id':
    continue
  else:
    #print(i)
    for genre in genres:
      if genre['genre']==i:
        #print(genre['genre_id'])
        genre_id=genre['genre_id']
        break
    tmp=result[['game_id',i]].copy()
    tmp.dropna(inplace=True)
    tmp['genre_id']=genre_id
    games_genres_list.append(tmp)
game_genres_table = pd.concat(games_genres_list, ignore_index=True)

game_genres_table=game_genres_table[['game_id','genre_id']]
game_genres_table = game_genres_table.reset_index(names='game_genre_id')
game_genres_table.to_csv('game_genres_table.csv',index=False)
game_genres_table