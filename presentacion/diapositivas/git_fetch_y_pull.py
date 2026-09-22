from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    VGroup,
)

from animaciones import teclear
from componentes import ALTO_BARRA, arista, imagen_circular, linea_terminal
from componentes import nodo_commit, puntero, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import FONDO, OK, RAMA_MAIN, SECUNDARIO, SUPERFICIE

TITULO = "git fetch"
TITULO_PULL = "git pull"

TAM = 16
ANCHO_PANEL = 6.4
ALTO_PANEL = 5.1
MARGEN = 0.4
BUFF = 0.2
X_PANEL, Y_PANEL = -3.5, -0.25

PROMPT = (("", "cmd"),)
SESION = (
    ("git fetch", "cmd"),
    ("  c4f0..b8e2  main -> origin/main", "out"),
    ("", "sep"),
    ("git merge origin/main", "cmd"),
    ("Fast-forward", "ok"),
)
SANGRIA_SESION = {1: 2}
TRAMOS = ((0, 2), (2, 5))
FILAS_ORDENES = (0, 3)
ORDEN_PULL = "git pull"

X_NODOS = (2.5, 3.4, 4.3, 5.2, 6.1)
RADIO = 0.28
TAM_HASH = 13
HASHES = ("0e5f", "77ab", "c4f0", "a3c1", "b8e2")
TUYOS = 3

Y_REMOTO = 1.55
Y_LOCAL = -1.55
Y_BAJADO = -0.55
X_ROTULO = 1.15
DIAMETRO_LOGO = 1.2
OCUPACION_LOGO = 0.7
ALTO_PORTATIL = 0.72
TAM_ROTULO = 16
TAM_PUNTERO = 13
BUFF_PUNTERO = 0.3
BUFF_ORIGIN = 0.26

X_DIV = (2.6, 3.6, 4.6, 5.9)
HASHES_DIV = ("0e5f", "c4f0")
HASH_TUYO = "f1a0"
HASH_SUYO = "b8e2"
HASH_UNION = "m7e1"
RADIO_UNION = 0.33
SESION_DIV = (
    ("git commit", "cmd"),
    ("", "sep"),
    ("git pull", "cmd"),
    ("Merge made by the 'ort' strategy.", "ok"),
)
TRAMOS_DIV = ((0, 2), (2, 4))


def _panel(lineas):
    chrome = ventana(ANCHO_PANEL, ALTO_PANEL, None, TAM - 2)
    chrome.move_to([X_PANEL, Y_PANEL, 0])
    filas = VGroup(*[linea_terminal(c, t, TAM) for c, t in lineas])
    filas.arrange(DOWN, buff=BUFF, aligned_edge=LEFT)
    filas.move_to(chrome[0].get_top() + DOWN * (ALTO_BARRA + MARGEN), UP)
    filas.align_to(chrome[0].get_left() + RIGHT * MARGEN, LEFT)
    return VGroup(chrome, filas)


def _sangrar(panel, sangrias):
    paso = texto("mm", TAM).width - texto("m", TAM).width
    for fila, espacios in sangrias.items():
        panel[1][fila].shift(RIGHT * espacios * paso)


