from manim import (
    DOWN,
    LEFT,
    UP,
    Create,
    FadeIn,
    Flash,
    GrowFromCenter,
    Group,
    VGroup,
)

from componentes import (
    enlace,
    enmarcar,
    imagen_recortada,
    nodo_commit,
    puntero,
    texto,
)
from componentes import titulo as hacer_titulo
from estilo import CLARO, RAMA_FEATURE, RAMA_MAIN

TITULO = "Un ejemplo: Minecraft"

VERSIONES = (
    ("mc/mc_1.12", "1.12", -4.6),
    ("mc/mc_1.13", "1.13", -2.9),
    ("mc/mc_1.14", "1.14", -1.2),
    ("mc/mc_1.15", "1.15", 0.5),
    ("mc/mc_1.16", "1.16", 5.2),
)
ANCHO_ARTE = 1.5
MEDIA_TARJETA = ANCHO_ARTE / 2 + 0.07
Y_JAVA = 0.3

X_SNAPSHOT = (2.4, 3.3)
Y_SNAPSHOT = 1.2
R_NODO = 0.26

CENTRADO = DOWN * 1.26 + LEFT * 0.3


def _tarjeta(archivo, version, x):
    arte = imagen_recortada(archivo, ANCHO_ARTE).move_to([x, Y_JAVA, 0])
    marco = enmarcar(arte, margen=0.14, color=RAMA_MAIN).set_stroke(width=2.5)
    etiqueta = texto(version, 16, color=CLARO).next_to(marco, UP, buff=0.18)
    return Group(arte, marco, etiqueta)


def _fila_java():
    tarjetas = [_tarjeta(*v) for v in VERSIONES]
    tramos = VGroup(*[
        enlace([VERSIONES[i][2] + MEDIA_TARJETA, Y_JAVA, 0],
               [VERSIONES[i + 1][2] - MEDIA_TARJETA, Y_JAVA, 0], RAMA_MAIN)
        for i in range(len(VERSIONES) - 1)
    ])
    return tarjetas, tramos


def _rama_snapshots():
    nodos = VGroup(*[
        nodo_commit("", RAMA_FEATURE, R_NODO).move_to([x, Y_SNAPSHOT, 0])
        for x in X_SNAPSHOT
    ])
    x_sale, x_entra = VERSIONES[3][2], VERSIONES[4][2]
    tramos = VGroup(
        enlace([x_sale + MEDIA_TARJETA, Y_JAVA, 0],
               [X_SNAPSHOT[0] - R_NODO, Y_SNAPSHOT, 0], RAMA_FEATURE),
        enlace([X_SNAPSHOT[0] + R_NODO, Y_SNAPSHOT, 0],
               [X_SNAPSHOT[1] - R_NODO, Y_SNAPSHOT, 0], RAMA_FEATURE),
        enlace([X_SNAPSHOT[1] + R_NODO, Y_SNAPSHOT, 0],
               [x_entra - MEDIA_TARJETA, Y_JAVA, 0], RAMA_FEATURE),
    )
    rotulo = puntero("snapshots", RAMA_FEATURE, 14)
    rotulo.next_to(nodos, UP, buff=0.28)
    return nodos, tramos, rotulo


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    tarjetas, tramos = _fila_java()
    snapshots, tramos_snap, rotulo_snap = _rama_snapshots()
    Group(*tarjetas, tramos, snapshots, tramos_snap, rotulo_snap).shift(CENTRADO)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(tarjetas[0], scale=0.92), run_time=0.6)
    for tramo, tarjeta in zip(tramos, tarjetas[1:]):
        scene.play(Create(tramo), FadeIn(tarjeta, scale=0.92), run_time=0.55)
    scene.next_slide()

    scene.play(Create(tramos_snap[0]), run_time=0.45)
    scene.play(GrowFromCenter(snapshots[0]), run_time=0.3)
    scene.play(Create(tramos_snap[1]), GrowFromCenter(snapshots[1]),
               run_time=0.45)
    scene.play(FadeIn(rotulo_snap, shift=DOWN * 0.12), run_time=0.35)
    scene.play(Create(tramos_snap[2]), run_time=0.5)
    scene.play(
        Flash(tarjetas[4], color=RAMA_FEATURE, line_length=0.25, num_lines=16,
              flash_radius=MEDIA_TARJETA + 0.5),
        run_time=0.7,
    )
    scene.next_slide()

    scene.next_slide()
