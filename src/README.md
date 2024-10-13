# BoardToe 2.0 🎮

BoardToe 2.0 es un juego basado en terminal escrito en **Python** y profundamente influenciado por el famoso juego de mesa "tres-en-raya", pero llevandolo al siguiente nivel. 

En Boardtoe mejoramos la experiencia de juego añadiendo **dimensiones**, donde podrás jugar desde 3 tableros clásicos de 3x3 conectados entre sí hasta un máximo de 3 tableros de 6x6 interconectados entre sí. 
Aunque queremos mantener la esencia del juego, BoardToe tambien proporcina a los jugadores **diferentes tokens** mas allá del círculo o la cruz, diversos modos de juego como el contrareloj,invertido o el restringido, y una **IA incorporada** con diferentes dificultades esperando a ser derrotada 🤖🧨.

[NEW] También se tendrá la posibilidad de poder jugar desde diferentes dispositivos que estén conectados a la misma red local.


## Instalacion 📦

> [!IMPORTANT]
> Boardtoe necesita **Python 3.9** o una versión superior para poder ejecutarse
> Adicionalmente, se recomienda que Python esté instalado en el **PATH**.

Dado que Python no viene instalado por defecto en todos los sitemas operativos, necesitarás tener Python instalado en tu sistema.
Si tienes permiso para instalar paquete en el interprete global, la instalación será un poco mas rápida y fácil.
Si no es el caso, también ofrecemos una opción sencilla, pero un poco mas costosa a cambio de comandos.

## 🔧 Pasos

> [!NOTE]
> Siguiendo estos pasos instalarás Boardtoe en la carpeta HOME (~/$HOME).
> Puedes cambiar esta ruta a otra diferente, aunque se recomienda que sea un lugar común para aplicaciones y ejecutables.


## 🐍 Si tienes Python instalado en tu sistema:
#### Instalando ``boardtoe`` en el interprete global de tu sistema:
```sh
# Lo instalamos
pip install boardtoe

#Si python estaba instalado en el PATH, se habrá instalado boardtoe como un enlace simbolico. 
#Lo ejecutamos
boardtoe
# -- Eso es todo
```

### Linux/OpenBsd/MacOS
---

#### 1. Instala BoardToe desde el repositorio oficial de Github usando ``curl``: 
```sh

# Nos posicionamos en la carpeta del usuario
cd ~

curl [-L] -o ~/Boardtoe.tar.gz https://github.com/Backist/Boardtoe/archive/refs/heads/main.tar.gz
# OPCIONAL: -L puede no funcionar siempre e indica que curl seguirá redirecciones.
# -o ~/Boardtoe.zip indica la ruta de destino, en este caso la carpeta HOME.
```

#### 2. Descomprime el ``.tar.gz`` instalado que contiene los archivos del juego
```sh
# tar viene preinstalado en casi todas las versiones de linux
tar -xvzf ./Boardtoe.tar.gz
# Si tienes unzip instalado, puedes usarlo si lo prefieres
unzip ./Boardtoe.tar.gz


# Debido a que Github comprime dos veces, debemos renombrar la carpeta y eliminar la carpeta temporal.
mv Boardtoe/BoardToe-main/* Boardtoe/
rmdir Boardtoe/BoardToe-main
```

#### 3. Ejecuta el instalador del juego
Este instalador se encargará de instalar las dependencias necesarias para instalar el juego.
Para ello crearemos un entorno virtual en la carpeta del juego e instalaremos las dependencias. De esta manera
podemos aislar el juego para que las dependencias no interfieran con la configuracion de Python del usuario.

> [!WARNING]
> Para ejecutar el instalador se necesitan permisos de ejecucción.


```sh
# Entramos en el directorio del juego 
cd ./Boardtoe

# Damos permisos de ejecucion al archivo para evitar errores.
# -R dará permiso a que los ejecutables puedan funcionar correctamente
chmod -R +x ./scripts
# Llamamos al instalador
./install.sh -v
# -v indica que será verboso en sus operaciones
```

