#!/usr/bin/env python3

# r5a
# It needs a lot of TLC, not fully refactored.

# standard:
import os
import re
import ssl
import sys
import time
import codecs
import shutil
import hashlib
import pathlib
import datetime
import platform
import urllib.request
from itertools import islice
from urllib.error import HTTPError

# third party:
import argparse
import requests
import configparser
from mutagen import File
from clint.textui import progress
from mutagen.flac import FLAC, Picture
from nested_lookup import nested_lookup
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC, TRCK, APIC, WOAS, TPUB, TOPE, TCOP

def getConfig(option, req, section='Main'):
	config = configparser.ConfigParser()
	config.read('config.ini')
	try:
		if req:
			if not config[section][option].strip('"'):
				msList.append(option)
				return
		return config[section][option].strip('"')
	except KeyError:
		msList2.append(option)

def takeDataFromJSON(data):
	for num, trackid in enumerate(data['tracks']['items'], start=0):
		yield {'num': num, 'id': trackid['id'], 'title': trackid['title']}
		
def get_uat():
	print("UserAuthToken field in config file is empty. Fetching it...")
		
	responsetuat = requests.post("https://www.qobuz.com/api.json/0.2/user/login?",
		params={
			"email": email,
			"password": password,
			"app_id": appId,
		}
	)
	responset = responsetuat.json()
	rc = responsetuat.status_code
	if rc == 401:
		print("Bad credentials. Exiting...")
		time.sleep(3)
		sys.exit()
	elif rc == 200:
		uat = responset['user_auth_token']
		config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
		config.optionxform=str
		config.read('config.ini')
		config.set('Main', 'UserAuthToken', f'"{uat}"')
		with open("config.ini", "w") as fi:
			config.write(fi)
		print("Wrote UAT token to config file.")

def add_mp3_tags(filename, title, alartist, trart, year, altitle, curTr, totaltracks, comment, composer,
				copyright, genre, label, url, tracktg, albumtg, albatsttg, artisttg, performertg, yeartg, 
				composertg, copyrighttg, genretg, labeltg):
	try: 
		audio = ID3(filename)
	except ID3NoHeaderError:
		audio = ID3()
	if tracktg.lower() == "y":
		audio["TIT2"] = TIT2(encoding=3, text=title)			
	if albumtg.lower() == "y":		
		audio["TALB"] = TALB(encoding=3, text=altitle)
	if albatsttg.lower() == "y":
		audio["TPE2"] = TPE2(encoding=3, text=alartist)
	if artisttg.lower() == "y":
		audio["TPE1"] = TPE1(encoding=3, text=trart)
	if performertg.lower() == "y":
		audio["TOPE"] = TOPE(encoding=3, text=trart)
	if yeartg.lower() == "y":	
		audio["TDRC"] = TDRC(encoding=3, text=year)
	if tracktg.lower() == "y":				
		audio["TRCK"] = TRCK(encoding=3, text=str(curTr) + "/" + str(totaltracks))
	if composertg.lower() == "y":
		audio["TCOM"] = TCOM(encoding=3, text=composer)
	if copyrighttg.lower() == "y":	
		audio["TCOP"] = TCOP(encoding=3, text=copyright)
	if genretg.lower() == "y":	
		audio["TCON"] = TCON(encoding=3, text=genre)
	if labeltg.lower() == "y":
		audio["TPUB"] = TPUB(encoding=3, text=label)			
	if comment != "":
		if comment.lower() == "url":
			audio["COMM"] = COMM(encoding=3, lang=u'eng', text=url)
		else:
			audio["COMM"] = COMM(encoding=3, lang=u'eng', text=comment)
	audio.save(filename, 'v2_version=3')
	
def add_mp3_cover(filename, albumart):
	if alcovfapi == True:
		audio = ID3(filename)
		audio.add(APIC(3, 'image/jpeg', 3, '', albumart))
		audio.save(filename, 'v2_version=3')

