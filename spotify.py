import json
import re
import sys
import subprocess
import spotipy
import urllib.parse
import urllib.request
from os.path import expanduser
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import oauth2 as spotify_web_oauth
import spotipy.util as util

client_id ='239f993e90b54895a1faebc8b6b2f485'
client_secret ='e70808aa36e540c6b0dc545fbe4e5768'
# redirect_uri ='http://listparser.com/callback'
username = 'd.flucas'
# username = '12144157524'
list_ = '4Kls4WcczUw0Fj5XAx4Jbp'


# list_ = '1UmF20zPbew2OHOiZfWwUA'

# uri = 'spotify:user:spotify:playlist:5ILSWr90l2Bgk89xuhsysy'
# spotify:user:d.flucas:playlist:4Kls4WcczUw0Fj5XAx4Jbp



def runCMD(cmd, timeout=1):
    print ('CMD:', str(cmd))
    return str(subprocess.run(cmd, stdout=subprocess.PIPE))



def show_tracks(results, playlist):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        track_name = track['name']
        artist = track['artists'][0]['name']
        show_youtube_url(track_name, playlist, artist)
        print("%d %2.32s / %s" % (i, artist, track_name))


def show_youtube_url(track, playlist, artist):
    full_search = track + ' ' + artist + ' audio'
    print(full_search)
    query_string = urllib.parse.urlencode({"search_query": full_search})
    print(query_string)
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    print(html_content)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    print(search_results)
    url = "http://www.youtube.com/watch?v=" + search_results[0]
    print(url)
    download_audio_from_youtube(url, track, playlist, artist)
    print("http://www.youtube.com/watch?v=" + search_results[0])


def download_audio_from_youtube(url, track, playlist, artist):
    home = expanduser('~\Desktop')
    path = home + '\\' + playlist.replace(' ', '_')
    print(path)
    artist_ = str(artist).replace(' ', '_').replace('/', '_')
    track_ = str(track).replace(' ', '_').replace('/', '_')
    print(artist_, track_)
    command = "youtube-dl --newline --no-post-overwrites --no-playlist -x --audio-format mp3 --audio-quality 0 -o "
    cmd = command + path + "\\" + track_ + "_" + artist_ + ".%(ext)s " + url

    runCMD(cmd, 3)


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     uri = sys.argv[1]
    # else:
    #     print ("Whoops, need your username!")
    #     print ("usage: python user_playlists.py [URI]")
    #     sys.exit()
    # print ("Parsing: " + uri)
    #
    # playlist_re = re.compile("spotify:user:[\w]+:playlist:[\w]+")
    # for playlist_uri in playlist_re.findall(uri):
    #     segments = playlist_uri.split(":")
    #     user_id = segments[2]
    #     playlist_id = segments[4]
    #
    #     playlist = sp.user_playlist(user_id, playlist_id)
    #
    #     scope = " ".join([
    #         "playlist-read-private",
    #         "playlist-read-collaborative",
    #     ])
    # with open("client_secret_key.json") as creditials:
    #     pass

    token = SpotifyClientCredentials(client_id, client_secret)
    print(token)
    if token:
        sp = spotipy.Spotify(client_credentials_manager=token)
        playlist = sp.user_playlist(username,list_,fields="tracks, next, name")
        tracks = playlist['tracks']
        name_playlist = playlist['name']
        print('Playlist: ' + name_playlist)
        show_tracks(tracks, name_playlist)
        while tracks['next']:
            tracks = sp.next(tracks)
            show_tracks(tracks, name_playlist)
    else:
        print ("Can't get token for", username)