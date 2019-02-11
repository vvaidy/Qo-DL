# Qobuz-DL
Tool written in Python to download MP3s & FLACs from Qobuz for Windows & Linux (Ubuntu x64 only for now).

Latest versions:    
Qobuz DL: 11th Feb 19 - Release 4    
Qobuz DL Playlist: 11th Feb 19 - Release 4   

![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/1.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/2.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/3.jpg)

# Setup
## Mandatory ##
The following need to be inputted into the config file:
- App id
- App secret - you can get your app id & app secret by contacting Qobuz (you can also use the ones already in the config file).
- Email address
- Format id - download quality (5 = 320 kbps MP3, 6 = 16-bit FLAC, 7 = 24-bit / =< 96kHz FLAC, 27 = best avail - 24-bit / >96 kHz =< 192 kHz FLAC).
- MD5 hashed password
- User auth token - you'll be given this automatically if it's not already inputted in. App id & app secret are required.
- Naming scheme - file naming scheme (1 = "01. ", 2 = "01 -").
- Cover size - cover size to request from API (1 = 230x230, 2 = 600x600).
- Tag_swap1 - FLAC only, write to TRACKNUMBER instead of TRACK, Y or N
- Tag_swap2 - FLAC only, write to DATE instead of YEAR, Y or N 

**You can't download ANY tracks with a free account.**
## Optional ##
- Comment tag 

You can specify what you want to be put into the comment field in your tracks. Special characters will be escaped.

# Usage
It's simple; input Qobuz Player or Qobuz store URL. 
Ex. 
```
https://play.qobuz.com/album/hxyqb40xat3uc
https://www.qobuz.com/xxxx/album/mount-to-nothing-sangam/hxyqb40xat3uc

```
Qobuz-DL can also be used via command line. Pass the URL to it. 
Ex:
```
Qobuz-DL_x64.exe https://play.qobuz.com/album/hxyqb40xat3uc
 ./Qobuz-DL https://play.qobuz.com/album/hxyqb40xat3uc

```
# Update Log
## Qobuz-DL ##
### 26th Jan 19 - Release 1 ###
### 27th Jan 19 - Release 2 ###
- Mp3 support.
- metaflac is no longer needed. Mutagen handles tagging for both MP3s and FLACs.
- Max downloadable tracks per album 50 -> 100.
- More efficient code for checking if files exists & deleting them if they do. 
- Integrated Get UAT into main exe.
- implemented invalid URL input handling.
- Crash fixed when attempting to download albums with video goodies.
- Ability to choose naming scheme via config file.
- Ability to choose which size album cover to fetch via config file.
### 27th Jan 19 - Release 2a ###
- Check for empty user_auth_token field would prevent users from getting to the url input screen, thus not allowing them to get the uat.
### 28th Jan 19 - Release 3 ###
- Unlimited tracks downloadable per album.
- Code clean up - 1800 lines down to 400! Mainly thanks to the above.
- "<" & ">" handled in file names.
- uat input removed - you'll be given your uat automatically now if it's needed.
### 28th Jan 19 - Release 3a ###
- Handled the below. This happens when you try to download tracks using a free account. You can't.
```
TypeError: 'NoneType' object is not subsciptable Failed to execute script Qobuz-DL
```
### 29th Jan 19 - Release 3b ###
- Download from list or URLs - put your urls inside a text file named "list.txt" in the current working dir (one per line), then load up Qobuz-DL and input "list" into the console.
- Fixed crash which would happen if you were to download the same album again already with booklet.pdf inside of it.
- Improved code of checking if files exist and deleting them if they do. 
### 31st Jan 19 - Release 3c ###
Nothing major.
- x86 binary added.
- Put back in the accidentally removed line that prints "(album artist) - (album title)" at the top of the console while downloading albums.
### 7th Feb 19 - Release 3d ###
- x64 Linux version added. I'm very inexperienced with it, so I apologize if it doesn't work on your distro. Tested working on Ubuntu 18.10 x64. EDIT: put up a fixed version.
- Command line support. Pass a URL.
This is the only option for now. Passing "list" probably won't work. It will exit upon finishing.
- Better code to strip special characters for Windows filenames.
- ">" wasn't being stripped in filenames. Fixed.
- New field 'Tag_swap1' in config file - write to TRACKNUMBER instead of TRACK, Y or N.
- New field 'Tag_swap2' in config file  - write to DATE instead of YEAR, Y or N.
This only works for FLACs due to ID3 limitations. Not very tested. Metaflac can pick up the two new tags, but Mp3tag can't.
- Handled the below. This happens when the API returns 'None' when requesting the release year for albums. 'xxxx' will be used instead. I'm not sure why the API would do this. It's not album specific, and only seems to hit a small percentage of users.
```
OSError: [Errno 22] Invalid argument [2084] Failed to execute script Qobuz-DL
```
- Handled the below. This happens when the API's album response doesn't conatin a performer key. Album specific. "performer**s**" will be used as a fallback.
```
KeyError: 'performer' [12992] Failed to execute script Qobuz-DL
```
### 11th Feb 19 - Release 4 ###
- Download playlists using separate exe.

