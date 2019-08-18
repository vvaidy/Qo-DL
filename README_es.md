# Qo-DL
Herramienta escrita en Python para descargar MP3s & FLACs de Qobuz.

Por favor, [únete a nuestro server de Discord](https://discord.gg/2WGqT7B). Estamos experimentando con bots :).

[Binarios pre-compilados.](https://github.com/Sorrow446/Qo-DL/releases)

**Una nueva versión del archivo "config.ini" es usualmente requerida en cada versión nueva**     
**Aquí hay una [imagen](https://imgur.com/a/bUQJU8q) que indica cómo conseguir la última versión del archivo mencionado arriba**   

Las versiones anteriores están alojadas [aquí](https://thoas.feralhosting.com/sorrow/Qobuz-DL/Old%20Builds/).

![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/GUI3.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/GUI1.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/GUI2.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/b1.jpg)
![](https://thoas.feralhosting.com/sorrow/Qobuz-DL/b2.jpg)


# Configuración
## Obligatorio ##
Estos datos deben ser incluidos obligatoriamente en el config.ini:
- Dirección de email
- ID del formato - calidad de descarga (5 = 320 kbps MP3, 6 = 16-bit FLAC, 7 = 24-bit / =< 96kHz FLAC, 27 = best avail - 24-bit / >96 kHz =< 192 kHz FLAC).
- Contraseña encriptada en MD5 - sin embargo, como en la versión 5, también puedes introducirla en texto plano si quieres.
 
**No puedes descargar ninguna canción con una cuenta sin plan.**
## Opcional ##

- Tags: Cambia a "n" en las partes que quieras omitir.  
Todo lo demás está documentado en el config.ini.

# Uso
Primero, llena el config.ini.
### Windows ###
Ejecuta el exe.
### Linux & macOS ###
Utiliza el comando 'cd' para acceder a la carpeta en que todo lo de este repositorio está descargado.
```
cd Desktop
```
Dale permisos de ejecutable.
```
chmod +x Qo-DL_Lin_x64
```
Ejecutalo.
```
./Qo-DL_Lin_x64
```
### Android ###
1. Primero, identifica el tipo de arquitecura de tu celular. Puedes usar [esta app para ello](https://play.google.com/store/apps/details?id=com.inkwired.droidinfo). 
Fíjate debajo de "Instruction Sets." La mayoría de los celulares Android modernos son ARM o ARM64.

2. Descarga los respectivos archivos de este repositorio a tu celular. En este caso, los descargaremos en: /storage/emulated/0/download.

3. Descarga e instala Termux. Andoid 5.0 / Lollipop o nuevo?

4. Corre Termux

5. Dale acceso a tus archivos.
```
termux-setup-storage
```
Los usuarios con root pueden saltarse este paso. Los usuarios sin root sólo pueden ejecutar Qo-DL en la carpeta "home" de Termux.

6. Mueve los archivos del repositorio a la carpeta "home" de Termux. No te olvides el fullstop al final ("."), ignora los errores que aparezcan.
```
mv /storage/emulated/0/download/Qo-DL_ARM64 /storage/emulated/0/download/config.ini .
```
7. Hazlo ejecutable.
```
chmod +x Qo-DL_ARM64
```
8. Ejecútalo.
```
./Qo-DL_ARM64
```

Qo-DL puede ser también usado en la línea de comandos.   
**Asegúrate de ubicarte en el directorio de Qo-DL antes de ejecutarlo o no podrá leer el archivo de configuración.**  
```
uso: Qo-DL.py [-h] [-url URL] [-q Q] [-p P] [-list LIST] [-c C] [-s S]
                   [-k K] [-proxy PROXY] [-comment COMMENT]

argumentos opcionales:
  -h, --help        muestra este mensaje de ayuda y cierra la aplicación.
  -url URL          URL de Qobuz Player o Qobuz Store.
  -q Q              Calidad de la descarga. 5 = 320 kbps MP3, 6 = 16-bit FLAC, 7 =
                    24-bit / =< 96kHz FLAC, 27 = best avail - 24-bit / >96 kHz
                    =< 192 kHz FLAC. Si la calidad elegida no está disponible, la
                    siguiente "mejor" opción será usada.
  -p P              Dónde se descargarán los archivos. Asegúrate de ponerlo entre comillas dobles.
  -list LIST        Descarga desde una lista de URLs. -list <archivo txt>.
  -c C              Tamaño de la portada. 1 = 230x230, 2 = 600x600.
  -s S              Esquema de los archivos. 1 = "01. ", 2 = "01 -"
  -k K              Deja el folder.jpg dentro del directorio del álbum. Y o N.
  -proxy PROXY      <IP address>:<port>. Debe ser https. Esto no puede ser usado para
                    evadir las restricciones regionales de Qobuz. 
                    Sólo sirve pare prevenir un 404.
                    
  -comment COMMENT  Comentario personalizado.
  -embed EMBED      Adiciona portadas incrustadas a las canciones. "Y" o "N".