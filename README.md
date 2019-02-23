# Qobuz-DL
Tool written in Python to download MP3s & FLACs from Qobuz for Windows & Linux (Linux builds have been fixed).

Latest versions:    
Qobuz-DL: 23rd Feb 19 - Release 4b   
Qobuz-DL Playlist: 23rd Feb 19 - Release 1c   
Qobuz-DL Linux: 13th Feb 19 - Release 4a   
Qobuz-DL Playlist Linux: 13th Feb 19 - Release 1b   

Old builds are hosted [here](https://thoas.feralhosting.com/sorrow/Qobuz-DL/Old%20Builds/).

![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/b1.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/b2.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/p1.jpg)

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
- Keep_cover' - leave folder.jpg in album dir, Y or N. Not usable with Qobuz-DL_Playlist.
- Use_proxy - enable or disable proxy.
- Proxy - <IP address>:<port> Must be https.
- All tags under "[Tags]" except comment - "Y" or "N".  
 
**If the provided app id & secret get blacklisted, let me know. I have a bunch of working ones.**
**You can't download ANY tracks with a free account.**
## Optional ##
- Comment tag - custom comment. You can also input "URL" to write the album URL to the field. 

You can specify what you want to be put into the comment field in your tracks. Special characters will be escaped.
- Move_to - specify where to move album folder after downloading, "" = default.

# Usage
Fill in your config file first.
### Windows ###
Run the exe.
### Linux ###
CD to wherever the exe is.
```
cd Desktop
```
Make it executable.
```
chmod +x Qobuz-DL_Lin_x64
```
Launch it.
```
./Qobuz-DL_Lin_x64
```
Qobuz-DL + Playlist can also be used via command line. Pass a URL to it. 
Ex:
```
Qobuz-DL_x64.exe https://play.qobuz.com/album/hxyqb40xat3uc
./Qobuz-DL_Lin_x64 https://play.qobuz.com/album/hxyqb40xat3uc
Qobuz-DL_Playlist_x64.exe https://play.qobuz.com/playlist/1285066
./Qobuz-DL_Playlist_Lin_x64 https://play.qobuz.com/playlist/1285066
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
TypeError: 'NoneType' object is not subsciptable
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
- Command line support. Pass a URL. This is the only option for now. 
It will automatically exit when it's finished its current task. Passing "list" probably won't work. 
- Better code to strip special characters for Windows filenames.
- ">" wasn't being stripped in filenames. Fixed.
- New field 'Tag_swap1' in config file - write to TRACKNUMBER instead of TRACK, Y or N.
- New field 'Tag_swap2' in config file  - write to DATE instead of YEAR, Y or N.
This only works for FLACs due to ID3 limitations. Not very tested. Metaflac can pick up the two new tags, but Mp3tag can't.
- Handled the below. This happens when the API returns 'None' when requesting the release year for albums. 'xxxx' will be used instead. I'm not sure why the API would do this. It's not album specific, and only seems to hit a small percentage of users.
```
OSError: [Errno 22] Invalid argument
```
- Handled the below. This happens when the API's album response doesn't conatin a performer key. Album specific. "performer**s**" will be used as a fallback.
```
KeyError: 'performer'
```
### 11th Feb 19 - Release 4 ###
- Download playlists using separate exe.
- Handled the below. This would happen if you were to download an album with no album cover.
```
urllib.error.HTTPError: HTTP Error 404: Not Found
```
**You can't use Qobuz-DL_xxx.exe to download playlists. I haven't merged the playlist code into the main exe yet, so you have to use Qobuz-DL_Playlist_xxx.exe for now.**
- Download progress bar.
- New field 'Move_to' in config file  - specify where to move album folder after downloading, "" = default.
- New field 'Keep_cover' in config file  - leave folder.jpg in album dir, Y or N. Not usable with Qobuz-DL_Playlist.
- Better way of checking if track is restricted by right holders. The previous method would crash and allow the below to happen with some albums:
```
KeyError: 'url'
```
### 13th Feb 19 - Release 4a ###
- Fixed the right holder restriction checker. Restricted tracks with samples won't be downloaded any more and treated like full tracks. 
- Handled the below. Would happen when exiting.
```
NameError: name 'exit' is not defined
```
- Handled the below. Would happen when the API wouldn't return neither a performer key nor a performer**s** key.
```
During handling of the above exception, another exception occured:
TypeError: string indices must be integers
```
### 23rd Feb 19 - Release 4b ###
- Proxy support.
Configure & enable via config file. Must be http**s**, and not http. It will only be used once (for the album/get? req).
- Configure tagging via config file.


## Qobuz-DL Playlist ##
### 11th Feb 19 - Release 1 ###
### 12th Feb 19 - Release 1a ###
- Fixed major issue where the API would only provide info for the first 50 tracks. After finishing downloading track 50, it would loop back to track 1. 
- Handled the below. This would happen when trying to download a track with no album cover.
```
urllib.error.HTTPError: HTTP Error 404: Not Found
```
- Handled the below. This would happen when trying to download a track restricted by right holders in the playlist. This was already handled, but the below would prevent the handler from executing.
```
TypeError: an ineger is required (got type NoneType)
```
- Handled the below. Would happen when the API wouldn't return neither a performer key nor a performer**s** key.
```
During handling of the above exception, another exception occured:
TypeError: string indices must be integers
```
### 13th Feb 19 - Release 1b ###
- Same notes as Qobuz-DL Release 4a.

### 23rd Feb 19 - Release 1c ###
- Same notes as Qobuz-DL Release 4b.

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

The user can choose which tags are to be written to.

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
- Implement Japanese translation.
- General code clean up.
- More command line options.
- Reduce size of executables (exclude libs etc.).
- Add a check to see if the user has inputted a plain password into the config file instead of an MD5 hashed one.
- Merge main exe and playlist exe.
- Single track (https://open.qobuz.com/track/xxxxxxxx) support.
- List feature broken? Look into that.

# Known Issues
- Albums with more than one disks will be treated as single-disk albums.

To make this clearer, track 1 of disk 2 wouldn't be tagged as track #1, but as the track after the last track of disk 1.

- Printing languages like Chinese, Japanese & Korean to the console prints garbage instead.

This doesn't effect anything else in the code; tracks containing any of the above languages will still download & tag correctly.

- If the "Downloading track x out of y" line is too long for the console, it'll be spammed instead of printed on a single line.

You can fix this by setting the width & height before calling the exe, like this:
```
REM 200 & 30 should be fine
MODE CON cols=200 lines=30
QOBUZ-DL_X64.EXE
```
Enlarging the console window manually by dragging out from the edges might also work. The Linux builds are also affected by this.

- The API has a limit of 500 tracks per playlist. I can't do anything about this.


# Troubleshooting
- If you are getting the message below and are 100% sure that you're inputting a valid URL, it's because of Qobuz's region lock. You can either use a VPN or enable the proxy feature via the config file.
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
- Users are able to acquire their own app id & app secret through sniffing without contacting Qobuz, but when used, the following will be returned from the API:
```
{'status': 'error', 'code': 400, 'message': 'Invalid Request Signature parameter (req_sig)'}
```
Chances are, Qobuz have to "activate" your app id & secret before you can use them.

# Disclaimer
I will not be responsible for how you use these tools.   
These tools use the Qobuz API but are not certified by Qobuz.      
By using them you agree to the following: http://static.qobuz.com/apps/api/QobuzAPI-TermsofUse.pdf
