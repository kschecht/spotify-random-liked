import random
import logging
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from argparse import ArgumentParser

# ====== CONFIG ======
parser = ArgumentParser()
parser.add_argument("-s", "--size", help="size of playlist", type=int, default=292)
parser.add_argument("-n", "--name", help="name of playlist", type=str, default="Random Liked Songs")
parser.add_argument("-r", "--refresh", help="refresh liked songs", type=bool, default=False)
args = parser.parse_args()

REDIRECT_URI = "http://127.0.0.1:8888/callback"
PLAYLIST_NAME = args.name
NUMBER_OF_SONGS = args.size
SHOULD_REFRESH = args.refresh
# =====================

# -------- Logging Setup --------
logging.basicConfig(
    level=logging.INFO,  # Change to INFO if too verbose
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)
# --------------------------------


def load_secret(filename):
    logger.debug(f"Loading secret from {filename}")
    with open(filename, "r") as file:
        return file.read().strip()


try:
    logger.info("Loading client credentials...")
    CLIENT_ID = load_secret("client_id.txt")
    CLIENT_SECRET = load_secret("client_secret.txt")

    scope = "user-library-read playlist-modify-private playlist-modify-public"

    logger.info("Initializing Spotify OAuth...")
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope,
        open_browser=True
    )

    logger.info("Creating Spotify client...")
    sp = spotipy.Spotify(auth_manager=auth_manager)

    logger.info("Fetching current user...")
    user = sp.current_user()
    user_id = user["id"]
    logger.info(f"Authenticated as user: {user_id}")

    # 1️⃣ Get all liked songs
    if SHOULD_REFRESH:
        logger.info("Fetching liked songs...")
        tracks = []
        results = sp.current_user_saved_tracks(limit=50)

        with open("track_ids.txt", 'a') as file:
            while results:
                tracks.extend(results['items'])
                for item in results['items']:
                    file.write(item['track']['id'] + '\n')
                logger.info(f"Fetched {len(tracks)} tracks so far...")
                if results['next']:
                    results = sp.next(results)
                else:
                    break

        logger.info(f"Total liked songs found: {len(tracks)}")

        track_ids = [track['track']['id'] for track in tracks]
    else:
        with open("D:\\DocumentsD\\Programming\\spotify\\liked_sample\\track_ids.txt") as file:
            track_ids = [line.rstrip() for line in file]
    
    # 2️⃣ Randomly select songs
    if NUMBER_OF_SONGS > len(track_ids):
        raise ValueError("Requested more songs than available liked tracks.")

    logger.info(f"Selecting {NUMBER_OF_SONGS} random tracks...")
    selected_track_ids = random.sample(track_ids, NUMBER_OF_SONGS)

    # 3️⃣ Create playlist
    logger.info("Creating playlist...")
    playlist = sp.user_playlist_create(
        user=user_id,
        name=PLAYLIST_NAME,
        public=False
    )

    logger.info("Adding tracks to playlist...")
    for i in range (0,len(selected_track_ids),50):
        sp.playlist_add_items(playlist['id'], selected_track_ids[i:i+50])

    logger.info("Playlist created successfully!")
    logger.info(f"Playlist URL: {playlist['external_urls']['spotify']}")

except Exception as e:
    logger.exception("An error occurred:")
