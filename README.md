# Qo-DL
Tool written in Python to download MP3s & FLACs from Qobuz for Windows & Linux. Sister of [Tidal-DL](https://github.com/Sorrow446/Tidal-DL).

Latest versions:   
Qo-DL: 9th Mar 19 - Release 4e   
Qo-DL Linux: 9th Mar 19 - Release 4e    
Qo-DL Playlist: 23rd Feb 19 - Release 1c **Latest build is broken. Use the previous one.**   
Qo-DL Playlist Linux: 13th Feb 19 - Release 1b   
**You'll need [this config template](https://thoas.feralhosting.com/sorrow/Qobuz-DL/config.ini) instead to use playlist.**   

Old builds are hosted [here](https://thoas.feralhosting.com/sorrow/Qobuz-DL/Old%20Builds/).

![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/b1.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/b2.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/p1.jpg)

# Setup
## Mandatory ##
The following need to be inputted into the config file:
- App id
- App secret - App IDs & secrets hosted [here](https://thoas.feralhosting.com/sorrow/Qobuz-DL/App.txt).
- Email address
- Format id - download quality (5 = 320 kbps MP3, 6 = 16-bit FLAC, 7 = 24-bit / =< 96kHz FLAC, 27 = best avail - 24-bit / >96 kHz =< 192 kHz FLAC).
- MD5 hashed password
- User auth token - you'll be given this automatically if it's not already inputted in. App id & app secret are required.
- Naming scheme - file naming scheme (1 = "01. ", 2 = "01 -").
- Cover size - cover size to request from API (1 = 230x230, 2 = 600x600).
- Keep_cover' - leave folder.jpg in album dir, Y or N. Not usable with Qobuz-DL_Playlist.
- Use_proxy - enable or disable proxy. "Y" or "N".  
- All tags under "[Tags]" except comment - "Y" or "N".  
 
**If the provided app id & secret get blacklisted, let me know. I have a bunch of working ones.**   
**You can't download ANY tracks with a free account.**
## Optional ##

- Move_to - specify where to move album folder after downloading, "" = default.
- Proxy - <IP address>:<port> Must be https. This can't be used to bypass Qobuz's region restrictions for track downloading. It only prevents 404s.

# Usage
Fill in your config file first.
### Windows ###
Run the exe.
### Linux ###
CD to wherever the exe is.
```
cd Desktop
```
Launch it.
```
./Qo-DL_Lin_x64
```
or
```
./Desktop/Qo-DL_Lin_x64
```

Qo-DL can also be used via command line.
Ex
```
usage: Qo-DL.py [-h] [-url URL] [-q Q] [-p P] [-list LIST] [-c C] [-s S]
                   [-k K] [-proxy PROXY] [-comment COMMENT]

optional arguments:
  -h, --help        show this help message and exit
  -url URL          Qobuz Player or Qobuz store URL.
  -q Q              Download quality. 5 = 320 kbps MP3, 6 = 16-bit FLAC, 7 =
                    24-bit / =< 96kHz FLAC, 27 = best avail - 24-bit / >96 kHz
                    =< 192 kHz FLAC. If the chosen qual is unavailable, the
                    next best option will be used as a fallback.
  -p P              Where to move album after downloading. Make sure you wrap
                    this up in double quotes.
  -list LIST        Download from a list of URLs. -list <txt filename>.
  -c C              Cover size to fetch. 1 = 230x230, 2 = 600x600.
  -s S              File naming scheme. 1 = "01. ", 2 = "01 -"
  -k K              Leave folder.jpg in album dir. Y or N.
  -proxy PROXY      <IP address>:<port>. Must be https. This can't be used to
                    bypass Qobuz's region restrictions for track downloading.
                    It only prevents 404s.
  -comment COMMENT  Custom comment. You can also input "URL" to write the
                    album URL to the field. Make sure you wrap this up in
                    double quotes.
```
Qobuz-DL Playlist can also be used via command line, but only supports one option for now.
```
Qobuz-DL_Playlist_x64.exe https://play.qobuz.com/playlist/1285066
```
# Update Log
## Qo-DL ##
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
- Download from list or URLs - put your urls inside a text file named "list.txt" in the current working dir (one per line), then load up Qo-DL and input "list" into the console.
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
**You can't use Qo-DL_xxx.exe to download playlists. I haven't merged the playlist code into the main exe yet, so you have to use Qobuz-DL_Playlist_xxx.exe for now.**
- Download progress percentage.
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
### 2nd Mar 19 - Release 4c ###
- Much more command line options.
- Fixed downloading from a list via CLI.
- Windows' max path limit handled.
I couldn't do much about this. Qo-DL won't crash anymore if it runs into this. The track's filename will be left as it was before the renaming attempt. Tags won't be affected.
### 2nd Mar 19 - Release 4d ###
- Single track download support. This can be used with the "-url" arg too.
### 9th Mar 19 - Release 4e ###
- Linux builds updated.
- Fixed downloading from list.
- Less strict filename & dir name replace regex. Brackets and commas were being replaced before. Only the characters Windows / Linux doesn't support in filenames will be replaced now.
- Unneeded cover.jpg wasn't being deleted before termination. This would only happen when used via command line.
- Composer would always be set to "xxxx". Even if the API returned composer info.
- Handled the below.
```
KeyError: 'copyright'
```
This would happen when the API wouldn't return copyright info.
- Default download folder changed from "Qobuz-DL Downloads" to "Qo-DL Downloads".

## Qo-DL Playlist ##
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
- Same notes as Qo-DL Release 4a.

### 23rd Feb 19 - Release 1c ###
- Same notes as Qo-DL Release 4b.

# Misc Info
Written around Python v3.6.7.  
Used libraries:
- argparse
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
- Video goodies must be purchased. Qo-DL can't get them for you (API returns "None" when requesting).
- Downloaded tracks are put in the "Qo-DL Downloads" folder. Ex. (Qo-DL Dir)\\Qo-DL Downloads\\(albumartist) - (albumtitle)\\(tracks)
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
- Add a check to see if the user has inputted a plain password into the config file instead of an MD5 hashed one.
- Merge main exe and playlist exe.

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
QO-DL_X64.EXE
```
Enlarging the console window manually by dragging out from the edges might also work. The Linux builds are also affected by this.

- The API has a limit of 500 tracks per playlist. I can't do anything about this.

# Troubleshooting
- If you are getting the message below and are 100% sure that you're inputting a valid URL, you need to either use a VPN or enable the proxy feature via the config file. **Nothing can be done about region locks. Your region is tied to your account.**
```
Not found (404). Bad URL? Returning to URL input screen...
```
- If you're getting this for every album you're trying to download, you either need a new uat or the app id + sec are dead. To get a new uat, wipe your current uat from the config file and start up Qo-DL. It'll give you a new one. Input this into your config file. If you're getting this for specific albums, there's either a region lock or the track is actually restricted by the right holders.
```
"Track <num> is restricted by right holders. Can't download."
```
- My format id is set to "27", and the album is advertised as being 24-bit on the Qobuz Player and Qobuz store, but Qo-DL will only fetch it in 16-bit at best.

Simple explanation: Qobuz lie about/mislabel the highest available streaming quality. Ex. URL:
 
```
https://play.qobuz.com/album/qi7icfdkslpva
```
Try playing the above album in 24/96 via Qobuz Player. Could it be something to do with label rights?

# Disclaimer
I will not be responsible for how you use Qo-DL and Qo-DL Playlist   
Neither Qo-DL nor Qo-DL Playlist contain code to bypass Qobuz's region restrictions for track downloading.     
Qo-DL & Qo-DL Playlist use the Qobuz API but are not endorsed, certified or otherwise approved in any way by Qobuz. Qobuz brand and name is the registered trademark of its respective owner. Qo-DL & Qo-DL Playlist has no partnership, sponsorship or endorsement with Qobuz.   
By using Qo-DL & Qo-DL Playlist, you agree to the following: http://static.qobuz.com/apps/api/QobuzAPI-TermsofUse.pdf
