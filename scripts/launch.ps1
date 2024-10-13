# Este archivo es el que se encarga de ejecutar el juego

# Funcionamiento
# -- 
# Este archivo se llama cada vez que el juego se vaya a ejecutar. El install.ps1 ya lo habrá copiado a un directorio del PATH, ya que este 
# archivo es el que ejecuta el juego y activa el entorno virtual y lo desactiva cuando se sale del juego.

# Ruta al directorio del juego
$gameDirectory = "$HOME\Boardtoe"
$venvDirectory = "$gameDirectory\.venv"

# Comprobar si el entorno virtual existe
if (Test-Path $venvDirectory) {
    # Activar el entorno virtual
    & "$venvDirectory\Scripts\Activate.ps1"
    
    # Ejecutar el juego
    python -m src

    # Desactivar el entorno virtual al salir
    deactivate
} else {
    Write-Host "El entorno virtual no existe. Por favor, asegúrate de haber ejecutado el script de instalación."
}
