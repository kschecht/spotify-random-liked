**Has this ever happened to you?** *Probably not, but just in case you also meet these factors...*
- Have more than 10,000 liked songs on Spotify
- Mainly listen to music on a Chromecast device

Then you may have run into a problem where the Chromecast won't play your "Liked Songs" playlist because it's too long, and you rarely get to hear so many of the songs you've liked and forgotten about!

This solution gets around this limitation by allowing you to create new playlists with a smaller random selection of your liked tracks (at least until Spotify [removes](https://developer.spotify.com/blog/2026-02-06-update-on-developer-access-and-platform-security) the `user_playlist_create` functionality...)

## Setup
### Spotify app

1. Visit the [Spotify for Developers Dashboard](https://developer.spotify.com/dashboard)
1. Create app
1. Add the following `Redirect URIs`:
```
http://127.0.0.1:8888/callback
https://localhost:8080
```
1. Copy the `Client ID` and `Client Secret`

### Code

Add two new files containing the `Client ID` (`client_id.txt`) and `Client Secret` (`client_secret.txt`).

### Run

Run the `random_playlist.py` script with any of the following flags:
* `-r`: `True` or `False` (default), refresh list of liked songs (otherwise will use last cached list)
* `-n`: Specify a name for the playlist created
* `-s`: Number of random liked songs the playlist will contain
