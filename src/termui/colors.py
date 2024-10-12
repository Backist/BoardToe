
class Color:
    """
    Clase estatica que agrupa los colores representables en terminales de hasta 16 colores.
    """
    
    BLACK = '\033[30m'   # Negro
    RED = '\033[31m'     # Rojo
    GREEN = '\033[32m'   # Verde
    YELLOW = '\033[33m'  # Amarillo
    BLUE = '\033[34m'    # Azul
    MAGENTA = '\033[35m' # Magenta
    CYAN = '\033[36m'    # Cian
    WHITE = '\033[37m'   # Blanco
    LIGHT_GRAY = '\033[37m' # Gris claro
    DARK_GRAY = '\033[90m'   # Gris oscuro
    LIGHT_RED = '\033[91m'    # Rojo claro
    LIGHT_GREEN = '\033[92m'  # Verde claro
    LIGHT_YELLOW = '\033[93m' # Amarillo claro
    LIGHT_BLUE = '\033[94m'    # Azul claro
    LIGHT_MAGENTA = '\033[95m' # Magenta claro
    LIGHT_CYAN = '\033[96m'    # Cian claro
    LIGHT_WHITE = '\033[97m'   # Blanco claro

    @staticmethod
    def all_colors():
        """Devuelve todos los colores básicos."""
        return [getattr(Color, color) for color in dir(Color) if not color.startswith('__') and color != 'all_colors']


class TrueColor:
    """
    Clase estatica que agrupa algunos de los principales colores representables en terminales 
    con soporte de 256 (8-bit) colores.
    
    La gran mayoria de ellos son colores cuyos nombres fueron inicialmente atribuidos
    en HTML como acceso rapido a algunos de los mas usados.
    """
    
    DARKKHAKI = '\033[38;2;189;183;107m'  # Dark Khaki
    MARINE = '\033[38;2;0;0;128m'          # Marine
    LIGHTCORAL = '\033[38;2;240;128;128m'  # Light Coral
    LIGHTSALMON = '\033[38;2;255;160;122m'  # Light Salmon
    PALEGREEN = '\033[38;2;152;251;152m'   # Pale Green
    LIGHTSEAGREEN = '\033[38;2;32;178;170m' # Light Sea Green
    LIGHTSKYBLUE = '\033[38;2;135;206;250m' # Light Sky Blue
    PLUM = '\033[38;2;221;160;221m'        # Plum
    LIGHTYELLOW = '\033[38;2;255;255;224m' # Light Yellow
    KHAKI = '\033[38;2;240;230;140m'       # Khaki
    LIGHTGOLDENRODYELLOW = '\033[38;2;250;250;210m'  # Light Goldenrod Yellow
    THISTLE = '\033[38;2;216;191;216m'     # Thistle
    CORAL = '\033[38;2;255;127;80m'        # Coral
    DEEPSKYBLUE = '\033[38;2;0;191;255m'   # Deep Sky Blue
    DARKSALMON = '\033[38;2;233;150;122m'  # Dark Salmon
    PALEVIOLETRED = '\033[38;2;219;112;147m'  # Pale Violet Red
    MISTYROSE = '\033[38;2;255;228;225m'   # Misty Rose
    PEACHPUFF = '\033[38;2;255;218;185m'   # Peach Puff
    ORCHID = '\033[38;2;218;112;214m'      # Orchid
    SANDYBROWN = '\033[38;2;244;164;96m'   # Sandy Brown
    LAVENDER = '\033[38;2;230;230;250m'    # Lavender
    TOMATO = '\033[38;2;255;99;71m'        # Tomato
    LIGHTPINK = '\033[38;2;255;182;193m'   # Light Pink
    IVORY = '\033[38;2;255;255;240m'       # Ivory
    MEDIUMSLATEBLUE = '\033[38;2;123;104;238m'  # Medium Slate Blue
    CADETBLUE = '\033[38;2;95;158;160m'    # Cadet Blue
    NAVAJOWHITE = '\033[38;2;255;222;173m' # Navajo White
    SLATEBLUE = '\033[38;2;106;90;205m'    # Slate Blue
    SPRINGGREEN = '\033[38;2;0;255;127m'   # Spring Green
    LIGHTCYAN = '\033[38;2;224;255;255m'   # Light Cyan
    GHOSTWHITE = '\033[38;2;248;248;255m'  # Ghost White
    LIGHTSTEELBLUE = '\033[38;2;176;196;222m' # Light Steel Blue
    DARKORANGE = '\033[38;2;255;140;0m'    # Dark Orange
    DODGERBLUE = '\033[38;2;30;144;255m'   # Dodger Blue
    MEDIUMPURPLE = '\033[38;2;147;112;219m' # Medium Purple

    @staticmethod
    def all_colors():
        """Devuelve todos los colores especiales."""
        return [getattr(TrueColor, color) for color in dir(TrueColor) if not color.startswith('__') and color != 'all_colors']


class Style:
    """
    Clase estatica que agrupa los principales estilos de codigos ANSI.
    """

    # Códigos de escape para estilos de texto
    BOLD = '\033[1m'                # Negrita
    DIM = '\033[2m'                  # Atenuado
    ITALIC = '\033[3m'               # Cursiva
    UNDERLINE = '\033[4m'            # Subrayado
    BLINKING = '\033[5m'             # Parpadeante
    REVERSED = '\033[7m'             # Inversión de colores (fondo y texto)
    HIDDEN = '\033[8m'               # Texto oculto
    STRIKETHROUGH = '\033[9m'        # Tachado
    
    @staticmethod
    def all_styles():
        """Devuelve todos los estilos disponibles."""
        return [getattr(Style, style) for style in dir(Style) if not style.startswith('__') and style != 'all_styles']
    
    
class ResetSequence:
    """
    Clase estatica que agrupa las principales secuencias de escape ANSI 
    para reiniciar ciertos estilos de la terminal.
    """
    
    
    BOLD = "\033[22m"
    DIM = "\033[22m"
    ITALIC = "\033[23m"  
    UNDERLINE = "\033[24m"
    BLINKING = "\033[25m"
    REVERSE = "\033[27m"
    HIDDEN = "\033[28m"
    STRIKETHROUGH = "\033[29m"
    
    ALL = '\033[0m'             



if __name__ == '__main__':
    # Colors
    print(f"{Color.RED}Este texto es rojo{Color.RESET}")
    print(f"{Color.GREEN}Este texto es verde{Color.RESET}")
    print(f"{Color.BLUE}Este texto es azul{Color.RESET}")

    # Truecolors
    print(f"{TrueColor.DARKKHAKI}Este texto es Dark Khaki{Color.RESET}")
    print(f"{TrueColor.MARINE}Este texto es Marine{Color.RESET}")
    print(f"{TrueColor.LIGHTCORAL}Este texto es Light Coral{Color.RESET}")


    # Styles
    print(f"{Style.BOLD}Este texto es negrita{Style.RESET}")
    print(f"{Style.DIM}Este texto está atenuado{Style.RESET}")
    print(f"{Style.ITALIC}Este texto es cursiva{Style.RESET}")
    print(f"{Style.UNDERLINE}Este texto está subrayado{Style.RESET}")
    print(f"{Style.BLINKING}Este texto parpadea{Style.RESET}")
    print(f"{Style.REVERSED}Este texto tiene colores invertidos{Style.RESET}")
    print(f"{Style.HIDDEN}Este texto está oculto{Style.RESET}")
    print(f"{Style.STRIKETHROUGH}Este texto está tachado{Style.RESET}")