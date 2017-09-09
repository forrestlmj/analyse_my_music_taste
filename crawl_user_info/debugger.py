import music163.lyric as ly
import music163.user_info as user


# song_id = "111"

# ly.get_lyric_text(song_id)
# user.get_user_playlist_info(82729523)


# search_list = ["风采无限的一只猫", "李胖胖034081", "joker199319"]
search_list = ["joker199319"]
my_user_list = []
for search_word in search_list:
    my_user = user.search_user(search_word)
    my_user_list.append(my_user)

# for user_id, user_name in my_user:
#     print(user_name)
#     user_playlist = user.get_user_playlist(user_id)

user_playlist = user.get_user_playlist(my_user['user_id'])

for single_user_playlist in user_playlist:
    info = user.get_user_playlist_info(single_user_playlist['playlist_id'])
