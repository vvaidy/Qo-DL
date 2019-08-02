Traduzione di Cuntstantin:
# Qo-DL
Strumento creato con Python per scaricare file mp3 & FLAC da Qobuz.

Unitevi [al nostro server Discord](https://discord.gg/2WGqT7B). Stiamo sperimentando con i BOT :) .
[Binari precompilati.](https://github.com/Sorrow446/Qo-DL/releases)
#
**� richiesto il nuovo modello di configurazione dalla versione 5c in poi**
**Se volete scaricare playlist dovete usare [questo modello di configurazione](https://thoas.feralhosting.com/sorrow/Qobuz-DL/config.ini) **

Le versioni precedenti si possono trovare [qui](https://thoas.feralhosting.com/sorrow/Qobuz-DL/Old%20Builds/).

![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/GUI3.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/GUI1.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/GUI2.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/b1.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/b2.jpg)

# Impostazioni
##Obbligatorio##
I seguenti campi devono essere compilati nel file config:
- Indirizzo email
- Format id - formato/qualit� del file (5 = 320 kbps, 6 = 16-bit FLAC, 7 = 24-bit / =< 96kHz FLAC,  27 = la qualit� migliore disponibile - 24-bit / >96 kHz =< 192 kHz FLAC).
- Password criptata in MD5 hash - dalla versione 5 in poi, potete semplicemente scrivere la password in testo normale.

**Non potete scaricare nessuna traccia con un account FREE**
## Opzionale ##

- Tag : cambiate il valore a "n" per non scaricare nessun tag nel file.
Tutto il resto si pu� trovare nel file config.ini

# Utilizzo 
Compilate i campi richiesti nel file config.
### Windows ###
Avviate il file .exe
### Linux & macOS ###
CD al file exe
```
cd Desktop
```
Fatelo diventare un eseguibile
```
chmod +x Qo-DL_Lin_x64
```
Avviatelo.
```
./Qo-DL_Lin_x64
```

### Android ###
1 .  Scoprite l�architettura della CPU del vostro dispositivo e scegliete la versione corrispondente. Potete utilizzare [questa app] (https://play.google.com/store/apps/details?id=com.inkwired.droidinfo).
Guardate sotto �Instruction Sets.� . La maggior parte dei dispositivi android oggi utilizzano ARM o ARM64.

2.  Scaricate la versione che corrisponde con il vostro dispositivo e il file config sul vostro dispositivio. In questa guida scaricheremo entrambi i file in: /storage/emulated/0/download.

3.  Scaricate e installate Termux dal Play Store. � richiesta una versione di android almeno 5.0 / Lollipop.

4.  Avviate Termux

5.  Consentite l�accesso ai vostri file.
```
impostazioni termux-storage
```
Se il vostro dispositivo � rootato potete saltare questi passi. Se il vostro dispositivo non � rootato potete avviare Qo-DL solo dalla cartella home in Termux.

6. Spostate la versione scaricata e il file config nella cartella home in Termux. Non dimenticatevi del punto alla fine, ignornate gli errori di �ownership�.
mv /storage/emulated/0/download/Qo-DL_ARM64 /storage/emulated/0/download/config.ini .
```
7. Fatelo diventare un eseguibile
```
chmod +x Qo-DL_ARM64
```
8. Avviatelo.
```
./Qo-DL_ARM64
```

Qo-DL pu� essere utilizzato anche attraverso il command line.
**Assicuratevi che lo indirizzate nella cartella di Qo-DL altrimenti il file config non sar� letto correttamente.**
```
Utilizzo : Qo-DL.py [-h] [-url URL] [-q Q] [-p P] [-list LIST] [-c C] [-s S]
                   [-k K] [-proxy PROXY] [-comment COMMENT]

argomenti opzionali:
-h, --help               verr� visualizzato questo messaggio.
- url URL                URL di Qobuz Player o Qobuz Store.
-q Q                     Qualit� del file. 5 = 320 kbps MP3, 6 = 16-bit FLAC, 7 =
                         24-bit / =< 96kHz FLAC, 27 = best avail - 24-bit / >96 kHz
                         =< 192 kHz FLAC. Se la qualit� scelta non � disponibile sar� automaticamente scelta la qualit� migliore disponibile.
-p P                     Dove vengono scaricati i file. Assicuratevi di Aggiungere le virgolette all�inizio e alla fine.
-list LIST               Scaricate da una lista di URL . �list <txt nomedelfile>
-c C                     Dimensione della cover. 1 = 230x230, 2 = 600x600.
-s S                     Denominazione dei file. 1 = "01. ", 2 = "01 -"
-k K                     Lasciare la cover in .jpg nella cartella dell�album. Y (s�) o N (no) .
-proxy PROXY             <IP address>:<port>. Deve contenere https. Non pu� essere usato per bypassare le restrizioni geografiche ma solo per prevenire errori 404.
-comment COMMENT         Commento personalizzato. Potete anche scrivere �URL� per inserire la url dell�album in questo campo. Assicuratevi di aggiungere le virgolette all�inizio e alla fine.
-embed EMBED             Aggiungete la cover dell�album nel file. �Y� o �N�.
```
Qobuz-DL Playlist pu� essere usato anche attraverso il command line, ma per il momento supporta solo un comando.
```
Qobuz-DL_Playlist_x64.exe https://play.qobuz.com/playlist/1285066


#Altre informazioni
Creato con Python v3.6.7.
Gli utenti possono scegliere quali tag vogliono presenti nei file.

Altro:
- Se � disponibile una copertina digitale verr� scaricate insieme ai file nella cartella dell�album.
- I video devono essere acquistati. Qo-DL non � ancora in grado di scaricare video (L�API mostra �None� quando richiede un video)
- I file scaricati si trovano nella cartella �Qo-DL Downloads�. Es. (cartella Qo-DL) \\Qo-DL Downloads\\(albumartist) - (albumtitle)\\(tracks)
-Tutti I caratteri speciali che non sono sopportati da windows verranno scambiati con �-�.
- Se la cartella di un album deve essere creata, ma c�� gi� una cartella con lo stesso nome, la cartella che gi� c�� verr� cancellata, cancellando tutti i file che contiene.
- Se una traccia non � disponibile in streaming verr� saltata (alcuni file su qobuz non possono essere streamati, ma solo acquistati).
- ID3v2.4 tag � utilizzato per i tag dei file mp3.
-**Se i seguenti file sono gi� presenti nella cartella dove vengono scaricati i file, saranno cancellati: (1-1000).flac/.mp3, cover.jpg, booklet.pdf.**

Se avete bisogno di aiuto e siete troppo impazienti per utilizzare Github Issues o per domande in generale, potete contattarci su discord:
* DashLt: Dash#0297 (se avete bisogno di aiuto e non sarete pazienti, non lo sar� neanche io)
* Sorrow446: Sorrow#5631

# Alcuni problemi dei quali siamo al corrente
-Album che hanno pi� di un disco saranno riconosciuti comunque come un album di un solo disco.
Per essere pi� chiari, la prima traccia del secondo CD non sar� denominata traccia #1, ma continuer� la numerazione dall�ultimo numero dell�ultima traccia del primo CD.

- Il cinese, giapponese e coreano non saranno scritti correttamente nella console, questo comunque non presenter� problemi con i file scaricati, avranno i tag corretti.
-Se la riga �Downloading track x out of y� � troppo lunga per la console sar� spammata nella console invece di essere scritta su una riga singola.
Si pu� aggiustare settando la lunghezza e larghezza prima di avviare l�eseguibile, cos�:
���
REM 200 & 30 dovrebbero bastare
MODE CON cols=200 lines=30
QO-DL_X64.EXE
���
Si pu� risolvere anche aggiustando le dimensioni della finestra console manualmente. Le versioni linux hanno lo stesso problema.
-Le API hanno un limite di 500 tracce per playlist. 

# Risoluzione dei problemi
-Se ricevete questo messaggio e siete sicuri al 100% che il link che state inserendo � corretto, dovete o usare un VPN oppure abilitare l�opzione proxy nel file config. ** Questo messaggio non ha nulla a che fare con le restrizioni geografiche. Non c�� nulla che si pu� fare a riguardo dato che la regione � collegata al vostro account.**
���
Not found (404). Bad URL? Returning to URL input screen...
���
-Se ricevete questo messaggio ogni volta che cercato di scaricare un album, avete bisogno di un nuovo uat oppure l�app id + sec sono scaduti. Per ricever un nuovo uat, cancellate l�uat nel file config.ini e avviate Qo-DL. Vi sar� assegnato uno nuovo. Incollatelo nel vostro file config. Se ricevete questo messaggio per alcuni album in particolare, l�album oppure alcune tracce non sono disponibili nella vostra regione.
���

"Track <num> is restricted by right holders. Can't download."
���
-	Ho impostato la qualit� a -27, e l�album su Qobuz Player viene mostrato come 24-bit, Qo-DL comunque scarica un file flac 16 bit, o un formato inferiore.
Spiegazione semplice, Qobuz non mostra correttamente la qualit� massima del file. Es. 

```
https://play.qobuz.com/album/qi7icfdkslpva

Provate a riprodurre la traccia dal player in 24/96. Forse avr� qualcosa a che fare con i diritti d�autore della casa discografica?
-Quando aggiornate a una versione 5> da una versiona inferiore senza scaricare il nuovo config:
��
Se il file config � gi� presente nella vostra cartella, potete semplicemente cancellare la riga 13 e sostiturila con la riga 13 del nuovo file config.

#Diniego

Non sono responsabile per come utilizzate Qo-DL o Qo-DL playlist.
Qo-DL o Qo-DL Playlist non bypassano i blocchi regionali imposti da Qobuz.
Qo-Dl & Qo-DL Playlist utilizzano l�Api Qobuz, ma non sono approvati o certificati da Qobuz in nessun modo.
Il marchio Qobuz � un marchio registrato e appartiene ai rispettivi proprietari.
Qo-DL & Qo-DL Playlist non hanno un partnership o sono sponsorizzati o approvati da Qobuz.
Utilizzando Qo-DL & Qo-DL Playlist state accettando i seguenti termini: http://static.qobuz.com/apps/api/QobuzAPI-TermsofUse.pdf
