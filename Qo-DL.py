#!/usr/bin/env python3

# r5c
# It needs a lot of TLC, not fully refactored.

# standard:
import os
import re
import ssl
import sys
import time
import gzip
from pathlib import Path
import codecs
import shutil
import hashlib
import pathlib
import argparse
import datetime
import platform
import configparser
import urllib.request
from itertools import islice
from urllib.error import HTTPError

# third party:
import requests
import pySmartDL
from mutagen import File
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3NoHeaderError
import mutagen.id3 as id3

class BundleError(Exception):
	pass

class BundleNotFoundError(BundleError):
	def __init__(self, login_page_req):
		with open("login.html.gz", "wb") as login_file:
			login_file.write(
				gzip.compress(login_page_req.content)
			)

class BundleParseError(BundleError):
	def __init__(self, bundle_req):
		self.url = bundle_req.url
		# save local copy of bundle file for debugging purposes
		with open("bundle.js.gz", "wb") as bundle_file:
			bundle_file.write(
				gzip.compress(bundle_req.content)
			)

class AppIdNotFoundError(BundleParseError):
	pass

class SecretNotFoundError(BundleParseError):
	pass

def getConfig(option, req, section='Main'):
	config = configparser.ConfigParser()
	config.read('config.ini')
	try:
		if req:
			if not config[section][option].strip('"'):
				msList.append(option)
		return config[section][option].strip('"')
	except KeyError:
		msList2.append(option)

def sanitizeFilename(filename):
	if getOsType():
		return re.sub(r'[\\/:*?"><|]', '-', filename)
	else:
		return re.sub('/', '-', filename)

def getAppIdAndSecret():
	login_page_req = requests.get("https://play.qobuz.com/login")
	login_page = login_page_req.text
	bundle_url_match = re.search(r'<script src="(/resources/\d+\.\d+\.\d+-[a-z]\d{3}/bundle\.js)"></script>',
		login_page)
	if not bundle_url_match:
		raise BundleNotFoundError(login_page_req)
	else:
		bundle_url = bundle_url_match.group(1)
	bundle_req = requests.get("https://play.qobuz.com" + bundle_url)
	bundle = bundle_req.text
	id_secret_match = re.search(r'{app_id:"(?P<app_id>\d{9})",app_secret:"(?P<secret>\w{32})",base_port:"80",base_url:"https://www\.qobuz\.com",base_method:"/api\.json/0\.2/"},n\.base_url="https://play\.qobuz\.com"', bundle)
	if id_secret_match is None or "app_id" not in id_secret_match.groupdict():
		raise AppIdNotFoundError(bundle_req)
	elif "secret" not in id_secret_match.groupdict():
		raise SecretNotFoundError(bundle_req)
	else:
		return (id_secret_match.group("app_id"), id_secret_match.group("secret"))

def add_mp3_tags(filename, metadata):
	audio = id3.ID3(filename)
	# ID3 is weird about the track number and total so we have to set that manually
	audio["TRCK"] = id3.TRCK(encoding=3, text=f"{metadata.pop('TRACKNUMBER')}/{metadata.pop('TRACKTOTAL')}")
	legend = {
		"ALBUM": id3.TALB,
		"ALBUMARTIST": id3.TPE2,
		"ARTIST": id3.TPE1,
		"COMMENT": id3.COMM,
		"COMPOSER": id3.TCOM,
		"COPYRIGHT": id3.TCOP,
		"DATE": id3.TDAT,
		"GENRE": id3.TCON,
		"ORGANIZATION": id3.TPUB,
		"TITLE": id3.TIT2,
		"ISRC": id3.TSRC
	}
	for tag, value in metadata.items():
		id3tag = legend[tag]
		audio[id3tag.__name__] = id3tag(encoding=3, text=value if value is not None else "")
	audio.save(filename, 'v2_version=3')
	
def getAlbumId(link):
	return re.match(r"https?://(?:w{0,3}|play|open)\.qobuz\.com/(?:(?:album|track)/|[a-z]{2}-[a-z]{2}/album/\w+(?:-\w+)*/)(\w+)", link).group(1)

