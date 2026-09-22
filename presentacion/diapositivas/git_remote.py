from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    Transform,
    VGroup,
)

from animaciones import flecha, teclear
from componentes import ALTO_BARRA, imagen_circular, linea_terminal
from componentes import puntero, terminal, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import OK, SECUNDARIO

TITULO = "git remote"

USUARIO = "aperture"
REPO = "aperture_repo"
URL = f"https://github.com/{USUARIO}/{REPO}.git"

SESION = (
    (f"git remote add origin {URL}", "cmd"),
    ("", "sep"),
    ("git remote -v", "cmd"),
    (f"origin  {URL} (fetch)", "out"),
    (f"origin  {URL} (push)", "out"),
)
TAM_SESION = 15
Y_SESION = 0.35

APODO = "origin"
TAM_APODO = 21
TAM_DIRECCION = 17
SEPARACION_APODO = 1.15
Y_APODO = -2.45

NAVEGADOR = f"github.com/{USUARIO}/{REPO}"
TAM_WEB = 16
ANCHO_WEB = 11.0
ALTO_WEB = 4.6
MARGEN_WEB = 0.42
BUFF_WEB = 0.2
X_WEB, Y_WEB = 0.9, 0.1
DIAMETRO_LOGO = 1.5
OCUPACION_LOGO = 0.7
X_LOGO = -5.8

NUEVO = (
    ("…or create a new repository on the command line", "out"),
    (f'echo "# {REPO}" >> README.md', "txt"),
    ("git init", "txt"),
    ("git add README.md", "txt"),
    ('git commit -m "first commit"', "txt"),
    ("git branch -M main", "txt"),
    (f"git remote add origin {URL}", "txt"),
    ("git push -u origin main", "txt"),
)
EXISTENTE = "…or push an existing repository from the command line"
SOBRAN = (1, 2, 3, 4)
QUEDAN = (5, 6, 7)

TITULO_CLONE = "git clone"
CLONAR = (
    (f"git clone {URL}", "cmd"),
    (f"Cloning into '{REPO}'...", "out"),
    ("", "sep"),
    (f"cd {REPO}", "cmd"),
    ("git remote -v", "cmd"),
    (f"origin  {URL} (fetch)", "out"),
    (f"origin  {URL} (push)", "out"),
)
TRAMOS_CLONE = ((0, 3), (3, 7))


def _pagina(lineas, nombre=None):
    chrome = ventana(ANCHO_WEB, ALTO_WEB, nombre, TAM_WEB - 2)
    chrome.move_to([X_WEB, Y_WEB, 0])
    filas = VGroup(*[linea_terminal(c, t, TAM_WEB) for c, t in lineas])
    filas.arrange(DOWN, buff=BUFF_WEB, aligned_edge=LEFT)
    filas.move_to(chrome[0].get_top() + DOWN * (ALTO_BARRA + MARGEN_WEB), UP)
    filas.align_to(chrome[0].get_left() + RIGHT * MARGEN_WEB, LEFT)
    return VGroup(chrome, filas)


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    consola = terminal(SESION, tam=TAM_SESION).move_to([0, Y_SESION, 0])

    etiqueta = puntero(APODO, OK, TAM_APODO)
    direccion = texto(URL, TAM_DIRECCION, color=SECUNDARIO)
    direccion.next_to(etiqueta, RIGHT, buff=SEPARACION_APODO)
    puente = flecha(
        etiqueta.get_right() + RIGHT * 0.1,
        direccion.get_left() + LEFT * 0.1,
        OK, buff=0.04,
    )
    apodo = VGroup(etiqueta, puente, direccion).move_to([0, Y_APODO, 0])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(consola[0]), run_time=0.5)
    teclear(scene, consola, ritmo=0.32)
    scene.play(FadeIn(etiqueta, shift=RIGHT * 0.12), run_time=0.5)
    scene.play(FadeIn(puente), FadeIn(direccion, shift=RIGHT * 0.12),
               run_time=0.6)
    scene.next_slide()

    pagina = _pagina(NUEVO, NAVEGADOR)
    logo = imagen_circular("github.jpg", diametro=DIAMETRO_LOGO,
                           ocupacion=OCUPACION_LOGO)
    logo.move_to([X_LOGO, Y_WEB, 0])
    scene.play(
        FadeOut(consola), FadeOut(apodo), run_time=0.6,
    )
    scene.play(FadeIn(logo, shift=RIGHT * 0.15), FadeIn(pagina[0]),
               run_time=0.6)
    teclear(scene, pagina, ritmo=0.26)
    scene.next_slide()

    filas = pagina[1]
    alturas = [f.get_y() for f in filas]
    otro = linea_terminal(EXISTENTE, "out", TAM_WEB).move_to(filas[0], LEFT)
    scene.play(
        Transform(filas[0], otro),
        *[FadeOut(filas[i], shift=LEFT * 0.2) for i in SOBRAN],
        *[filas[q].animate.shift(UP * (alturas[d] - alturas[q]))
          for d, q in enumerate(QUEDAN, start=1)],
        run_time=1.2,
    )
    scene.next_slide()

    otro_encabezado = hacer_titulo(TITULO_CLONE)
    clonar = _pagina(CLONAR)
    vivas = VGroup(filas[0], *[filas[q] for q in QUEDAN])

    scene.play(
        FadeOut(pagina[0]), FadeOut(vivas),
        FadeOut(encabezado), FadeIn(otro_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(clonar[0]), run_time=0.5)
    teclear(scene, clonar, *TRAMOS_CLONE[0], ritmo=0.3)
    scene.next_slide()

    teclear(scene, clonar, *TRAMOS_CLONE[1], ritmo=0.3)
    scene.wait(0.3)
    scene.next_slide()