def add_flac_tags(filename, title, alartist, trart, year, altitle, curTr, totaltracks, comment, composer,
				copyright, genre, label, url, tracktg, albumtg, albatsttg, artisttg, performertg, yeartg, 
				composertg, copyrighttg, genretg, labeltg, datetg, trnumtg, trtotaltg, trtotal2tg):
	audio = FLAC(filename)
	if albumtg.lower() == "y":
		audio['album'] = altitle
	if albatsttg.lower() == "y":
		audio['albumartist'] = alartist
	if artisttg.lower() == "y":
		audio['artist'] = trart		
	if comment != "":
		if comment.lower() == "url":
			audio['artist'] = url	
		else:
			audio['artist'] = comment
	if composertg.lower() == "y":
		audio['composer'] = composer		
	if copyrighttg.lower() == "y":
		audio['copyright'] = copyright	
	if datetg.lower() == "y":
		audio['date'] = year
	if genretg.lower() == "y":
		audio['genre'] = genre
	if labeltg.lower() == "y":
		audio['label'] = label
	if albumtg.lower() == "y":
		audio['title'] = title
	if albumtg.lower() == "y":			
		audio['track'] = str(curTr)
	if yeartg.lower() == "y":			
		audio['year'] = year
	if trnumtg.lower() == "y":	
		audio['tracknumber'] = str(curTr)
	if trtotaltg.lower() == "y":	
		audio['tracktotal'] = str(totaltracks)
	if trtotal2tg.lower() == "y":	
		audio['totaltracks'] = str(totaltracks)
	audio.save()

def add_flac_cover(filename, albumart):
	if alcovfapi == True:
		audio = File(filename)
		image = Picture()
		image.type = 3
		mime = 'image/jpeg'
		with open(albumart, 'rb') as f:
			image.data = f.read()
			audio.add_picture(image)
			audio.save()
	if os.path.isfile(fullDlDir):
		os.remove(fullDlDir)
	desFile = f"{cwd}/{fullDlDir}/{filename}"
	if os.path.isfile(desFile):
		os.remove(desFile)
	shutil.move(filename, fullDlDir)

def reporthook(blocknum, blocksize, totalsize):
		readsofar = blocknum * blocksize
		if totalsize > 0:
			percent = readsofar * 1e2 / totalsize		
			try:
				if blet:
					pass
			except NameError:
				l = "Downloading new build..."
			else:
				if blet == "N":
					if fext == ".mp3":
						if not isTrack:
							l = f"Downloading track {curTr} of {totaltracks}: {trackTr} - 320 kbps MP3"
						else:
							l = f"Downloading track 1 of 1: {trackTr} - 320 kbps MP3"	
					if fext == ".flac":
						if not isTrack:
							l = f"Downloading track {curTr} of {totaltracks}: {trackTr} - {tspa}-bit / {tspb} kHz FLAC"
						else:
							l = f"Downloading track 1 of 1: {trackTr} - {tspa}-bit / {tspb} kHz FLAC"			
				elif blet == "Y":
					l = "Digital booklet available. Downloading..."
			s = "\r%5.f%%" % (
			percent)		
			sys.stderr.write(f"{l}{percent:5.0f}%\r")			
			if readsofar >= totalsize:
				sys.stderr.write("\n")

