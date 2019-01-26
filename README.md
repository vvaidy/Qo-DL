# Qobuz-DL
Tool written in Python to download FLACs from Qobuz (even 24-bit!) for Windows.

# Setup
## Mandatory ##
The following need to be inputted into the config file (config.ini):
- App id
- App secret - you can get your app id & app secret by contacting Qobuz (you can also use the ones already in the config file).
- Email address
- Format id - download quality (6 = 16-bit FLAC, 7 = 24-bit / =< 96kHz FLAC, , 27 = best avail - 24-bit / >96 kHz =< 192 kHz FLAC)

**Format id 5 (MP3 320) is currently unsupported as I haven't finished the tagging side for it yet.**
- MD5 hashed password
- User auth token - Run "Get UAT.exe" to get this. App id + secret is required.
## Optional ####
- Comment tag

You can specify what you want to be put into the comment field in your FLACs. Special characters will be escaped.

# Usage
It's simple; input Qobuz Player or Qobuz store URL. 
Ex. 
```
https://play.qobuz.com/album/hxyqb40xat3uc,
https://www.qobuz.com/xxxx/album/mount-to-nothing-sangam/hxyqb40xat3uc
```
# Misc Info
Coded in Python. Tested on 3.6.7.
Used libraries:
- codecs
- configparser
- datetime
- glob
- hashlib
- mutagen
- os
- pathlib
- re
- requests
- shutil
- sys
- time
- urllib.request

# To do
- **Increase max tracks downloadable in an album. It is currently 50, and will crash if it goes over.**
- More efficient way of increasing max tracks downloadable in an album.
- Bad URL input handling.
- Progress bar?
- Download playlists.
- ability to choose which size album cover to fetch in config file.
- Implement Japanese translation.
- General code clean up.

# Known issues
- Albums with more than one disks will be treated as single-disk albums.

To make this clearer, track 1 of disk 2 wouldn't be tagged as track #1, but as the track after the last track of disk 1.

- Printing languages like Chinese, Japanese & Korean to the console prints garbage instead. 

This doesn't affect anything else in the code; FLACs containing any of the above languages will still download & tag correctly.
