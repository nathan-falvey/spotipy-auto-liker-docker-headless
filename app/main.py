import spotipy, sys, os, time
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_USERNAME = os.environ.get("SPOTIPY_APP_USER")
SPOTIFY_SECRET = os.environ.get("SPOTIFY_APP_SECRET")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIFY_APP_URI_REDIRECT")
SPOTIFY_AUTO_LIKER_PERCENT = int(os.environ.get("AUTO_LIKER_MINIMUM_PERCENT", 90))
SCOPE = 'user-read-playback-state,user-library-read,user-library-modify'


def like_song(id):
    results = sp.current_user_saved_tracks_contains(tracks=[id])
    if results == [False]:
        sp.current_user_saved_tracks_add(tracks=[id])
        print(f"Liked {id}.")
        return True
    else:
        return False

def has_active_device():
    devices = sp.devices()
    for device in devices['devices']:
        if device['is_active']:
            return True
    return False

def main():
    try:
        while True:
            if has_active_device():
                current = sp.current_playback(market=None, additional_types=None)
                if current['currently_playing_type'] == 'track' and current['is_playing'] == True:
                    required_ms = current['item']['duration_ms'] * (SPOTIFY_AUTO_LIKER_PERCENT / 100)
                    if current['progress_ms'] > required_ms:
                        id = current['item']['id']
                        like_song(id)
                time.sleep(3)
            else:
                time.sleep(5)
    except KeyboardInterrupt as e:
        print("Loop cancelled by user, exiting...")
    finally:
        exception_info = sys.exc_info()
        if exception_info[0] != None:
            print(exception_info[0])
            print(exception_info[1])
            raise exception_info[2]

if __name__ == "__main__":
    
    print("Trying to do a test log in...")
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_USERNAME,client_secret=SPOTIFY_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI,scope=SCOPE,open_browser=False))
        username = sp.me()['display_name'] # gathers the display username from the provided credentials which is currently logged in
        print("Logged in successful.")
        print(f"Logged in as {username}. Iniating script loop....")
        main()
    except Exception as er:
        raise er