def rip(trackid, num, appId, appSecret, formatId, timeunx, userAuthToken, isTrack, data, fn2,
		downloadDir, dlDir0, alcovfapi, fn, artist, year2, altitle, totaltracks, comment,
		composer, copyright, genre, label, url, tracktg, albumtg, albatsttg, artisttg, 
		performertg, yeartg, composertg, copyrighttg, genretg, labeltg, dlDir1, datetg, 
		trnumtg, trtotaltg, trtotal2tg, trarttmp):
	reqsigt = f"trackgetFileUrlformat_id{formatId}track_id{trackid}{timeunx}{appSecret}"
	reqsighst = (hashlib.md5(reqsigt.encode('utf-8')).hexdigest())
	responset = requests.post("https://www.qobuz.com/api.json/0.2/track/getFileUrl?",
			params={
				"user_auth_token": userAuthToken,
				"app_id": appId,
				"request_ts": timeunx,
				"request_sig": reqsighst,
				"track_id": trackid,
				"format_id": formatId
			}
		)
	tr = responset.json()
	isRes = False
	try:
		finalurltr = tr['url']
	except KeyError:
		isRes = True
	try:
		finalurltrc = finalurltr[:25]
		if finalurltrc == "https://sample2.qobuz.com":
			isRes = True
	except:
		isRes = True
	if isRes:
		print(f"Track {curtr} is restricted by right holders. Can't download.")
	else:
		if not isTrack:
			try:
				trart = data['tracks']['items'][(num)]['performer']['name']
			except (KeyError, TypeError):
				try:
					trart = data['tracks']['items'][(num)]['performers']['name']
				except (KeyError, TypeError):
					trart = ""
		else:
			trart = trarttmp
		global blet
		global tspa
		global tspb
		tspa = tr['bit_depth']
		tspb = tr['sampling_rate']
		tfn0 = f"{fn2}{trackTr}{fext}"
		if GetOsType():
			tfn = re.sub(r'[\\/:*?"><|]', '-', tfn0)
		else:
			tfn = re.sub('/', '-', tfn0)
		blet = "N"	
		if downloadDir:
			os.chdir(downloadDir)
			if not os.path.isdir(dlDir0):
				os.mkdir(dlDir0)		
			os.chdir(dlDir0)		
			if not os.path.isdir(dlDir1):
				os.mkdir(dlDir1)
			os.chdir(dlDir1)
			if os.path.isfile(fullDlDir):
				os.remove(fullDlDir)
			cwd = downloadDir
		urllib.request.urlretrieve(finalurltr, f"{curTr}{fext}", reporthook)
		if alcovfapi == True:
			albumart2 = open('cover.jpg', 'rb').read()
		else:
			albumart2 = ""
		if fext == ".mp3":
			add_mp3_tags(fn, trackTr, artist, trart, year2, altitle, curTr, totaltracks, comment, composer, 
						 copyright, genre, label, url, tracktg, albumtg, albatsttg, artisttg, performertg,
						 yeartg, composertg, copyrighttg, genretg, labeltg)
			add_mp3_cover(fn, albumart2)
		else:
			add_flac_tags(fn, trackTr, artist, trart, year2, altitle, curTr, totaltracks, comment, composer, 
						 copyright, genre, label, url, tracktg, albumtg, albatsttg, artisttg, performertg,
						 yeartg, composertg, copyrighttg, genretg, labeltg, datetg, trnumtg, trtotaltg,
						 trtotal2tg)
			add_flac_cover(fn, 'cover.jpg')
		# clean this up
		if downloadDir:
			flcdirn = f"{cwd}/{fullDlDir}/{tfn}"
			flcdir = f"{cwd}/{fullDlDir}/{fn}"
		else:
			flcdirn = f"{fullDlDir}/{tfn}"
			flcdir = f"{fullDlDir}/{fn}"
		list = ["booklet.pdf", "folder.jpg"]
		for item in list:
			a = os.path.isfile(item)
			if a:
				os.remove(item)
		if os.path.isfile(tfn):
			os.remove(tfn)
		try:
			os.rename(fn, tfn)
		except OSError:
			print("Failed to rename track. Maybe it exceeds the max path length for your OS.")
		
def GetOsType():
	osPlatform = platform.system()
	if osPlatform == 'Windows':
		return True
	else:
		return False

