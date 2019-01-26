# Qobuz-DL
Tool written in Python to download FLACs from Qobuz for Windows.   
Latest version: 26th Jan 19 - Release 2.

![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/1.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/2.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/3.jpg)

# Setup
## Mandatory ##
The following need to be inputted into the config file:
- App id
- App secret - you can get your app id & app secret by contacting Qobuz (you can also use the ones already in the config file).
- Email address
- Format id - download quality (5 = 320 kbps MP3, 6 = 16-bit FLAC, 7 = 24-bit / =< 96kHz FLAC, , 27 = best avail - 24-bit / >96 kHz =< 192 kHz FLAC)
- MD5 hashed password
- User auth token - input "uat" into the console to get this. App id + app secret is required.
- Naming scheme - file naming scheme (1 = "01. ", 2 = "01 -")
- Cover size - cover size to request from API (1 = 230x230, 2 = 600x600)
## Optional ##
- Comment tag 

You can specify what you want to be put into the comment field in your FLACs. Special characters will be escaped.

# Usage
It's simple; input Qobuz Player or Qobuz store URL. 
Ex. 
```
https://play.qobuz.com/album/hxyqb40xat3uc
https://www.qobuz.com/xxxx/album/mount-to-nothing-sangam/hxyqb40xat3uc
```
# Update Log
## 26th Jan 19 - Release 1 ##
## 27th Jan 19 - Release 2 ##
- Mp3 support
- Max downloadable tracks per album 50 -> 100.
- More efficient code for checking if file exists & deleting.
- Integrated Get UAT into main exe.
- implemented invalid URL input handling.
- Crash fixed when attempting to download albums with video goodies.
- Ability to choose naming scheme via config file.
- Ability to choose which size album cover to fetch.

# Misc Info
Tested on Python v3.6.7.  
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

The following tag fields are wrote to:
- album
- albumartist
- artist
- comment (depends on users' choice)
- title
- track
- tracktotal
- year

The tracktotal field won't be written to mp3s, instead, the track total will be written to the track field. Ex: (current_track)/(total_tracks) 

Misc:
- If a digital booklet is available, it will be downloaded and put in its respective album folder.
- Video goodies must be purchased. Qobuz-DL can't get them for you (API returns "None" when requesting).
- Downloaded tracks are put in the "Qobuz-DL Downloads" folder. Ex. (Qobuz-DL Dir)\\Qobuz-DL Downloads\\(albumartist) - (albumtitle)\\(tracks)
- Any specials characters that Windows doesn't support in filenames are replaced with "-" (except "<" & ">" for now).  
- If an album folder needs to be made, but already exists, it and its contents will be deleted.  
- If a track is unavailable for streaming because of right owner restrictions, it will be skipped (some record labels disallow streaming of their music).
- If the following files exists in the current working dir, they'll be deleted: (1-100).flac/.mp3, cover.jpg, booklet.pdf. This is to avoid any filename clashes. 

If you need to get in touch: Sorrow#5631

# To do
- **Increase max tracks downloadable per album. It's currently 50.**
- **MP3 support.**
- Fix known issues.
- More efficient way of increasing max tracks downloadable per album.
- Invalid URL input handling.
- Progress bar?
- Download playlists.
- Ability to choose which size album cover to fetch via config file.
- Ability to choose from "01. " and "01 -" file naming schemes via config fie.
- Implement Japanese translation.
- General code clean up.
- Integrate "Get UAT.exe" code into main exe.
- Commandline options.
- Download from list of urls.
- "<" & ">" handling in file names.
- Reduce size of executables (exclude libs etc.). 

# Known issues
- Crashing when trying to download albums with video goodies.

- Albums with more than one disks will be treated as single-disk albums.

To make this clearer, track 1 of disk 2 wouldn't be tagged as track #1, but as the track after the last track of disk 1.

- Printing languages like Chinese, Japanese & Korean to the console prints garbage instead.

This doesn't affect anything else in the code; FLACs containing any of the above languages will still download & tag correctly.
