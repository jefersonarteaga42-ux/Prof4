"""
Modulo de configuracion de logs.
Registra todos los eventos operativos y excepciones en 'sistema_software_fj.log'
sin usar bases de datos.
"""

import logging


def configurar_logger(nombre_archivo: str = "sistema_software_fj.log") -> logging.Logger:
    """Inicializa y retorna un logger configurado para archivo y consola."""
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(nombre_archivo, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formato)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formato)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