# Untested. Only for compiled builds.
def update(currentVer):
	try:
		latestVer = urllib.request.urlopen('https://thoas.feralhosting.com/sorrow/Qobuz-DL/Check/Qo-DL_x86.txt').read().decode('utf-8').lower()
	except:
		print("Failed to check for update.\n")
	if latestVer != "r5a":
		q = None
		while q not in ("y", "n"):
			q = input(f"New version is available: {latestVer}. You have {currentVer}. Update now? [y/n]").lower()
			if q != "y" or q != "n":
				osCommands('clear')
		if q == "y":
			if "x64" and "OSX" in sys.argv[0]:
				arch = "OSX_x64"
			elif "x86" and "OSX" in sys.argv[0]:
				arch = "OSX_x86"
			elif "x64" and "Lin" in sys.argv[0]:
				arch = "Lin_x64"
			elif "x86" and "Lin" in sys.argv[0]:
				arch = "Lin_x86"
			else:
				arch = "Win_x86.exe"
			if os.path.isdir(f"Qo-DL_{arch}_{latestVer}"):
				shutil.rmtree(f"Qo-DL_{arch}_{latestVer}")
			os.mkdir(f"Qo-DL_{arch}_{latestVer}")
			os.chdir(f"Qo-DL_{arch}_{latestVer}")
			GHubPost = requests.post(f"https://raw.githubusercontent.com/Sorrow446/Qo-DL/master/Qo-DL_{arch}",
				params={
					# fake user agent to prevent 404.
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
				}
			)
			if GHubPost.status_code != 200:
				print("Failed to fetch updated build from GitHub. Trying FTP mirror...\n")
				urllib.request.urlretrieve(f'https://thoas.feralhosting.com/sorrow/Qobuz-DL/Latest%20Build/Qo-DL_{arch}', f'Qo-DL_{arch}', reporthook)
				urllib.request.urlretrieve(f'https://thoas.feralhosting.com/sorrow/Qobuz-DL/Latest%20Build/config.ini', 'config.ini')
			else:
				urllib.request.urlretrieve(f'https://raw.githubusercontent.com/Sorrow446/Qo-DL/master/Qo-DL_{arch}', f'Qo-DL_{arch}', reporthook)
				urllib.request.urlretrieve(f'https://raw.githubusercontent.com/Sorrow446/Qo-DL/master/config.ini', 'config.ini')
			os.chdir('..')
			print(f"Done. Updated build can be found in the 'Qo-DL_{arch}_{latestVer}' folder.\nExiting...")
			time.sleep(3)
			sys.exit()
		else:
			return

def osCommands(a):
	if a == "pause":
		if GetOsType():
			os.system('pause')
		else:
			os.system("read -rsp $\"\"")
	elif a == "clear":
		if GetOsType():
			os.system('cls')
		else:
			os.system("clear")
	else:
		if GetOsType():
			os.system('title Qo-DL R5a (by Sorrow446)')
		else:
			sys.stdout.write("\x1b]2;Qo-DL R5a (by Sorrow446)\x07")
		
