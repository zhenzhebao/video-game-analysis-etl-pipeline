import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests

key=''
parent_platforms_PC=None
store_Steam=None
parent_platforms_base_url='https://api.rawg.io/api/platforms/lists/parents'
store_base_url='https://api.rawg.io/api/stores'

"""### Retriece the value for Parent platforms (PC)"""

params={'page':1,'page_size':3,'key':key}
parent_platforms_raw_response=requests.get(parent_platforms_base_url,params=params)

parent_platforms_response=parent_platforms_raw_response.json()

for item in parent_platforms_response['results']:
  if item['name']=='PC':
    #print(item)
    #print(item['name'])
    parent_platforms_PC=item['platforms'][0]['id']
  else:
    continue

"""### Retriece the value for Parent platforms (PC) and Store (Steam)"""

params={'key':key,'page':1,'page_size':2}
store_raw_response=requests.get(store_base_url,params=params)
store_response=store_raw_response.json()

for item in store_response['results']:
  if item['name']=='Steam':
    #print(item)
    store_Steam=item['id']
  else:
    continue

"""### Retrieve a list of games"""

params={'key':key,'page':1,'page_size':1,'parent_platforms':parent_platforms_PC,'stores':store_Steam,
        'dates':'2015-01-01,2025-12-31'}
list_of_games_raw_response=requests.get('https://api.rawg.io/api/games',params=params)

list_of_games_response=list_of_games_raw_response.json()

list_of_games_raw_response.status_code

for i in list_of_games_response.keys():
  if i=='results':
    #print(data[i][0])
    for key in list_of_games_response[i][0].keys():
      print(key)
  else:
    continue

for i in list_of_games_response.keys():
  if i=='results':
    print(list_of_games_response[i][0])
    for key in list_of_games_response[i][0].keys():
      print(key,list_of_games_response[i][0][key])
  else:
    continue

"""### Retrieve detailed information for one game"""

params={'key':key,'page':1,'page_size':1,'parent_platforms':parent_platforms_PC,'stores':store_Steam,
        'dates':'2015-01-01,2025-12-31'}
game=requests.get('https://api.rawg.io/api/games/3439',params=params)

for i in game.json().keys():
  print(i)
  print(game.json()[i])