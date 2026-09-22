import os

import fuentes  # noqa: F401  registra las fuentes al importarse

FONDO = "#010409"
PRIMARIO = "#29c4d9"
SECUNDARIO = "#8dbccd"
CLARO = "#eaf6fc"
BLANCO = "#ffffff"

AMBAR = "#caa655"
MORADO = "#ac94f1"
VERDE = "#48d0a5"
ROJO = "#e06c75"

RAMA_MAIN = PRIMARIO
RAMA_FEATURE = MORADO
STAGING = AMBAR
OK = VERDE
ERROR = ROJO

ACENTO = PRIMARIO
GRIS = SECUNDARIO

SUPERFICIE = "#04121a"

FONT = "JetBrains Mono"
FONT_TITULO = "Press Start 2P"

RAIZ = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(RAIZ, "assets")

TAM_TITULO = 30
