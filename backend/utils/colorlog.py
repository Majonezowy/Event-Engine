import logging
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }
    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        msg = super().format(record)
        return f"{color}{msg}{Style.RESET_ALL}"

logger = logging.getLogger("event_engine")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter("[%(asctime)s] %(levelname)s: %(message)s", "%H:%M:%S"))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
logger.propagate = False
