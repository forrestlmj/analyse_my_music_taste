import requests
import json
import os
import logging
from datetime import datetime
# Request 163 web api,get response in json , so just draw useful info like user name,playlist name into another json.
# Every function return is a dict data structure,so the caller can json dump it.

# s: 搜索词
# limit: 返回数量
# sub: 意义不明(非必须参数)；取值：false
# type:
#    1 单曲
#    10 专辑
#    100 歌手
#    1000 歌单
#    1002 用户

headers = {"Content-type": "application/x-www-form-urlencoded",
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'User-Agent': "Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Connection": "close",
           "Cache-Control": "no-cache"}
RETURN_MAX_LIMIT = 10000


def get_user_playlist_info(playlist_id):
    # return song_id and song_name

    url = "http://music.163.com/api/playlist/detail"
    req = requests.get(url, params={'id': str(playlist_id)})
    context = req.json()
    logging.info("返回结果:"+str(context['code']))
    playlist_info = []
    for track in context['result']['tracks']:
        # artist just crawl the first one
        track_info = {'song_name': track['name'], 'song_id': track['id'], 'artist': track['artists'][0]['name']}
        playlist_info.append(track_info)
    return playlist_info


def get_user_playlist(user_id):
    # return playlist_id and playlist_name
    url = "http://music.163.com/api/user/playlist"
    req = requests.get(url, params={'uid': user_id, 'offset': 0, 'limit': RETURN_MAX_LIMIT})
    context = req.json()
    user_playlist_list = []
    for my_dict in context['playlist']:
        user_playlist = {'playlist_id': my_dict['id'], 'playlist_name': my_dict['name']}
        logging.info(str(user_playlist))
        user_playlist_list.append(user_playlist)
    return user_playlist_list


def search_user(search_word):
    # return 1 result:user_id and user_name
    url = "http://music.163.com/api/search/get/"
    req = requests.post(url, data={'s': search_word, 'limit': 1, 'type': 1002})
    context = req.json()
    logging.info("返回结果:"+str(context['code']))
    user_id = context['result']['userprofiles'][0]['userId']
    user_name = context['result']['userprofiles'][0]['nickname']
    search_result = {'user_id': user_id, 'user_name': user_name}
    logging.info(str(search_result))
    return search_result


def write_json(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(content, f)
    return


def check_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dir_name


def get_user_info(search_word='joker199319'):
    result = {}
    try:
        user_info = search_user(search_word)
        user_playlist = get_user_playlist(user_info['user_id'])
        for single_user_playlist in user_playlist:
            info = get_user_playlist_info(single_user_playlist['playlist_id'])
            logging.info("Playlist \""+str(single_user_playlist)+"\" done.")
            file = check_dir(str(user_info['user_name']))+'//'+single_user_playlist['playlist_name'].replace('/', '')\
                   +'_'+str(single_user_playlist['playlist_id'])
            write_json(file, info)
            logging.info("Playlist \""+str(single_user_playlist)+"\"write into \""+file+"\" done.")
        return result
    except Exception as e:
        # print(traceback.print_exception(e))
        logging.error(e)


def main():

    user_info=get_user_info()
    # write_json(str(user_info['user_info']['user_name'])+'.txt', user_info)
    return


if __name__ == "__main__":

    logging.basicConfig(filename=check_dir("log")+'//'+str(datetime.now().date())+'.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s:%(lineno)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logging.info("# ####### start #######")
    main()
    logging.info("# ####### end #######")