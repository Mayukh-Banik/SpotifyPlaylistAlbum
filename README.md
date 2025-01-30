# SpotifyPlaylistAlbum

A python script that takes in a spotify playlist URL (you must have access to it, private playlists not tested)

and makes a json file of that playlist that contains Spotify Album URL, Name, and First Artist. 

Can use spot-dl https://github.com/spotDL/spotify-downloader to download the subsequent albums with a tracker to not download duplicates. Doesn't support resuming downloading of interrupted album downloads.


Get Spotify API from:
```
https://developer.spotify.com/
```

And then run:
```
pip install spotdl
python -m spotdl --download-ffmpeg
pip install spotipy
```

After cloning the repository, do:
```
python script.py -i CLIENT_ID -s CLIENT_SECRET
python script.py -p PLAYLIST_LINK -c
python script.py -p PLAYLIST_LINK -e
python script.py -p PLAYLIST_LINK -o "OUTPUT DIRECTORY" -l [# Albums to download at once keep it less than 100]
```
