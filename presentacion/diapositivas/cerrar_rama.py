from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Flash,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    VGroup,
)

from animaciones import teclear
from componentes import ALTO_BARRA, arista, linea_terminal, nodo_commit
from componentes import puntero, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import AMBAR, ERROR, OK, RAMA_FEATURE, RAMA_MAIN, SECUNDARIO

TITULO = "git branch -d"

Y_BASE = 0.7
Y_ALTA = 1.85
RADIO = 0.33
RADIO_MERGE = 0.38
TAM_HASH = 14
TAM_PUNTERO = 15
BUFF_PUNTERO = 0.28
APAGADO = 0.25

X_BASE = (-4.9, -3.3, -1.6)
X_MERGE = 1.1
HASHES_BASE = ("0e5f", "77ab", "c4f0")
HASH_MERGE = "m9d3"

X_ALTA = (-1.6, 0.0)
HASHES_ALTA = ("a3c1", "b8e2")
RAMA = "experimento"
X_SUELTA = -4.1
HASH_SUELTA = "55dd"
RAMA_SUELTA = "borrador"

Y_CORTE = -0.55
X_ROTULO = -6.35
Y_ROTULO = 1.28
TAM_ROTULO = 15

ANCHO_CONSOLA = 8.0
ALTO_CONSOLA = 2.3
Y_CONSOLA = -2.1
MARGEN_CONSOLA = 0.5
TAM_SESION = 15
BUFF_SESION = 0.16
Y_SESION = Y_CONSOLA + ALTO_CONSOLA / 2 - ALTO_BARRA - 0.25

SESIONES = (
    (("git branch --merged", "cmd"),
     ("* main", "ok"),
     (f"  {RAMA}", "out")),
    ((f"git branch -d {RAMA}", "cmd"),
     (f"Deleted branch {RAMA} (was b8e2f4).", "out")),
    ((f"git branch -d {RAMA_SUELTA}", "cmd"),
     (f"error: the branch '{RAMA_SUELTA}' is not fully merged", "err"),
     (f"git branch -D {RAMA_SUELTA}", "cmd")),
)


def _marco_consola():
    return ventana(ANCHO_CONSOLA, ALTO_CONSOLA, "terminal", 14).move_to(
        [0, Y_CONSOLA, 0])


def _sesion(indice):
    filas = VGroup(*[
        linea_terminal(c, t, TAM_SESION) for c, t in SESIONES[indice]
    ]).arrange(DOWN, buff=BUFF_SESION, aligned_edge=LEFT)
    unidad = linea_terminal("M", "out", TAM_SESION).width
    for fila, (contenido, _tipo) in zip(filas, SESIONES[indice]):
        sangria = len(contenido) - len(contenido.lstrip(" "))
        if sangria:
            fila.shift(RIGHT * unidad * sangria)
    filas.align_to([0, Y_SESION, 0], UP)
    return filas.align_to([-ANCHO_CONSOLA / 2 + MARGEN_CONSOLA, 0, 0], LEFT)