#### 4. 🎊 Genial! Boardtoe ya ha sido instalado en tu sistema y ahora puedes ejecutarlo en la terminal de la siguiente manera:

**[DESAROLLADOR]** Para que el usuario pueda hacer boardtoe y pueda jugar, es neceario instalar boardtoe en PATH.
Como eso a veces no es posible (y además es mas trabajo), lo suyo sería usar ``python -m boardtoe``. Problema?
Que el usuario se tiene que desplazar al directorio fuente siempre que lo quiera ejecutar.

```sh
boardtoe
python -m boardtoe (si no está en PATH + tendrías que meterme a la carpeta para jugarlo.)
```


### Windows
---

#### Abre una ``PowerShell`` con ``Permisos de administrador``:

1. Usando la tecla inicio
2. ``Win + X`` y selecciona **Windows PowerShell (Administrador)**

#### 1. Instala BoardToe desde el repositorio oficial de Github usando ``curl``: 
 
A partir de la versión 1803 de ``Windows 10``, ``curl`` viene preinstalado por defecto en el sistema.

```bash
# Nos movemos a la carpeta %HOME
cd $HOME

# Usamos curl para descargar el .zip
curl [-L] -o .\Boardtoe.zip https://www.github.com/Backist/Boardtoe/archive/refs/heads/main.zip

# OPCIONAL: -L puede no funcionar siempre e indica que curl seguirá redirecciones.
# -o ~/Boardtoe.zip indica la ruta de destino, en este caso la carpeta HOME.

# -----
# Si tienes una version anterior de windows, puedes probar usando Invoke-Request
Invoke-WebRequest -Uri "https://www.github.com/Backist/Boardtoe/archive/refs/heads/main.zip" -OutFile ".\Boardtoe.zip"
```

#### 2. Descomprime el ``.zip`` instalado que contiene los archivos del juego

Si lo prefieres, usa tu herramienta de terceros para descomprimirlo o el propio menu contextual de windows.

```ps1
Expand-Archive -Path .\Boardtoe.zip -DestinationPath .\Boardtoe

# Debido a que Github comprime dos veces, debemos renombrar la carpeta y eliminar la carpeta temporal.
Move-Item -Path "Boardtoe\BoardToe-main\*" -Destination "Boardtoe"
Remove-Item -Path "Boardtoe\BoardToe-main" -Recurse
```

#### 3. Ejecuta el instalador del juego
Este instalador se encargará de instalar las dependencias necesarias para instalar el juego.
Para ello crearemos un entorno virtual en la carpeta del juego e instalaremos las dependencias. De esta manera
podemos aislar el juego para que las dependencias no interfieran con la configuracion de Python del usuario.

```bash
# Damos permisos a Powershell para ejecutar scripts (solo al user)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser


# Llamamos al instalador
./install.ps1 -v
# -v indica que será verboso en sus operaciones
```

#### 4. Genial! Boardtoe ya ha sido instalado en tu sistema y ahora puedes ejecutarlo en la terminal de la siguiente manera:

**[DESAROLLADOR]** Para que el usuario pueda hacer boardtoe y pueda jugar, es neceario instalar boardtoe en PATH.
Como eso a veces no es posible (y además es mas trabajo), lo suyo sería usar ``python -m boardtoe``. Problema?
Que el usuario se tiene que desplazar al directorio fuente siempre que lo quiera ejecutar.

```bash 
boardtoe
python -m boardtoe (si no está en PATH + tendrías que meterme a la carpeta para jugarlo.)
```


## Plataformas compatibles


| Plataforma | README |
| ------ | ------ |
| Windows 7-8 or lower | ⚠️ |
| Windows 10/11 | ✅ |
| Linux (Arch, Ubuntu, Manjaro, Debian, ...) | ✅ |
| Mac | ✅* |


## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
