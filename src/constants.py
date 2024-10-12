"""
Game constants
"""

from platform import system


# def get_os_info():
#     # Obtener el nombre del sistema operativo
#     os_name = platform.system()
#     os_version = platform.version()
#     os_release = platform.release()

#     print(f"Sistema Operativo: {os_name}")
#     print(f"Versión: {os_version}")
#     print(f"Liberación: {os_release}")

#     # Información adicional dependiendo del sistema operativo
#     if os_name == "Windows":
#         print("Información adicional: ", os.environ['OS'])
#     elif os_name == "Linux":
#         print("Distribución: ", platform.linux_distribution() if hasattr(platform, 'linux_distribution') else "N/A")
#     elif os_name == "Darwin":
#         print("Información adicional: macOS")

# get_os_info()


IS_WINDOWS: bool = system() == 'Windows'
IS_MAC: bool = system() == 'Darwin'
IS_LINUX: bool = system() == 'Linux'

