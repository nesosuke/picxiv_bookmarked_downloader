from datetime import datetime
import json
import os
import sys
import time

import pixivpy3
import metadata
with open('config.json', 'r') as f:
    config = json.load(f)
    refresh_token = config['refresh_token']
    getAll = config['getAll']
    user_id = config['user_id']
    save_to = config['save_to']
    pagecount = config['pagecount']
    max_bookmark_id = config['max_bookmark_id']

available_saveto = ['local']

if save_to not in available_saveto:
    sys.exit('invalid save_to')

api = pixivpy3.AppPixivAPI()
api.auth(refresh_token=refresh_token)

# save to local
if save_to == 'local':
    with open('config.json', 'r') as f:
        config = json.load(f)
        save_dir = config['save_dir']

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    db_path = save_dir+'/pixiv.sqlite'

elif save_to == 's3':
    pass  # TODO


# fetch faved illust ids
total_bookmarks = api.user_detail(
    user_id).profile['total_illust_bookmarks_public']

if getAll is True:
    count = total_bookmarks // 30 + 1  # 全取得用
else:
    count = pagecount  # 定期取得用

if max_bookmark_id == '0':
    max_bookmark_id = None
json_result = api.user_bookmarks_illust(
    user_id, max_bookmark_id=max_bookmark_id)

print(db_path)
next_qs = ""
while count > 0:
    api.auth(refresh_token=refresh_token)
    if getAll is False:
        print('left_page:', count)
    if next_qs != "":
        json_result = api.user_bookmarks_illust(**next_qs)
        print(next_qs['max_bookmark_id'])
    else:
        print(max_bookmark_id)

    favoritesillust_ids = []
    for illust in json_result['illusts']:
        favoritesillust_ids.append(illust['id'])

    # Download pics
    for item_id in favoritesillust_ids:
        item_data = api.illust_detail(item_id)

        illust = item_data.illust
        if illust is not None:
            metadata.meta_to_db(metadata=illust, db_path=db_path)

            creator_id = str(illust.user.account)+'_'
            if illust.type == 'illust':

                # イラストが1枚のときのDL
                if illust['page_count'] == 1:
                    original_url = illust.meta_single_page.original_image_url
                    api.download(original_url, path=save_dir,
                                 prefix=creator_id)
                    time.sleep(1)

                # イラストが複数枚あるときのDL
                elif illust['page_count'] > 1:
                    image_info = illust.meta_pages
                    for data in image_info:
                        original_url = data['image_urls']['original']
                        api.download(original_url, path=save_dir,
                                     prefix=creator_id)
                        time.sleep(1)

    next_url = json_result.next_url
    next_qs = api.parse_qs(next_url)

    count -= 1
    time.sleep(5)
print('finished.')