def add_mp3_cover(filename, albumart):
	audio = id3.ID3(filename)
	audio.add(id3.APIC(3, 'image/jpeg', 3, '', albumart))
	audio.save(filename, 'v2_version=3')

def add_flac_tags(filename, metadata):
	audio = FLAC(filename)
	for tag, value in metadata.items():
		audio[tag] = value if value is not None else ""
	audio.save()

def add_flac_cover(filename, albumart):
	audio = File(filename)
	image = Picture()
	image.type = 3
	image.mime = "image/jpeg"
	with open(albumart, 'rb') as f:
		image.data = f.read()
		audio.add_picture(image)
		audio.save()

def rip(album_id, isTrack, session, comment, formatId, alcovs, downloadDir, naming_scheme, keep_cover):
	if formatId == "5":
		fext = ".mp3"
	else:
		fext = ".flac"
	if isTrack:
		response = session.post("https://www.qobuz.com/api.json/0.2/track/get?",
			params={
				"track_id": album_id,
			},
		)
		albumMetadata = response.json()["album"]
		album_url = "https://play.qobuz.com/album/" + albumMetadata["id"]
		tracks = [response.json()]
	else:
		response = session.post("https://www.qobuz.com/api.json/0.2/album/get?",
			params={
				"album_id": album_id,
			},
		)
		album_url = "https://play.qobuz.com/album/" + album_id
		albumMetadata = response.json()
		tracks = [track for track in albumMetadata["tracks"]["items"]]
	if alcovs == "3":
		album_cover_url = albumMetadata["image"]["large"][:-7] + "max.jpg"
	elif alcovs == "-1":
		pass
	else:
		album_cover_url = albumMetadata["image"][
			("thumbnail", "small", "large")[alcovs]
		]
	download_headers = {
		"range": "bytes=0-", 
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0", 
		"referer": album_url
	}
	base_download_dir = Path(downloadDir)
	album_download_dir = base_download_dir / sanitizeFilename(albumMetadata["artist"]["name"] + " - " + albumMetadata["title"])
	coverobj = pySmartDL.SmartDL(album_cover_url, str(album_download_dir / "cover.jpg"), progress_bar=False, threads=1)
	coverobj.start()
	for track in tracks:
		track_number = tracks.index(track) + 1
		metadata = {
			"ALBUM": albumMetadata["title"],
			"ALBUMARTIST": albumMetadata["artist"]["name"],
			"ARTIST": track["performer"]["name"],
			"COMMENT": comment,
			"COMPOSER": track["composer"]["name"]
						if track.get("composer", False)
						else print("The API didn't return a composer. Tag will be left empty."),
			"COPYRIGHT": track["copyright"],
			"GENRE": albumMetadata["genre"]["name"],
			"ORGANIZATION": albumMetadata["label"]["name"],
			"TITLE": track["title"],
			"TRACKNUMBER": str(track_number),
			"TRACKTOTAL": str(len(tracks)),
			"ISRC": track["isrc"]
		}
		if not comment:
			metadata.pop('COMMENT')
		date_fields = ["release_date_original", "release_date_stream", "release_date_download"]
		date_field = 0
		while not metadata.get("DATE"):
			try:
				metadata["DATE"] = albumMetadata[date_fields[date_field]].split("-")[0]
			except KeyError:
				pass
			date_field += 1
			if date_field == 3:
				print("The API didn't return a date field. Tag will be left empty, \
and you may want to report this on the GitHub with the album URL.")
				metadata["DATE"] = ""
				break
		for field in metadata:
			if getConfig(field, False, "Tags") == "n":
				del metadata[field]
		if getConfig('extendedMetadata', True, 'Tags').lower() == "y" and formatId != "5":
			performers = dict()
			for performerItem in track["performers"].split(" - "):
				person, role = performerItem.split(", ")[:2]
				role = role.upper()
				if role != "UNKNOWN":
					if performers.get(role, False):
						performers[role].append(person)
					else:
						performers[role] = [person]
			for role, people in performers.items():
				if len(people) <= 1:
					metadata[role] = people[0]
				elif len(people) > 1:
					metadata[role + "s"] = ", ".join(people)
		current_time = time.time()
		reqsigt = f"trackgetFileUrlformat_id{formatId}intentstreamtrack_id{track['id']}{current_time}0e47db7842364064b7019225eb19f5d2"
		reqsighst = hashlib.md5(reqsigt.encode('utf-8')).hexdigest()
		responset = session.post("https://www.qobuz.com/api.json/0.2/track/getFileUrl?",
				params={
					"request_ts": current_time,
					"request_sig": reqsighst,
					"track_id": track["id"],
					"format_id": formatId,
					"intent": "stream"
				}
			)
		tr = responset.json()
		isRes = False
		try:
			finalurltr = tr['url']
		except KeyError:
			isRes = True
		else:
			if "restrictions" in tr:
				if "TrackRestrictedByRightHolders" in tr['restrictions']:
					isRes = True 
		if isRes:
			print(f"Track {track_number} is restricted by right holders. Can't download.")
		temporary_filename = album_download_dir / f"{track_number}{fext}"
		songobj = pySmartDL.SmartDL(finalurltr, str(temporary_filename))
		songobj.headers = download_headers
		if formatId == "5":
			albumFormat = "320kbps MP3"
		else:
			try:
				albumFormat = f"{track['maximum_bit_depth']} bits / {track['maximum_sampling_rate']} kHz - {track['maximum_channel_count']} channels"
			except KeyError:
				albumFormat = "Unknown" 
		print(f"Downloading track {track_number} of {len(tracks)}: {track['title']} - {albumFormat}")
		songobj.start()
		if alcovs != "-1":
			albumArt = (album_download_dir / "cover.jpg").open(mode='rb').read()
		else:
			albumArt = ""
		if fext == ".mp3":
			add_mp3_tags(temporary_filename, metadata)
			if alcovs != "-1":
				add_mp3_cover(temporary_filename, albumArt)
		else:
			add_flac_tags(temporary_filename, metadata)
			if alcovs != "-1":
				add_flac_cover(temporary_filename, album_download_dir / 'cover.jpg')
		filename = album_download_dir / sanitizeFilename(f"{str(track_number).zfill(2)}{naming_scheme}{track['title']}{fext}")
		if filename.exists():
			os.remove(filename)
		try:
			os.rename(temporary_filename, filename)
		except OSError:
			print("Failed to rename track. Maybe it exceeds the max path length for your OS.")
	if alcovs != "-1":
		if keep_cover.lower() == "n":
			if (album_download_dir / "cover.jpg").exists():
				os.remove(album_download_dir / "cover.jpg")
		else:
			os.rename(album_download_dir / "cover.jpg", album_download_dir / "folder.jpg")

	if "goodies" in albumMetadata:
		if albumMetadata["goodies"][0]["file_format_id"] == 21:
			print("Booklet available, downloading...")
			bookletobj = pySmartDL.SmartDL(albumMetadata["goodies"][0]["original_url"], str(album_download_dir / "booklet.pdf"))
			bookletobj.headers = download_headers
			bookletobj.start()
		
