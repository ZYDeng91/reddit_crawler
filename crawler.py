# Reddit's documentation about APIs
# https://www.reddit.com/dev/api

import requests
import json
import os
from datetime import datetime

# Capitalization does not matter in url
subreddit = 'offmychest'
# hot, new, top, controversial, rising
sort = 'hot'

start_time = datetime.now()

# Seems like reddit does not like someone crawling their website
# It will return 502 (Bad Gateway), but explanation is "Too Many Requests"

'''
# api url from web traffic
url = f'https://gateway.reddit.com/desktopapi/v1/subreddits/{subreddit}?sort={sort}'

res = requests.get(url)
print(res.text)
'''

# be polite and use APIs instead, unless...
from fake_useragent import UserAgent

FAKE_HEADERS = {'User-Agent': UserAgent().random}
url = f'https://gateway.reddit.com/desktopapi/v1/subreddits/{subreddit}?sort={sort}'

res = requests.get(url, headers=FAKE_HEADERS)
# print(res.body) # response has no body?
posts = json.loads(res.text)['posts']

output = []
for i in posts:
    output.append(posts[i]['title'])

output_text = '\n'.join(output)

# save
directory = 'data'
filename = 'output.txt'
metadata = {'subreddit': subreddit,
            'sort': sort,
            'time': str(start_time),
            'no_posts': len(output)
            }

if not os.path.exists(directory):
    os.makedirs(directory)

with open(directory + '/' + 'metadata.json', 'w') as file:
    file.write(json.dumps(metadata))

with open(directory + '/' + filename, 'w') as file:
    file.write(output_text)

