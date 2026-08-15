
from colorama import Fore, Back, Style, init


init(autoreset=True)

class Colors:

    PRIMARY = Fore.CYAN
    SECONDARY = Fore.MAGENTA
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    INFO = Fore.BLUE
    MUTED = Fore.LIGHTBLACK_EX
    WHITE = Fore.WHITE

 
    BG_PRIMARY = Back.CYAN
    BG_SUCCESS = Back.GREEN
    BG_ERROR = Back.RED
    BG_WARNING = Back.YELLOW


    BOLD = Style.BRIGHT
    DIM = Style.DIM
    RESET = Style.RESET_ALL

    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        return f"{color}{text}{cls.RESET}"

    @classmethod
    def primary(cls, text: str) -> str:
        return cls.colorize(text, cls.PRIMARY)

    @classmethod
    def success(cls, text: str) -> str:
        return cls.colorize(text, cls.SUCCESS)

    @classmethod
    def error(cls, text: str) -> str:
        return cls.colorize(text, cls.ERROR)

    @classmethod
    def warning(cls, text: str) -> str:
        return cls.colorize(text, cls.WARNING)

    @classmethod
    def info(cls, text: str) -> str:
        return cls.colorize(text, cls.INFO)

    @classmethod
    def muted(cls, text: str) -> str:
        return cls.colorize(text, cls.MUTED)

    @classmethod
    def bold(cls, text: str) -> str:
        return cls.colorize(text, cls.BOLD)