**You can't use Qobuz-DL_xxx.exe to download playlists. I haven't merged the playlist code into the main exe yet, so you have to use Qobuz-DL_Playlist_xxx.exe for now.**
- Download progress bar.
- New field 'Move_to' in config file  - specify where to move album folder after downloading, "" = default.
- New field 'Keep_cover' in config file  - leave folder.jpg in album dir, Y or N. Not usable with Qobuz-DL_Playlist.
- Better way of checking if track is restricted by right holders. The previous method would crash and allow the below to happen:
```
KeyError: 'url' [12992] Failed to execute script Qobuz-DL
```

## Qobuz-DL Playlist ##
### 11th Feb 19 - Release 1 ###

# Misc Info
Written around Python v3.6.7.  
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
- date (depends on users' choice)
- comment (depends on users' choice)
- title
- track (depends on users' choice)
- tracknumber (depends on users' choice) 
- tracktotal
- year (depends on users' choice)

The tracktotal field won't be written to mp3s. Instead, the track total will be written to the track field. Ex: (current_track)/(total_tracks). The date & tracknumber field can only be written to FLACs.  

Misc:
- If a digital booklet is available, it will be downloaded and put in its respective album folder.
- Video goodies must be purchased. Qobuz-DL can't get them for you (API returns "None" when requesting).
- Downloaded tracks are put in the "Qobuz-DL Downloads" folder. Ex. (Qobuz-DL Dir)\\Qobuz-DL Downloads\\(albumartist) - (albumtitle)\\(tracks)
- Any specials characters that Windows doesn't support in filenames are replaced with "-".  
- If an album folder needs to be made, but already exists, it and its contents will be deleted.  
- If a track is unavailable for streaming because of right owner restrictions, it will be skipped (some record labels disallow streaming of their music).
- ID3v2.4 tag format is used for mp3 tags.
- **If the following files exist in the current working dir, they'll be deleted: (1-1000).flac/.mp3, cover.jpg, booklet.pdf. This is to avoid any filename clashes. Filename clashes are also handled inside of album folders.**

If you need to get in touch: Sorrow#5631
# To Do
- GUI version.
- Fix known issues.
- Progress bar?
- Download playlists.
- Implement Japanese translation.
- General code clean up.
- More command line options.
- Reduce size of executable (exclude libs etc.).
- Add a check to see if the user has inputted a plain password into the config file instead of an MD5 hashed one.
- Apparently the x86 binary isn't working. Look into that. Update: tested working on Win 10 1809 x86.

# Known Issues
- Albums with more than one disks will be treated as single-disk albums.

To make this clearer, track 1 of disk 2 wouldn't be tagged as track #1, but as the track after the last track of disk 1.

- Printing languages like Chinese, Japanese & Korean to the console prints garbage instead.

This doesn't effect anything else in the code; tracks containing any of the above languages will still download & tag correctly.

# Troubleshooting
- If you are getting the message below and are 100% sure that you're inputting a valid URL, it's because of Qobuz's region lock. You'll need a VPN.
```
Not found (404). Bad URL? Returning to URL input screen...
```
- If you're getting this for every album you're trying to download, you need a new uat. Wipe your current uat from the config file and start up Qobuz-DL. It'll give you a new one. Input this into your config file. 
```
"Track <num> is restricted by right holders; can't download."
```
- My format id is set to "27", and the album is advertised as being 24-bit on the Qobuz Player and Qobuz store, but Qobuz-DL will only fetch it in 16-bit at best.

Simple explanation: Qobuz lie about/mislabel the highest available streaming quality. Ex. URL:
 
```
https://play.qobuz.com/album/qi7icfdkslpva
```
Try playing the above album in 24/96 via Qobuz Player. Could it be something to do with label rights?
- I'm able to acquire my own app id & app secret without contacting Qobuz, but when used, the following is returned from the API:
```
{'status': 'error', 'code': 400, 'message': 'Invalid Request Signature parameter (req_sig)'}
```
Not sure why this happens. The app id & secret are definitely correct.