def construir(scene):
    encabezado = hacer_titulo(TITULO)

    corte = Line([-6.6, Y_CORTE, 0], [6.6, Y_CORTE, 0],
                 color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.3)
    rotulo_ramas = texto("las ramas", TAM_ROTULO, color=SECUNDARIO)
    rotulo_ramas.move_to([X_ROTULO, Y_ROTULO, 0], LEFT)
    rotulo_consola = texto("la terminal", TAM_ROTULO, color=SECUNDARIO)
    rotulo_consola.move_to([X_ROTULO, Y_CONSOLA, 0], LEFT)
    marco_consola = _marco_consola()

    base = VGroup(*[
        nodo_commit(h, RAMA_MAIN, RADIO, TAM_HASH).move_to([x, Y_BASE, 0])
        for x, h in zip(X_BASE, HASHES_BASE)
    ])
    m = nodo_commit(HASH_MERGE, RAMA_MAIN, RADIO_MERGE, TAM_HASH)
    m.move_to([X_MERGE, Y_BASE, 0])
    alta = VGroup(*[
        nodo_commit(h, RAMA_FEATURE, RADIO, TAM_HASH).move_to([x, Y_ALTA, 0])
        for x, h in zip(X_ALTA, HASHES_ALTA)
    ])
    suelta = nodo_commit(HASH_SUELTA, AMBAR, RADIO, TAM_HASH)
    suelta.move_to([X_SUELTA, Y_ALTA, 0])

    hilos = VGroup(
        arista(base[0], base[1], RAMA_MAIN, RADIO),
        arista(base[1], base[2], RAMA_MAIN, RADIO),
        arista(base[1], alta[0], RAMA_FEATURE, RADIO),
        arista(alta[0], alta[1], RAMA_FEATURE, RADIO),
        arista(base[2], m, RAMA_MAIN, RADIO),
        arista(alta[1], m, RAMA_FEATURE, RADIO),
    )
    hilo_suelto = arista(base[0], suelta, AMBAR, RADIO)

    p_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    p_main.next_to(m, DOWN, buff=BUFF_PUNTERO)
    p_head = puntero("HEAD", OK, TAM_PUNTERO)
    p_head.next_to(p_main, RIGHT, buff=BUFF_PUNTERO)
    p_rama = puntero(RAMA, RAMA_FEATURE, TAM_PUNTERO)
    p_rama.next_to(alta[-1], UP, buff=BUFF_PUNTERO)
    p_suelta = puntero(RAMA_SUELTA, AMBAR, TAM_PUNTERO)
    p_suelta.next_to(suelta, UP, buff=BUFF_PUNTERO)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in [*base, m, *alta, suelta]],
                    lag_ratio=0.15),
        FadeIn(rotulo_ramas, shift=RIGHT * 0.15), run_time=1.2,
    )
    scene.play(
        LaggedStart(*[Create(h) for h in [*hilos, hilo_suelto]],
                    lag_ratio=0.15),
        run_time=1.0,
    )
    scene.play(FadeIn(p_main, shift=UP * 0.1), FadeIn(p_head, shift=LEFT * 0.1),
               FadeIn(p_rama, shift=DOWN * 0.1),
               FadeIn(p_suelta, shift=DOWN * 0.1), run_time=0.6)
    scene.play(Create(corte), FadeIn(rotulo_consola, shift=RIGHT * 0.15),
               run_time=0.6)
    scene.play(FadeIn(marco_consola), run_time=0.5)
    scene.next_slide()

    sesion = _sesion(0)
    teclear(scene, VGroup(marco_consola, sesion), hasta=2, ritmo=0.32)
    scene.play(Indicate(p_main, color=RAMA_MAIN, scale_factor=1.12),
               run_time=0.5)
    teclear(scene, VGroup(marco_consola, sesion), desde=2, ritmo=0.32)
    scene.play(Indicate(p_rama, color=RAMA_FEATURE, scale_factor=1.15),
               run_time=0.6)
    scene.next_slide()

    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(1)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    scene.play(FadeOut(p_rama, shift=UP * 0.4), run_time=0.8)
    scene.play(
        LaggedStart(*[
            Flash(n, color=OK, line_length=0.18, num_lines=12,
                  flash_radius=RADIO + 0.3) for n in alta
        ], lag_ratio=0.3),
        run_time=0.9,
    )
    teclear(scene, VGroup(marco_consola, sesion), desde=1, ritmo=0.32)
    scene.next_slide()

    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(2)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    teclear(scene, VGroup(marco_consola, sesion), desde=1, hasta=2, ritmo=0.4)
    scene.play(Indicate(p_suelta, color=ERROR, scale_factor=1.15),
               run_time=0.7)
    teclear(scene, VGroup(marco_consola, sesion), desde=2, ritmo=0.32)
    scene.play(FadeOut(p_suelta, shift=UP * 0.4), run_time=0.8)
    scene.play(
        suelta.animate.set_opacity(APAGADO),
        hilo_suelto.animate.set_stroke(opacity=APAGADO),
        run_time=0.8,
    )
    scene.wait(0.3)

    scene.next_slide()