def _portatil(alto, color):
    ancho = alto * 1.4
    carcasa = RoundedRectangle(
        width=ancho, height=alto, corner_radius=alto * 0.1,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    pantalla = RoundedRectangle(
        width=ancho * 0.82, height=alto * 0.72, corner_radius=alto * 0.05,
        stroke_color=color, stroke_width=2,
    ).set_stroke(opacity=0.55).set_fill(FONDO, opacity=1.0)
    pantalla.move_to(carcasa.get_center())
    peana = RoundedRectangle(
        width=ancho * 1.26, height=alto * 0.14, corner_radius=alto * 0.07,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    peana.next_to(carcasa, DOWN, buff=alto * 0.07)
    return VGroup(
        VGroup(carcasa, pantalla, peana),
        texto("local", TAM_ROTULO, color=color),
    ).arrange(DOWN, buff=0.16)


def _nodos(xs, y, hashes, color):
    return VGroup(*[
        nodo_commit(h, color, RADIO, TAM_HASH).move_to([x, y, 0])
        for x, h in zip(xs, hashes)
    ])


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    logo = imagen_circular("github.jpg", diametro=DIAMETRO_LOGO,
                           ocupacion=OCUPACION_LOGO)
    logo.move_to([X_ROTULO, Y_REMOTO, 0])
    maquina = _portatil(ALTO_PORTATIL, SECUNDARIO)
    maquina.move_to([X_ROTULO, Y_LOCAL, 0])

    arriba = _nodos(X_NODOS, Y_REMOTO, HASHES, OK)
    enlaces_arriba = VGroup(*[
        arista(arriba[i], arriba[i + 1], OK, RADIO)
        for i in range(len(arriba) - 1)
    ])

    mios = _nodos(X_NODOS[:TUYOS], Y_LOCAL, HASHES[:TUYOS], RAMA_MAIN)
    enlaces_mios = VGroup(*[
        arista(mios[i], mios[i + 1], RAMA_MAIN, RADIO)
        for i in range(TUYOS - 1)
    ])
    p_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    p_main.next_to(mios[-1], DOWN, buff=BUFF_PUNTERO)
    p_origin = puntero("origin/main", OK, TAM_PUNTERO)
    p_origin.next_to(mios[-1], UP, buff=BUFF_ORIGIN)

    prompt = _panel(PROMPT)
    consola = _panel(SESION)
    _sangrar(consola, SANGRIA_SESION)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(logo), FadeIn(maquina), FadeIn(prompt[0]), run_time=0.6)
    scene.play(
        *[GrowFromCenter(n) for n in arriba],
        *[Create(e) for e in enlaces_arriba], run_time=1.0,
    )
    scene.play(
        *[GrowFromCenter(n) for n in mios],
        *[Create(e) for e in enlaces_mios], run_time=0.9,
    )
    scene.play(FadeIn(p_main, shift=UP * 0.1),
               FadeIn(p_origin, shift=DOWN * 0.1), run_time=0.5)
    scene.play(FadeIn(prompt[1][0]), run_time=0.3)
    scene.next_slide()

    bajados = _nodos(X_NODOS[TUYOS:], Y_BAJADO, HASHES[TUYOS:], OK)
    ramal = VGroup(
        arista(mios[-1], bajados[0], OK, RADIO),
        arista(bajados[0], bajados[1], OK, RADIO),
    )

    scene.play(FadeOut(prompt[1]), run_time=0.25)
    teclear(scene, consola, *TRAMOS[0], ritmo=0.32)
    scene.play(
        *[ReplacementTransform(arriba[TUYOS + i].copy(), bajados[i])
          for i in range(len(bajados))],
        run_time=1.1,
    )
    scene.play(
        *[Create(r) for r in ramal],
        p_origin.animate.next_to(bajados[-1], UP, buff=BUFF_ORIGIN),
        run_time=0.8,
    )
    scene.play(Indicate(p_main, color=RAMA_MAIN, scale_factor=1.15),
               run_time=0.8)
    scene.next_slide()

    planos = _nodos(X_NODOS[TUYOS:], Y_LOCAL, HASHES[TUYOS:], OK)
    rectas = VGroup(
        arista(mios[-1], planos[0], OK, RADIO),
        arista(planos[0], planos[1], OK, RADIO),
    )

    teclear(scene, consola, *TRAMOS[1], ritmo=0.32)
    scene.play(
        *[Transform(b, p) for b, p in zip(bajados, planos)],
        *[Transform(r, c) for r, c in zip(ramal, rectas)],
        p_origin.animate.next_to(planos[-1], UP, buff=BUFF_ORIGIN),
        run_time=1.1,
    )
    scene.play(p_main.animate.next_to(planos[-1], DOWN, buff=BUFF_PUNTERO),
               run_time=0.9)
    scene.next_slide()

    otro_encabezado = hacer_titulo(TITULO_PULL)
    ordenes = VGroup(*[consola[1][i] for i in FILAS_ORDENES])
    pull = linea_terminal(ORDEN_PULL, "cmd", TAM).move_to(
        consola[1][FILAS_ORDENES[0]], LEFT)
    salidas = VGroup(consola[1][1], consola[1][4])

    scene.play(FadeOut(salidas), run_time=0.4)
    scene.play(
        ReplacementTransform(ordenes, pull),
        FadeOut(encabezado), FadeIn(otro_encabezado, shift=DOWN * 0.2),
        run_time=1.1,
    )
    scene.next_slide()

    comunes = _nodos(X_DIV[:2], Y_LOCAL, HASHES_DIV, RAMA_MAIN)
    tuyo = nodo_commit(HASH_TUYO, RAMA_MAIN, RADIO, TAM_HASH)
    tuyo.move_to([X_DIV[2], Y_LOCAL, 0])
    linea_tuya = VGroup(arista(comunes[0], comunes[1], RAMA_MAIN, RADIO),
                        arista(comunes[1], tuyo, RAMA_MAIN, RADIO))
    suyos = _nodos(X_DIV[:3], Y_REMOTO, (*HASHES_DIV, HASH_SUYO), OK)
    enlaces_suyos = VGroup(*[
        arista(suyos[i], suyos[i + 1], OK, RADIO)
        for i in range(len(suyos) - 1)
    ])
    q_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    q_main.next_to(tuyo, DOWN, buff=BUFF_PUNTERO)

    scene.play(
        FadeOut(arriba), FadeOut(enlaces_arriba), FadeOut(mios),
        FadeOut(enlaces_mios), FadeOut(bajados), FadeOut(ramal),
        FadeOut(p_main), FadeOut(p_origin), FadeOut(pull), run_time=0.7,
    )
    consola = _panel(SESION_DIV)
    scene.play(
        *[GrowFromCenter(n) for n in suyos],
        *[Create(e) for e in enlaces_suyos], run_time=0.9,
    )
    scene.play(*[GrowFromCenter(n) for n in comunes],
               Create(linea_tuya[0]), run_time=0.7)
    teclear(scene, consola, *TRAMOS_DIV[0], ritmo=0.32)
    scene.play(GrowFromCenter(tuyo), Create(linea_tuya[1]),
               FadeIn(q_main, shift=UP * 0.1), run_time=0.8)
    scene.next_slide()

    bajado = nodo_commit(HASH_SUYO, OK, RADIO, TAM_HASH)
    bajado.move_to([X_DIV[2], Y_BAJADO, 0])
    q_origin = puntero("origin/main", OK, TAM_PUNTERO)
    q_origin.next_to(bajado, UP, buff=BUFF_ORIGIN)
    ramal_div = arista(comunes[1], bajado, OK, RADIO)
    union = nodo_commit(HASH_UNION, RAMA_MAIN, RADIO_UNION, TAM_HASH)
    union.move_to([X_DIV[3], Y_LOCAL, 0])
    padres = VGroup(arista(tuyo, union, RAMA_MAIN, RADIO),
                    arista(bajado, union, OK, RADIO))

    teclear(scene, consola, *TRAMOS_DIV[1], ritmo=0.32)
    scene.play(ReplacementTransform(suyos[2].copy(), bajado), run_time=1.0)
    scene.play(Create(ramal_div), FadeIn(q_origin, shift=DOWN * 0.1),
               run_time=0.6)
    scene.play(Create(padres[0]), Create(padres[1]), run_time=0.7)
    scene.play(
        GrowFromCenter(union),
        q_main.animate.next_to(union, DOWN, buff=BUFF_PUNTERO),
        run_time=0.8,
    )
    scene.play(Indicate(union, color=RAMA_MAIN, scale_factor=1.15),
               run_time=0.9)
    scene.wait(0.3)
    scene.next_slide()
