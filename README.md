# Qobuz-DL
Tool written in Python to download FLACs from Qobuz for Windows.   
26th Jan 19 - Release 1.

![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/1.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/2.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/3.jpg)

# Setup
## Mandatory ##
The following need to be inputted into the config file:
- App id
- App secret - you can get your app id & app secret by contacting Qobuz (you can also use the ones already in the config file).
- Email address
- Format id - download quality (6 = 16-bit FLAC, 7 = 24-bit / =< 96kHz FLAC, , 27 = best avail - 24-bit / >96 kHz =< 192 kHz FLAC)

**Format id 5 (MP3 320) is currently unsupported as I haven't finished the tagging side for it yet.**
- MD5 hashed password
- User auth token - Run "Get UAT.exe" to get this. App id + secret is required.
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

Misc:
- The largest available size album covers are wrote (600x600).  
- If a digital booklet is available, it will be downloaded and put in its respective album folder.  
- Downloaded FLACs are put in the "Qobuz-DL Downloads" folder. Ex. (Qobuz-DL Dir)\\Qobuz-DL Downloads\\(albumartist( - (albumtitle)\\FLACs
- Any specials characters that Windows doesn't support in filenames are replaced with "-" (except "<" & ">" for now).  
- If an album folder needs to be made, but already exists, it and its contents will be deleted.  
- If a track is unavailable for streaming because of right owner restrictions, it will be skipped (some record labels disallow streaming of their music).  

If you need to get in touch: Sorrow#5631

# To do
- **Increase max tracks downloadable per album. It's currently 50.**
- **MP3 support.**
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
- Albums with more than one disks will be treated as single-disk albums.

To make this clearer, track 1 of disk 2 wouldn't be tagged as track #1, but as the track after the last track of disk 1.

- Printing languages like Chinese, Japanese & Korean to the console prints garbage instead.

This doesn't affect anything else in the code; FLACs containing any of the above languages will still download & tag correctly.
