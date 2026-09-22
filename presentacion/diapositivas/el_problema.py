import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LaggedStart,
    VGroup,
)

from animaciones import teclear
from componentes import (
    avatar,
    burbuja,
    globo_mudo,
    telefono,
    terminal,
    texto,
)
from componentes import titulo as hacer_titulo
from estilo import AMBAR, ERROR, SECUNDARIO

TITULO = "Motivación"
Y_ACTO = -0.35

AULA = "aula virtual"
TAREA = (
    ("Proyecto final", "txt"),
    ("", "sep"),
    ("En equipos de 3 personas.", "out"),
    ("Un entregable por equipo.", "out"),
    ("", "sep"),
    ("Entrega: 15 de junio", "avi"),
)
EQUIPO = (("A", "ana"), ("L", "luis"), ("M", "mar"))
X_TAREA = -2.85
X_EQUIPO = 3.5
RADIO_AVATAR = 0.52

CHAT = (
    ("ana", "proyecto.zip", SECUNDARIO, True),
    ("luis", "proyecto_v2.zip", SECUNDARIO, True),
    ("mar", "proyecto_MIO.zip", AMBAR, True),
    ("ana", "¿cuál es el bueno?", ERROR, False),
)
LADO = (LEFT, RIGHT, LEFT, RIGHT)
CHAT_NOMBRE = "proyecto final"
CHAT_SUB = "ana, luis, mar"

HILO = (
    (0.60, 0.30, SECUNDARIO, LEFT),
    (0.52, 0.50, SECUNDARIO, RIGHT),
    (0.44, 0.30, SECUNDARIO, LEFT),
    (0.62, 0.50, SECUNDARIO, RIGHT),
    (0.50, 0.30, SECUNDARIO, LEFT),
    (0.58, 0.50, AMBAR, LEFT),
    (0.54, 0.32, ERROR, RIGHT),
)

ANCHO_MOVIL = 3.5
ALTO_MOVIL = 5.5
X_MOVIL = -3.35
TAM_BURBUJA = 22
MARGEN_BURBUJA = 0.12
X_COLUMNA = (-0.7, 5.1)


def _equipo():
    fichas = VGroup(*[
        avatar(inicial, nombre, RADIO_AVATAR) for inicial, nombre in EQUIPO
    ]).arrange(RIGHT, buff=0.5).move_to([X_EQUIPO, Y_ACTO, 0])
    rotulo = texto("el equipo", 15, color=SECUNDARIO)
    return rotulo.next_to(fichas, UP, buff=0.55), fichas


def _hilo_en(lienzo):
    util = lienzo.width - 2 * MARGEN_BURBUJA
    globos = VGroup(*[
        globo_mudo(util * ancho, alto, color) for ancho, alto, color, _ in HILO
    ]).arrange(DOWN, buff=0.16)
    if globos.height > lienzo.height:
        globos.scale(lienzo.height / globos.height)

    globos.move_to(lienzo).align_to(lienzo, DOWN)
    for globo, (_, _, _, lado) in zip(globos, HILO):
        globo.align_to(lienzo, lado).shift(-lado * MARGEN_BURBUJA)
    return globos


def _conversacion():
    izquierdo, derecho = X_COLUMNA
    globos = VGroup(*[
        burbuja(autor, mensaje, color, tam=TAM_BURBUJA, adjunto=adjunto,
                cola=lado)
        for (autor, mensaje, color, adjunto), lado in zip(CHAT, LADO)
    ]).arrange(DOWN, buff=0.32)
    globos.move_to([(izquierdo + derecho) / 2, Y_ACTO, 0])
    for globo, lado in zip(globos, LADO):
        x = derecho if lado[0] > 0 else izquierdo
        globo.align_to(np.array([x, 0, 0]), lado)
    return globos


def _chat():
    movil = telefono(ANCHO_MOVIL, ALTO_MOVIL, rotulo=CHAT_NOMBRE, sub=CHAT_SUB)
    movil.move_to([X_MOVIL, Y_ACTO, 0])
    return movil, _hilo_en(movil[1]), _conversacion()


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)

    tarea = terminal(TAREA, tam=20, nombre=AULA)
    tarea.move_to([X_TAREA, Y_ACTO, 0])
    rotulo_equipo, avatares = _equipo()

    scene.play(FadeIn(tarea[0]), run_time=0.6)
    teclear(scene, tarea, ritmo=0.42)
    scene.play(FadeIn(rotulo_equipo), run_time=0.35)
    scene.play(
        LaggedStart(*[GrowFromCenter(f) for f in avatares], lag_ratio=0.25),
        run_time=0.9,
    )
    scene.next_slide()

    movil, hilo, al_lado = _chat()

    scene.play(FadeOut(tarea), FadeOut(rotulo_equipo), FadeOut(avatares),
               run_time=0.7)
    scene.play(FadeIn(movil, shift=UP * 0.15), run_time=0.7)
    scene.play(
        LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in hilo], lag_ratio=0.18),
        run_time=1.0,
    )
    for globo in al_lado:
        scene.play(FadeIn(globo, shift=RIGHT * 0.18, scale=0.95), run_time=0.45)
    scene.wait(0.3)

    scene.next_slide()
