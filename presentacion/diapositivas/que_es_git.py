from manim import (
    DOWN,
    RIGHT,
    UP,
    Create,
    DashedLine,
    FadeIn,
    Flash,
    GrowFromCenter,
    LaggedStart,
    VGroup,
)

from animaciones import pulso
from componentes import arista, avatar, nodo_commit, puntero, texto
from componentes import titulo as hacer_titulo
from estilo import (
    CLARO,
    FONT_TITULO,
    RAMA_FEATURE,
    RAMA_MAIN,
    SECUNDARIO,
)

TITULO = "La solución"

X_MAIN = (-5.4, -3.6, -1.8, 0.0, 1.8)
X_MERGE = 3.6
Y_MAIN = 0.35
VERSIONES = ("v1", "v2", "v3", "v4", "v5")
VERSION_MERGE = "v6"

X_RAMA = (-1.8, 0.0)
Y_RAMA = 1.75
R = 0.32

X_TIEMPO = (2.4, 3.7)
APARTA_TIEMPO = RIGHT * 1.9

EQUIPO = (("A", "ana", 0), ("L", "luis", 2), ("M", "mar", 4))
Y_EQUIPO = -1.75
RADIO_AVATAR = 0.42

PALABRAS = (
    ("VERSIONES", RAMA_MAIN),
    ("RAMAS", RAMA_FEATURE),
    ("EN EQUIPO", CLARO),
)
Y_PALABRAS = -3.2
TAM_PALABRA = 17


def _historia():
    nodos = VGroup(*[
        nodo_commit(v, RAMA_MAIN, R).move_to([x, Y_MAIN, 0])
        for x, v in zip(X_MAIN, VERSIONES)
    ])
    tramos = VGroup(*[
        arista(a, b, RAMA_MAIN, R) for a, b in zip(nodos, nodos[1:])
    ])
    return nodos, tramos


def _rama(desde, hasta):
    nodos = VGroup(*[
        nodo_commit("", RAMA_FEATURE, R).move_to([x, Y_RAMA, 0]) for x in X_RAMA
    ])
    tramos = VGroup(
        arista(desde, nodos[0], RAMA_FEATURE, R),
        arista(nodos[0], nodos[1], RAMA_FEATURE, R),
        arista(nodos[1], hasta, RAMA_FEATURE, R),
    )
    return nodos, tramos


def _fichas(nodos):
    fichas, cuerdas = VGroup(), VGroup()
    for inicial, nombre, indice in EQUIPO:
        x = nodos[indice].get_center()[0]
        ficha = avatar(inicial, nombre, RADIO_AVATAR).move_to([x, Y_EQUIPO, 0])
        fichas.add(ficha)
        cuerdas.add(DashedLine(
            [x, Y_MAIN - R, 0], [x, ficha.get_top()[1], 0],
            color=SECUNDARIO, stroke_width=2, dash_length=0.09,
        ).set_stroke(opacity=0.55))
    return fichas, cuerdas


def _palabras():
    fila = VGroup()
    for i, (palabra, color) in enumerate(PALABRAS):
        if i:
            fila.add(texto("·", TAM_PALABRA, color=SECUNDARIO))
        fila.add(texto(palabra, TAM_PALABRA, color=color, font=FONT_TITULO))
    return fila.arrange(RIGHT, buff=0.5).move_to([0, Y_PALABRAS, 0])


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    nodos, tramos = _historia()
    merge = nodo_commit(VERSION_MERGE, RAMA_MAIN, R).move_to([X_MERGE, Y_MAIN, 0])
    rama, tramos_rama = _rama(nodos[1], merge)
    cierre_main = arista(nodos[-1], merge, RAMA_MAIN, R)
    fichas, cuerdas = _fichas(nodos)
    palabras = _palabras()

    p_main = puntero("main", RAMA_MAIN, 15).next_to(merge, DOWN, buff=0.3)
    p_rama = puntero("feature", RAMA_FEATURE, 15).next_to(rama[1], UP, buff=0.3)

    tiempo = DashedLine([X_TIEMPO[0], Y_MAIN, 0], [X_TIEMPO[1], Y_MAIN, 0],
                        color=SECUNDARIO, stroke_width=2, dash_length=0.12)
    tiempo.set_stroke(opacity=0.5)
    rotulo_tiempo = texto("tiempo", 14, color=SECUNDARIO)
    rotulo_tiempo.next_to(tiempo, RIGHT, buff=0.22)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(GrowFromCenter(nodos[0]), run_time=0.45)
    for tramo, nodo in zip(tramos, nodos[1:]):
        scene.play(Create(tramo), GrowFromCenter(nodo), run_time=0.45)
    scene.play(Create(tiempo), FadeIn(rotulo_tiempo), run_time=0.5)
    scene.play(FadeIn(palabras[0], shift=UP * 0.12), run_time=0.5)
    scene.next_slide()

    scene.play(Create(tramos_rama[0]), run_time=0.5)
    scene.play(GrowFromCenter(rama[0]), run_time=0.35)
    scene.play(Create(tramos_rama[1]), GrowFromCenter(rama[1]), run_time=0.45)
    scene.play(FadeIn(p_rama, shift=DOWN * 0.12), run_time=0.35)

    scene.play(VGroup(tiempo, rotulo_tiempo).animate.shift(APARTA_TIEMPO),
               run_time=0.45)
    scene.play(Create(cierre_main), Create(tramos_rama[2]), run_time=0.7)
    scene.play(
        GrowFromCenter(merge),
        Flash(merge, color=RAMA_MAIN, line_length=0.22, num_lines=14,
              flash_radius=R + 0.35),
        run_time=0.6,
    )
    scene.play(FadeIn(p_main, shift=UP * 0.12), run_time=0.35)
    scene.play(FadeIn(palabras[1]), FadeIn(palabras[2], shift=UP * 0.12),
               run_time=0.5)
    scene.next_slide()

    scene.play(
        LaggedStart(*[
            LaggedStart(Create(cuerda), GrowFromCenter(ficha), lag_ratio=0.4)
            for cuerda, ficha in zip(cuerdas, fichas)
        ], lag_ratio=0.35),
        run_time=1.6,
    )
    scene.play(FadeIn(palabras[3]), FadeIn(palabras[4], shift=UP * 0.12),
               run_time=0.5)

    scene.play(
        *[pulso(t, CLARO, 0.7) for t in tramos],
        *[pulso(t, CLARO, 0.9) for t in tramos_rama],
        pulso(cierre_main, CLARO, 0.7),
        run_time=1.2,
    )
    scene.wait(0.3)

    scene.next_slide()
