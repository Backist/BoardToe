# Script encargado de instalar el juego y sus dependencias en sistemas UNIX/OpenBSD/MacOS

# Funcionamiento
# ---

# El instalador se podrá llamar con un argumento (-v) que indica la verbosidad del instalador.


# 1. Comprobar que Python3.9 está instalado en el sistema.
# 3. Comprobar que el sistema tiene conexión a internet para descargar paquetes desde Pypi
# 4. Verificar si se tienen permisos para escribir en el directorio donde esté ubicado el juego (para crear la carpeta del entorno virutal).
    4.1 La razón es porque en vez de instalar las dependencias y ensuciar el interprete global, lo hacemos con un entorno virtual.
# 5. Verificar si ``Poetry`` está instalado en el interprete global de Python.
#     5.1 Si lo está, hacemos lo siguiente:
#     - poetry set config virtualenv.in-project false
#     - poetry shell
#     - poetry install -> Esto por defecto estará configurado para instalar las dependencias necesarias.
# 6. Si ``Poetry `` no está instalado en el sistema, entonces crear el entorno virutal usando el modulo por defecto de Python
#     - >>> python -m venv .venv
#     - >>> source ./.venv/bin/activate
#     - >>> pip install [dependencias en archivo pyproject.toml o requirements.txt]
# 7. Agregar el juego al PATH:


# Este archivo es el que se encarga de instalar el juego y configurar el entorno

# Ruta al directorio del juego
$gameDirectory = "$HOME\Boardtoe"
$venvDirectory = "$gameDirectory\.venv"
$launchScript = "$gameDirectory\launch.ps1"

# Comprobar si el directorio del juego existe, si no, crearlo
if (-Not (Test-Path $gameDirectory)) {
    New-Item -ItemType Directory -Path $gameDirectory
    Write-Host "Directorio de juego creado en: $gameDirectory"
}

# Comprobar si el entorno virtual ya existe
if (-Not (Test-Path $venvDirectory)) {
    # Crear el entorno virtual
    python -m venv $venvDirectory
    Write-Host "Entorno virtual creado en: $venvDirectory"
} else {
    Write-Host "El entorno virtual ya existe en: $venvDirectory"
}

# Activar el entorno virtual
& "$venvDirectory\Scripts\Activate.ps1"

# Instalar las dependencias
$requirementsFile = "$gameDirectory\requirements.txt"
if (Test-Path $requirementsFile) {
    pip install -r $requirementsFile
    Write-Host "Dependencias instaladas desde: $requirementsFile"
} else {
    Write-Host "No se encontró el archivo requirements.txt en: $gameDirectory"
}

# Copiar el script de lanzamiento a un directorio en el PATH
$targetPath = "C:\Program Files\Boardtoe"
if (-Not (Test-Path $targetPath)) {
    New-Item -ItemType Directory -Path $targetPath
    Write-Host "Directorio de destino creado en: $targetPath"
}

# Copiar el script a la carpeta del sistema
Copy-Item -Path $launchScript -Destination "$targetPath\boardtoe.ps1" -Force
Write-Host "El script de lanzamiento se ha copiado a: $targetPath\boardtoe.ps1"

# Añadir el directorio al PATH
$envPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
if (-Not $envPath.Contains($targetPath)) {
    [System.Environment]::SetEnvironmentVariable("Path", $envPath + ";$targetPath", [System.EnvironmentVariableTarget]::User)
    Write-Host "El directorio se ha añadido al PATH. Por favor, reinicia PowerShell o abre una nueva ventana para aplicar los cambios."
} else {
    Write-Host "El directorio ya estaba en el PATH."
}

# Desactivar el entorno virtual (opcional)
deactivate

