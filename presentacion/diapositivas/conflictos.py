from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    VGroup,
)

from animaciones import teclear
from componentes import ALTO_BARRA, linea_terminal, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import CLARO, ERROR

TITULO = "merge conflicts"

TAM = 16
ANCHO_PANEL = 6.4
ALTO_PANEL = 5.1
MARGEN = 0.4
BUFF = 0.2
X_ARCHIVO, X_TERMINAL = -3.5, 3.5
Y_PANEL = -0.25
NOMBRE = "media.py"
RAMA = "redondeo"

CONFLICTO = (
    ("def media(datos):", "txt"),
    ("    m = sum(datos) / len(datos)", "txt"),
    ("<<<<<<< HEAD", "ok"),
    ("    return m", "ok"),
    ("=======", "out"),
    ("    return round(m, 2)", "alt"),
    (f">>>>>>> {RAMA}", "alt"),
)
SANGRIA_CONFLICTO = {1: 4, 3: 4, 5: 4}
ANTES = ("    return m", 4)
FILA_ANTES = 2
MARCAS = (2, 3, 4, 5, 6)

FUERA = (2, 3, 4, 6)
QUEDA = 5
SLOT_QUEDA = 2

PROMPT = (("", "cmd"),)

MERGE = (
    ("git switch main", "cmd"),
    ("", "sep"),
    (f"git merge {RAMA}", "cmd"),
    (f"Auto-merging {NOMBRE}", "out"),
    (f"CONFLICT: Merge conflict in {NOMBRE}", "err"),
    ("Automatic merge failed", "err"),
    ("", "sep"),
    ("git merge --abort", "cmd"),
)
TRAMOS_MERGE = ((0, 4), (4, 6), (6, 8))
FILA_ABORTA = 7

STATUS = (
    ("git status", "cmd"),
    ("On branch main", "out"),
    ("You have unmerged paths.", "out"),
    ("", "sep"),
    ("Unmerged paths:", "out"),
    (f"  both modified:   {NOMBRE}", "err"),
)
SANGRIA_STATUS = {5: 2}
FILA_UNMERGED = 5

RESUELTO = (
    (f"git add {NOMBRE}", "cmd"),
    ("", "sep"),
    ("git commit", "cmd"),
    (f"[main 8f3a1c] Merge branch '{RAMA}'", "out"),
)
TRAMOS_RESUELTO = ((0, 2), (2, 4))


def _panel(lineas, x, nombre=None):
    chrome = ventana(ANCHO_PANEL, ALTO_PANEL, nombre, TAM - 2)
    chrome.move_to([x, Y_PANEL, 0])
    filas = VGroup(*[linea_terminal(c, t, TAM) for c, t in lineas])
    if len(filas):
        filas.arrange(DOWN, buff=BUFF, aligned_edge=LEFT)
        filas.move_to(chrome[0].get_top() + DOWN * (ALTO_BARRA + MARGEN), UP)
        filas.align_to(chrome[0].get_left() + RIGHT * MARGEN, LEFT)
    return VGroup(chrome, filas)


def _paso():
    return texto("mm", TAM).width - texto("m", TAM).width


def _sangrar(panel, sangrias):
    paso = _paso()
    for fila, espacios in sangrias.items():
        panel[1][fila].shift(RIGHT * espacios * paso)


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    archivo = _panel(CONFLICTO, X_ARCHIVO, NOMBRE)
    _sangrar(archivo, SANGRIA_CONFLICTO)
    prompt = _panel(PROMPT, X_TERMINAL)
    consola = _panel(MERGE, X_TERMINAL)
    marco_archivo, marco_consola = archivo[0], prompt[0]

    contenido, sangria = ANTES
    antes = linea_terminal(contenido, "txt", TAM)
    antes.move_to(archivo[1][FILA_ANTES], LEFT).shift(RIGHT * sangria * _paso())
    marcas = VGroup(*[archivo[1][i] for i in MARCAS])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(marco_archivo), FadeIn(marco_consola), run_time=0.6)
    teclear(scene, archivo, 0, FILA_ANTES, ritmo=0.26)
    scene.play(FadeIn(antes, shift=RIGHT * 0.12),
               FadeIn(prompt[1][0]), run_time=0.35)
    scene.next_slide()

    scene.play(FadeOut(prompt[1]), run_time=0.25)
    teclear(scene, consola, *TRAMOS_MERGE[0], ritmo=0.3)
    scene.next_slide()

    teclear(scene, consola, *TRAMOS_MERGE[1], ritmo=0.3)
    scene.next_slide()

    scene.play(FadeOut(antes, shift=LEFT * 0.15), run_time=0.3)
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.12) for f in marcas],
                    lag_ratio=0.3),
        run_time=1.2,
    )
    scene.next_slide()

    teclear(scene, consola, *TRAMOS_MERGE[2], ritmo=0.32)
    scene.play(Indicate(consola[1][FILA_ABORTA], color=ERROR,
                        scale_factor=1.08), run_time=0.8)
    scene.next_slide()

    status = _panel(STATUS, X_TERMINAL)
    _sangrar(status, SANGRIA_STATUS)
    scene.play(FadeOut(consola[1]), run_time=0.25)
    consola = status
    teclear(scene, consola, ritmo=0.3)
    scene.play(Indicate(consola[1][FILA_UNMERGED], color=ERROR,
                        scale_factor=1.06), run_time=0.8)
    scene.next_slide()

    filas = archivo[1]
    alturas = [f.get_y() for f in filas]
    scene.play(
        *[FadeOut(filas[i], shift=LEFT * 0.2) for i in FUERA],
        filas[QUEDA].animate
        .shift(UP * (alturas[SLOT_QUEDA] - alturas[QUEDA]))
        .set_color(CLARO),
        run_time=1.1,
    )
    scene.next_slide()

    resuelto = _panel(RESUELTO, X_TERMINAL)
    scene.play(FadeOut(consola[1]), run_time=0.25)
    consola = resuelto
    teclear(scene, consola, *TRAMOS_RESUELTO[0], ritmo=0.3)
    teclear(scene, consola, *TRAMOS_RESUELTO[1], ritmo=0.3)
    scene.wait(0.3)
    scene.next_slide()