def getOsType():
	osPlatform = platform.system()
	if osPlatform == 'Windows':
		return True
	else:
		return False

# Untested. Only for compiled builds.
def update(currentVer):
	try:
		latestVer = requests.get("https://thoas.feralhosting.com/sorrow/Qobuz-DL/latestVersion.txt").text.lower()
	except:
		print("Failed to check for update.\n")
	if latestVer != currentVer:
		q = None
		while q not in ("y", "n"):
			q = input(f"New version is available: {latestVer}. You have {currentVer}. Update now? [y/n]").lower()
			if q != "y" or q != "n":
				osCommands('clear')
		if q == "y":
			filename = sys.argv[0]
			if "x64" in filename and "OSX" in filename:
				arch = "OSX_x64"
			elif "x86" in filename and "OSX" in filename:
				arch = "OSX_x86"
			elif "x64" in filename and "Lin" in filename:
				arch = "Lin_x64"
			elif "x86" in filename and "Lin" in filename:
				arch = "Lin_x86"	
			elif "x86" in filename and "Win" in filename:
				arch = "Win_x86.exe"
			elif "x64" in filename and "Win" in filename:
				arch = "Win_x64.exe"
			elif ".py" in filename:
				arch = ".py"
			else:
				print("Cannot determine version: did you rename Qo-DL? If so, please rename it back or download the latest version from the Releases tab on GitHub.")
				time.sleep(5)
				sys.exit()
			if os.path.isdir(f"Qo-DL_{arch}_{latestVer}"):
				shutil.rmtree(f"Qo-DL_{arch}_{latestVer}")
			os.mkdir(f"Qo-DL_{arch}_{latestVer}")
			os.chdir(f"Qo-DL_{arch}_{latestVer}")
			latestInfo = requests.get("http://sorrow.thoas.feralhosting.com/Qobuz-DL/versionLinks.json").json()
			latestBuildURL = latestInfo[arch]
			latestConfigURL = latestInfo["config"]
			print(f"Downloading Qo-DL_{arch}...")
			latestBuild = pySmartDL.SmartDL(latestBuildURL, f"./Qo-DL_{arch}")
			latestBuild.start()
			print("Downloading config file...")
			latestConfig = pySmartDL.SmartDL(latestConfigURL, f"./config.ini")
			latestConfig.start()
			if arch == ".py":
				print("Downloading requirements.txt...")
				latestRequirementsURL = latestInfo["requirements"]
				latestRequirements = pySmartDL.SmartDL(latestRequirementsURL, f"./requirements.txt")
				latestRequirements.start()
			os.chdir('..')
			print(f"Done. Updated build can be found in the 'Qo-DL_{arch}_{latestVer}' folder. Make sure to re-fill config.ini \nExiting...")
			time.sleep(3)
			sys.exit()
		else:
			return