def init():
	if not os.path.isfile('config.ini'):
		print("Config file is missing.\nExiting...")
		time.sleep(2)
		sys.exit()
	osCommands('t')
	# Use alternative method instead of setting globals. Needed for reporthook function. More Global functions defined in rip func too.
	global fext
	global isTrack
	global curTr
	global trackTr
	global totaltracks
	global alcovfapi
	global cwd
	global fullDlDir
	lin = int(0)
	lin2 = int(-1)
	listStatus = ""
	cwd = os.getcwd()
	currentVer = "R5a"
	ssl._create_default_https_context = ssl._create_unverified_context
	msList, msList2, msList3 = [], [], ["appId", "appSecret", "email", "formatId", "password", "userAuthToken", "namingScheme", "coverSize",  "downloadDir", "keepCover", "useProxy", "proxy", "skipPwHashCheck", "checkForUpdates"]
	try:
		if sys.argv[1]:
			cline = True
			parser = argparse.ArgumentParser(
				description='A tool written in Python to download MP3s & FLACs from Qobuz.')
			parser.add_argument(
				'-url',
				default='',
				help='Qobuz Player or Qobuz store URL. Single track or album.')
			parser.add_argument(
				'-q',
				default='',
				help='Download quality. 5 = 320 kbps MP3, 6 = 16-bit FLAC, 7 = 24-bit / =< 96kHz FLAC, 27 = best avail - 24-bit / >96 kHz =< 192 kHz FLAC. If the chosen qual is unavailable, the next best option will be used as a fallback.') 
			parser.add_argument(
				'-p',
				default='',
				help='Where to download tracks to. Make sure you wrap this up in double quotes.')
			parser.add_argument(
				'-list',
				default='',
				help='Download from a list of URLs. -list <txt filename>.')
			parser.add_argument(
				'-c',
				default='',
				help='Cover size to fetch. 0 = 50x50, 1 = 230x230, 2 = 600x600. 3 = max')
			parser.add_argument(
				'-s',
				default='',
				help='File naming scheme. 1 = "01. ", 2 = "01 -"')
			parser.add_argument(
				'-k',
				default='',
				help='Leave folder.jpg in album dir. Y or N.')
			parser.add_argument(
				'-proxy',
				default='',
				help="<IP address>:<port>. Must be https. This can't be used to bypass Qobuz's region restrictions for track downloading. It only prevents 404s.")
			parser.add_argument(
				'-comment',
				default='',
				help='Custom comment. You can also input "URL" to write the album URL to the field. Make sure you wrap this up in double quotes.')
			parser.add_argument(
				'-embed',
				default='',
				help='Write album covers to tracks.')
			parser.add_argument(
				'-skipcheck',
				default='',
				help='Skip check to see if password is a valid MD5 hash.')
			args = parser.parse_args()
			if args.url:
				album_url = args.url
			if args.q:
				formatId = args.q
			else:
				formatId = getConfig('formatId', True, 'Main')
			if formatId == "5":
				fext = ".mp3"
			else:
				fext = ".flac"
			if not args.c == "":
				cover_size = args.c
			else:
				cover_size = getConfig('coverSize', True, 'Main')
			if cover_size == "0":
				alcovs = "thumbnail"
			elif cover_size == "1":
				alcovs = "small"
			elif cover_size == "2":
				alcovs = "large"
			else:
				alcovs = cover_size
			if args.p:
				downloadDir = args.p
			else:
				downloadDir = getConfig('downloadDir', False, 'Main')
			if args.list:
				txtFilename = args.list
			if args.s:
				naming_scheme = args.s
			else:
				naming_scheme = getConfig('namingScheme', True, 'Main')
			if naming_scheme == "1":
				fp = ". "
			elif naming_scheme == "2":
				fp = " - "
			if args.k:
				keepCover = args.k
			else:
				keepCover = getConfig('keepCover', True, 'Main')
			if args.proxy:
				proxy = args.proxy			
				useProxy = "y"
			if args.comment:
				comment = args.comment
			else:
				comment = getConfig('comment', False, 'Tags')		
			if args.embed:
				embed_cover	= args.embed
			else:
				embed_cover = getConfig('embedCover', True, 'Tags')
			if args.skipcheck:
				skipPwHashCheck = args.skipcheck
	except IndexError:
		cline = False
		formatId = getConfig('formatId', True, 'Main')
		cover_size = getConfig('coverSize', True, 'Main')
		downloadDir = getConfig('downloadDir', False, 'Main')	
		naming_scheme = getConfig('namingScheme', True, 'Main')
		keepCover = getConfig('keepCover', True, 'Main')
		comment = getConfig('comment', False, 'Tags')			
		embed_cover = getConfig('embedCover', True, 'Tags')
		if naming_scheme == "1":
			fp = ". "
		elif naming_scheme == "2":
			fp = " - "
		if formatId == "5":
			fext = ".mp3"
		else:
			fext = ".flac"		
		if cover_size == "0":
			alcovs = "thumbnail"
		elif cover_size == "1":
			alcovs = "small"
		elif cover_size == "2":
			alcovs = "large"
		else:
			alcovs = cover_size	
	appId = getConfig('appId', True, 'Main')
	appSecret = getConfig('appSecret', True, 'Main')
	email = getConfig('email', True, 'Main')
	password = getConfig('password', True, 'Main')
	userAuthToken = getConfig('userAuthToken', False, 'Main')
	useProxy = getConfig('useProxy', True, 'Main')
	skipPwHashCheck = getConfig('skipPwHashCheck', True, 'Main')
	proxy = getConfig('proxy', False, 'Main')
	checkForUpdates = getConfig('checkForUpdates', True, 'Main')
	albumtg = getConfig('album', True, 'Tags')
	albatsttg = getConfig('albumArtist', True, 'Tags')
	artisttg = getConfig('artist', True, 'Tags')
	composertg = getConfig('composer', True, 'Tags')
	copyrighttg = getConfig('copyright', True, 'Tags')
	genretg = getConfig('genre', True, 'Tags')
	labeltg = getConfig('label', True, 'Tags')
	performertg = getConfig('performer', 'y', 'Tags')
	titletg = getConfig('title', True, 'Tags')
	tracktg = getConfig('track', True, 'Tags')
	yeartg = getConfig('year', True, 'Tags')
	datetg = getConfig('date', True, 'Tags')
	trnumtg = getConfig('trackNumber', True, 'Tags')
	trtotaltg = getConfig('trackTotal', True, 'Tags')
	trtotal2tg = getConfig('totalTracks', True, 'Tags')
	if checkForUpdates.lower() == "y":
		update(currentVer)
	if msList2:
		msList2j = ', '.join(msList2)
		print(f"The following required fields in your config file are missing: {msList2j}.")
		config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
		config.optionxform=str
		config.read('config.ini')
		for item in msList2:
			if item.lower() in msList3:
				config.set('Main', item, f'""')
			else:
				config.set('Tags', item, f'""')			
		with open("config.ini", "w") as fi:
				config.write(fi)
		print("Wrote missing field(s) to config file. Please fill them in.\n"
			  "Exiting...")
		time.sleep(5)
		sys.exit()
	if msList:
		msList = ', '.join(msList)
		print(f"The following required fields in your config file are empty: {msList}.\n"
			   "Please fill them in\n. Press any key to exit.")
		os.system("pause >nul")
		os.system("read -rsp $\"\"")
		sys.exit()
	if skipPwHashCheck.lower() == "n":
		if not re.findall(r"\b([a-f\d]{32}|[A-F\d]{32})\b", password):
			print("Your password is not a valid MD5 hash.")
			npassword = hashlib.md5(password.encode("utf-8")).hexdigest()
			config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
			config.optionxform=str		
			config.read('config.ini')
			config.set('Main', 'password', f'"{npassword}"')
			with open("config.ini", "w") as fi:
				config.write(fi)
			password = getConfig('password', True, 'Main')
			print("Wrote hashed password to config file.")
	if useProxy == "y":
		if not proxy:
			print("You have useProxy enabled, but didn't provide a proxy. Exiting...")
			time.sleep(3)
			sys.exit()
	timeunx = int(time.time())
	responset0 = requests.post("https://www.qobuz.com/api.json/0.2/user/login?",
		params={
			"email": email,
			"password": password,
			"app_id": appId,
		}
	)
	ssc0 = responset0.json()
	rc = responset0.status_code
	if rc == 401:
		print("Bad credentials. Exiting...")
		time.sleep(3)
		sys.exit()
	elif rc == 200:
		try:
			ssc1 = ssc0['user']['credential']['parameters']['label']
		except TypeError:
			print("Free accounts are not eligible to get tracks.\nExiting...")
			time.sleep(3)
			sys.exit()
		if not cline:
			print(f"Signed in successfully - {ssc1} account. \n")
	while True:
		if not userAuthToken:
			get_uat()
		if cline:
			try:
				if txtFilename:
					if not os.path.isfile('config.ini'):
						os.chdir(cwd)
					if os.path.isfile(txtFilename):
						totalLines = sum(1 for line in open(txtFilename))
						lin = lin + 1
						lin2 = lin - 1
						with open(txtFilename) as fin:
							for line in islice(fin, lin2, lin):
								listStatus = "ND"
								album_id = line.strip()
								album_id2 = album_id.split('/')[-2]
								album_id = album_id.split('/')[-1]
								if album_id2.lower() == "track":
									isTrack = True
									album_id == album_id2
								elif album_id2.lower() == "album":
									isTrack = False
								else:
									print("Invalid URL. Skipping...")
									continue
						if totalLines == lin:
							listStatus = "D"
							album_id = line.strip()
							album_id2 = album_id.split('/')[-2]
							album_id = album_id.split('/')[-1]
							if album_id2.lower() == "track":
								isTrack = True
								album_id == album_id2
							elif album_id2.lower() == "album":
								isTrack = False
							else:		
								print("Invalid URL. Skipping...")							
					else:
						print(f"Specified text file {txtFilename} doesn't exist. Exiting...")
						time.sleep(2)
						sys.exit()
			except NameError:
				pass
		if not listStatus or listStatus == "ND":
			try:
				if args.url:
					album_url = args.url
					album_id = album_url.split('/')[-1]
					album_id2 = album_url.split('/')[-2]
					listStatus = "D"
					if album_id2.lower() == "track":
						isTrack = True
					elif album_id2.lower() == "album":
						isTrack = False
					else:
						print("Invalid URL. Exiting...")
						time.sleep(2)
						osCommands('clear')
						sys.exit()
			except NameError:
				album_url = input("Input Qobuz Player or Qobuz store URL:")
				try:
					album_id = album_url.split('/')[-1]
					album_id2 = album_url.split('/')[-2]
				except IndexError:
					print("Invalid URL. Returning to URL input screen...")
					time.sleep(2)
					osCommands('clear')
					continue
				if album_id2.lower() == "track":
					isTrack = True
				elif album_id2.lower() == "album":
					isTrack = False
				else:
					print("Invalid URL. Returning to URL input screen...")
					time.sleep(2)
					osCommands('clear')
					continue		
		osCommands('clear')
		if useProxy == "y":
			proxies={
				"https":str(proxy)
			}
		else:
			proxies = None
		if isTrack:
			response = requests.post("https://www.qobuz.com/api.json/0.2/track/get?",
				params={
					"app_id": appId,
					"track_id": album_id,
				},
				proxies=proxies
			)		
		else:
				response = requests.post("https://www.qobuz.com/api.json/0.2/album/get?",
					params={
						"app_id": appId,
						"album_id": album_id,
					},
					proxies=proxies
				)
		rc2 = response.status_code
		if rc2 == 404:
			print("Not found (404). a proxy / VPN is needed. If you're already connected to a proxy, "
				  "try a different one in a different country and make sure it's https, and not http.\n" 
				  "Returning to URL input screen...")
			time.sleep(3)
			osCommands('clear')
			continue
		data = response.json()
		if not isTrack:
			try:
				composer = data['composer']['name']
			except KeyError:
				print("The API didn't return a composer. Tag will be left empty.") 
				composer = ""
			totaltracks = data['tracks_count']
			artist = data['artist']['name']
			if not artist:
				print("The API didn't return an album artist. Tag will be left empty.") 			
				artist = ""
			artistts = data['artist']['name']
			if not artistts:
				artistts = ""
			if not artistts:
				print("The API didn't return a track artist. Tag will be left empty.") 			
				artistts = ""
			genre = data['genre']['name']
			label = data['label']['name']
			url = data['url']
			if alcovs == '3':
				alcov = data['image']['large'][:-7] + "max.jpg"
			else:
				alcov = data['image'][str(alcovs)]
			year = data['released_at']
			diskCount = data['media_count']
			altitlets = data['title']
		else:
			try:
				composer = data['album']['composer']['name']
			except KeyError:
				print("The API didn't return a composer. Tag will be left empty.") 
				composer = ""
			totaltracks = data['album']['tracks_count']
			artist = data['album']['artist']['name']
			if not artist:
				print("The API didn't return an album artist. Tag will be left empty.") 			
				artist = ""
			artistts = data['album']['artist']['name']
			if not artistts:
				print("The API didn't return a track artist. Tag will be left empty.") 			
				artistts = ""
			genre = data['album']['genre']['name']
			label = data['album']['label']['name']
			url = data['album']['url']
			if alcovs == '3':
				alcov = data['album']['image']['large'][:-7] + "max.jpg"
			else:
				alcov = data['album']['image'][str(alcovs)]
			year = data['album']['released_at']
			diskCount = data['album']['media_count']
			num = data['track_number']
			version = data['version']
			altitlets = data['album']['title']
			altitle, tracktrtmp = data['title'], data['title']
		try:
			trarttmp = data['performer']['name']
		except (KeyError, TypeError):
			try:
				trarttmp = data['performers']['name']
			except (KeyError, TypeError):
				trarttmp = ""
		try:
			copyright = data['copyright']
		except KeyError:
			print("The API didn't return copyright information. Tag will be left empty.") 
			copyright = ""
		dlDir0 = "Qo-DL Downloads"
		if not os.path.exists(dlDir0):
			os.makedirs(dlDir0)
		if GetOsType():
			dlDir1a2 = re.sub(r'[\\/:*?"><|]', '-', altitlets)
			dlDir1ar2 = re.sub(r'[\\/:*?"><|]', '-', artistts)
		else:
			dlDir1a2 = re.sub('/', '-', altitlets)
			dlDir1ar2 = re.sub('/', '-', artistts)
		dlDir1 = f"{dlDir1ar2} - {dlDir1a2}"		
		fullDlDir = f"{dlDir0}/{dlDir1}"
		if not os.path.exists(fullDlDir):
			pathlib.Path(fullDlDir).mkdir(parents=True)
		if embed_cover.lower() == "y":
			alcovfapi = True
		else:
			alcovfapi = False
		if downloadDir:
			os.chdir(f"{downloadDir}/{dlDir0}/{dlDir1}")
		else:
			os.chdir(f"{dlDir0}/{dlDir1}")
		try:
			urllib.request.urlretrieve(alcov, 'cover.jpg')
		except HTTPError:
			print("This album doesn't have an album cover.")
			alcovfapi = False
		try:	
			year2 = datetime.datetime.fromtimestamp(year).strftime('%Y')
		except OSError:
			print("The API didn't return a release year. Tag will be left empty.") 
			year2 = ""
		if not isTrack:
			print(f"{artist} - {altitle}\n")
		else:
			print(f"{trarttmp} - {tracktrtmp}\n")
		# WEB tracks shouldn't really have disks anyway.
		if diskCount >= 2:
			print("This album has multiple disks. It can still be downloaded, but it will be treated as a single disk album.") 	
		if not isTrack:
			# Temporary nested_lookup to recurse through track versions. Couldn't get enumerate to work properly.
			for item, version in zip(takeDataFromJSON(data), nested_lookup("version", data, True)):
				trackid = item.get("id")
				if version:
					trackTr = f"{item.get('title')} ({version})"
				else:
					trackTr = item.get("title")
				num = item.get("num")
				curTr = int(num + 1)
				if fext == ".mp3":
					fn = f"{curTr}.mp3"
				else:
					fn = f"{curTr}.flac"
				if curTr <= 9:
					fn2 = f"0{curTr}{fp}"
				else:
					fn2 = f"{curTr}{fp}"
				# Do something about arg passing.
				rip(trackid, num, appId, appSecret, formatId, timeunx, userAuthToken, isTrack, data, fn2,
					downloadDir, dlDir0, alcovfapi, fn, artist, year2, altitle, totaltracks, comment,
					composer, copyright, genre, label, url, tracktg, albumtg, albatsttg, artisttg,
					performertg, yeartg, composertg, copyrighttg, genretg, labeltg, dlDir1, datetg, 
					trnumtg, trtotaltg, trtotal2tg, trarttmp)
		else:
			trackid = album_id
			trackTr = tracktrtmp
			curTr = num
			if curTr <= 9:
				fn2 = f"0{curTr}{fp}"
			else:
				fn2 = f"{curTr}{fp}"
			if fext == ".mp3":
				fn = f"{curTr}.mp3"
			else:
				fn = f"{curTr}.flac"
			# Do something about arg passing.	
			rip(trackid, num, appId, appSecret, formatId, timeunx, userAuthToken, isTrack, data, fn2,
					downloadDir, dlDir0, alcovfapi, fn, artist, year2, altitle, totaltracks, comment,
					composer, copyright, genre, label, url, tracktg, albumtg, albatsttg, artisttg,
					performertg, yeartg, composertg, copyrighttg, genretg, labeltg, dlDir1, datetg, 
					trnumtg, trtotaltg, trtotal2tg, trarttmp)
		if keepCover.lower() == "y":
			os.rename('cover.jpg', 'folder.jpg')
		else:
			os.remove('cover.jpg')
		bl = "goodies" in data.keys()
		if bl:
			blid = data['goodies'][0]['file_format_id']
			if blid == 21:	
				booklet = data['goodies'][0]['original_url']
				blet = "Y"
				urllib.request.urlretrieve(booklet, 'booklet.pdf', reporthook)
		if cline:
			if listStatus == "ND":
				print("Moving onto next item in list...")
				time.sleep(1)
				osCommands('clear')
				continue
			elif listStatus == "D":
				print("Exiting...")
				time.sleep(2)
				sys.exit()
		print("Returning to URL input screen...")
		lin = int(0)
		lin2 = int(-1)
		listStatus = ""
		time.sleep(2)
		osCommands('clear')

if __name__ == '__main__':
	init()
