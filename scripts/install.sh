# Script encargado de instalar el juego y sus dependencias en sistemas UNIX/OpenBSD/MacOS

# Funcionamiento
# ---

# El instalador se podrá llamar con un argumento (-v) que indica la verbosidad del instalador.


# 1. Comprobar que Python3.9 está instalado en el sistema.
# 3. Comprobar que el sistema tiene conexión a internet para descargar paquetes desde Pypi
# 4. Verificar si se tienen permisos para escribir en el directorio donde esté ubicado el juego.
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

# Este archivo copia el archivo de ejecucción al PATH.
cp launch.sh /usr/local/bin/boardtoe
chmod +x /usr/local/bin/boardtoe

echo "El script de lanzamiento ha sido instalado como 'boardtoe'."

