import opml
import json
import requests
import time
import sys
import os
from datetime import datetime
from base64 import b64encode


LASTCAST_API_URL = 'https://lastcast.fm/api/v1/scrobbles'

OVERCAST_CACHE_FILE = '.lastcast_scrobbler_overcast_export.xml'
LASTCAST_CACHE_FILE = '.lastcast_scrobbler_overcast_cache.txt'



# load episodes we already scrobbled earlier from cache

cached = []
if os.path.isfile(LASTCAST_CACHE_FILE):
    with open(LASTCAST_CACHE_FILE, "r") as cache_file:
        cached = [line.rstrip() for line in cache_file]


# log into Overcast account and download opml archive (max once every three hours)

refresh_overcast = True

if os.path.isfile(OVERCAST_CACHE_FILE):
    if os.path.getmtime(OVERCAST_CACHE_FILE ) > (time.time() - (3 * 3600)):
        refresh_overcast = False

if refresh_overcast:
    payload = {
        'email': sys.argv[1],
        'password': sys.argv[2]
    }

    with requests.Session() as s:
        p = s.post('https://overcast.fm/login', data=payload)
        r = s.get('https://overcast.fm/account/export_opml/extended')


    with open(OVERCAST_CACHE_FILE, 'w') as file:
        file.write(r.text)




# determine newly played episodes by comparing opml archive data and cache

new_plays = []

for item in opml.parse(OVERCAST_CACHE_FILE):
    if item.text == "feeds":
        for feed in item:
            for episode in feed:
                # episode is played
                if hasattr(episode, 'played') and episode.played == "1":
                    # and we didn't scrobble it earlier
                    if episode.enclosureUrl not in cached:
                        new_plays.append(episode)



# prepare data for scrobble API call

scrobble_payload = []
nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
for new_play in new_plays:
    scrobble_payload.append({'timestamp': nowtime, 'percentage': 100, 'matching_hints': {'episode_url': new_play.enclosureUrl}})

headers = {'Accept': 'application/json', 'Content-Type': 'application/json; charset=utf-8', 'Lastcast-Api-Token': 'ApiKey-v1 ' + sys.argv[3]}
payload = {'client': 'Lastcast for Mac (Overcast)', 'events': scrobble_payload}



# perform API call and parse response

response = requests.post(LASTCAST_API_URL, headers=headers, data=json.dumps(payload))
parsed_response = json.loads(response.text)



# save everything we don't need to scrobble again in local cache
# (either because newly created, 'success', or because already existed, 'existing')

successful_scrobbles = ''
with open(LASTCAST_CACHE_FILE, "a+") as cache_file:
    for scrobble in parsed_response['success'] + parsed_response['existing']:
        successful_scrobbles = successful_scrobbles + scrobble[0]['matching_hints']['episode_url'] + "\n"
    cache_file.write(successful_scrobbles)