def osCommands(a):
	if a == "pause":
		if getOsType():
			os.system('pause >nul')
		else:
			os.system('read -rsp $\"\"')
	elif a == "clear":
		if getOsType():
			os.system('cls')
		else:
			os.system('clear')
	else:
		if getOsType():
			os.system('title Qo-DL R5c (by Sorrow446 & DashLt)')
		else:
			sys.stdout.write("\x1b]2;Qo-DL R5c (by Sorrow446 & DashLt)\x07")
		
def init():
	if not os.path.exists('config.ini'):
		print("Config file appears to be missing, but this may be a false positive. Please check and re-download the file if necessary.\n\n")
	osCommands('title')
	global msList
	global msList2
	global msList3
	lin = int(0)
	lin2 = int(-1)
	listStatus = ""
	cwd = os.getcwd()
	currentVer = "r5c"
	ssl._create_default_https_context = ssl._create_unverified_context
	msList, msList2, msList3 = [], [], ["appId", "appSecret", "email", "formatId", "password", "namingScheme", "coverSize",  "downloadDir", "keepCover", "useProxy", "proxy", "skipPwHashCheck", "checkForUpdates"]
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
				help='Cover size to fetch. -1 = no cover fetched, 0 = 50x50, 1 = 230x230, 2 = 600x600. 3 = max')
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
	email = getConfig('email', True, 'Main')
	password = getConfig('password', True, 'Main')
	appId = getConfig('appId', False, 'Main')
	appSecret = getConfig('appSecret', False, 'Main')
	useProxy = getConfig('useProxy', True, 'Main')
	skipPwHashCheck = getConfig('skipPwHashCheck', True, 'Main')
	proxy = getConfig('proxy', False, 'Main')
	checkForUpdates = getConfig('checkForUpdates', True, 'Main')
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
		time.sleep(3)
		sys.exit()
	if msList:
		msList = ', '.join(msList)
		print(f"The following required fields in your config file are empty: {msList}.\n"
			   "Please fill them in\n. Press any key to exit.")
		osCommands('pause')
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
			sys.exit(1)
	timeunx = int(time.time())
	global session
	session = requests.Session()
	session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"})
	responset0 = session.post("https://www.qobuz.com/api.json/0.2/user/login?",
		params={
			"email": email,
			"password": password,
			"app_id": appId,
		}
	)
	ssc0 = responset0.json()
	rc = responset0.status_code
	if ssc0.get("message") == "Invalid or missing app_id parameter":
		print("appId in config missing on not working; getting new one...")
		try:
			appId, appSecret = getAppIdAndSecret()
		except BundleError as error:
			if isinstance(error, BundleNotFoundError):
				print("Unable to find URL for bundle.js in login page")
				print("If you raise an issue about this, please include the file login.html.gz, residing in " + os.getcwd(), end="\n\n")
			elif isinstance(error, AppIdNotFoundError):
				print("Unable to get AppId (and possibly appSecret) from bundle.js")
				print("If you raise an issue about this, please include the file bundle.js.gz, residing in " + os.getcwd(), end="\n\n")
			elif isinstance(error, SecretNotFoundError):
				print("Unable to get appSecret from bundle.js")
				print("If you raise an issue about this, please include the file bundle.js.gz, residing in " + os.getcwd(), end="\n\n")
			sys.exit()
		config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
		config.optionxform=str
		config.read('config.ini')
		config.set('Main', 'appId', f'"{appId}"')
		config.set('Main', 'appSecret', f'"{appSecret}"')
		with open("config.ini", "w") as fi:
			config.write(fi)
		print("Obtained new appId and appSecret.")
		responset0 = session.post("https://www.qobuz.com/api.json/0.2/user/login?",
			params={
				"email": email,
				"password": password,
				"app_id": appId,
			}
		)
		ssc0 = responset0.json()
		rc = responset0.status_code
		if ssc0.get("message") == "Invalid or missing app_id parameter":
			print("Obtained appId invalid, exiting...")
			sys.exit()
	session.headers.update({"X-App-Id": appId})
	if rc == 401:
		print("Bad credentials. Exiting...")
		time.sleep(2)
		sys.exit()
	elif rc == 200:
		try:
			ssc1 = ssc0['user']['credential']['parameters']['label']
		except TypeError:
			print("Free accounts are not eligible to get tracks.\nExiting...")
			time.sleep(2)
			sys.exit()
		userAuthToken = ssc0["user_auth_token"]
		session.headers.update(({"X-User-Auth-Token": userAuthToken}))
		if not cline:
			print(f"Signed in successfully - {ssc1} account. \n")
	while True:
		if cline:
			try:
				if txtFilename:
					if not os.path.isfile('config.ini'):
						os.chdir(cwd)
					if os.path.isfile(txtFilename):
						with open(txtFilename) as fin:
							for line in fin:
								listStatus = "ND"
								album_url = line.strip()
								try:
									album_id = getAlbumId(album_url)
								except AttributeError:
									print(f"Invalid URL {album_url}, skipping...")
								isTrack = "/track/" in album_url # could be better, but does it really matter?
							listStatus = "D"						
					else:
						print(f"Specified text file {txtFilename} doesn't exist. Exiting...")
						time.sleep(2)
						sys.exit(1)
			except NameError:
				pass
		if not listStatus or listStatus == "ND":
			try:
				if args.url:
					album_url = args.url
					listStatus = "D"
					try:
						album_id = getAlbumId(album_url)
					except:
						print("Invalid URL. Exiting...")
						time.sleep(1)
						osCommands('clear')
						sys.exit(1)
					isTrack = "/track/" in album_url
			except NameError:
				album_url = input("Input Qobuz Player or Qobuz store URL:")
				try:
					album_id = getAlbumId(album_url)
				except IndexError:
					print("Invalid URL. Returning to URL input screen...")
					time.sleep(1)
					osCommands('clear')
					continue
				isTrack = "/track/" in album_url
		if useProxy == "y":
			session.proxies.update({
				"https":str(proxy)
			})
		rip(album_id, isTrack, session, comment, formatId, alcovs, downloadDir, fp, keepCover)
		if listStatus == "ND":
			print("Moving onto next item in list...")
			time.sleep(1)
			osCommands('clear')
			continue
		elif listStatus == "D":
			print("Exiting...")
			time.sleep(1)
			sys.exit()
		print("Returning to URL input screen...")
		lin = int(0)
		lin2 = int(-1)
		listStatus = ""
		time.sleep(1)
		osCommands('clear')

if __name__ == '__main__':
	init()
