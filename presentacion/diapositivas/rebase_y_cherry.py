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
    ReplacementTransform,
    VGroup,
)

from animaciones import teclear
from componentes import ALTO_BARRA, arista, linea_terminal, nodo_commit
from componentes import puntero, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import AMBAR, OK, RAMA_FEATURE, RAMA_MAIN, SECUNDARIO

TITULO = "git rebase y git cherry-pick"

Y_BASE = 0.7
Y_ALTA = 1.85
RADIO = 0.33
TAM_HASH = 14
TAM_PUNTERO = 15
BUFF_PUNTERO = 0.28

X_BASE = (-5.0, -3.3, -1.6)
X_ALTA = (-1.6, 0.1)
X_REBASE = (0.1, 1.8)
HASHES_BASE = ("0e5f", "77ab", "c4f0")
HASHES_ALTA = ("a3c1", "b8e2")
HASHES_NUEVOS = ("f19d", "6b70")
RAMA = "experimento"

X_OTRA = (-2.4, -0.7, 1.0)
HASHES_OTRA = ("11aa", "22bb", "33cc")
ELEGIDO = 1
X_COPIA = 0.1
HASH_COPIA = "9f04"
OTRA_RAMA = "otra-rama"

Y_CORTE = -0.55
X_ROTULO = -6.35
Y_ROTULO = 1.28
TAM_ROTULO = 15

ANCHO_CONSOLA = 7.8
ALTO_CONSOLA = 2.3
Y_CONSOLA = -2.1
MARGEN_CONSOLA = 0.5
TAM_SESION = 15
BUFF_SESION = 0.16
Y_SESION = Y_CONSOLA + ALTO_CONSOLA / 2 - ALTO_BARRA - 0.25

SESIONES = (
    ((f"git switch {RAMA}", "cmd"),
     ("git rebase main", "cmd")),
    (("git switch main", "cmd"),
     (f"git cherry-pick {HASHES_OTRA[ELEGIDO]}", "cmd")),
)


def _marco_consola():
    return ventana(ANCHO_CONSOLA, ALTO_CONSOLA, "terminal", 14).move_to(
        [0, Y_CONSOLA, 0])


def _sesion(indice):
    filas = VGroup(*[
        linea_terminal(c, t, TAM_SESION) for c, t in SESIONES[indice]
    ]).arrange(DOWN, buff=BUFF_SESION, aligned_edge=LEFT)
    filas.align_to([0, Y_SESION, 0], UP)
    return filas.align_to([-ANCHO_CONSOLA / 2 + MARGEN_CONSOLA, 0, 0], LEFT)


def _mudar(scene, p_head, cartel, run_time=0.9):
    scene.play(p_head.animate.next_to(cartel, RIGHT, buff=BUFF_PUNTERO),
               run_time=run_time)


def _plantar(scene, cartel, p_head, nodo, direccion=UP, run_time=0.6):
    destino = cartel.copy().next_to(nodo, direccion, buff=BUFF_PUNTERO)
    animaciones = [cartel.animate.move_to(destino)]
    if p_head is not None:
        detras = p_head.copy().next_to(destino, RIGHT, buff=BUFF_PUNTERO)
        animaciones.append(p_head.animate.move_to(detras))
    scene.play(*animaciones, run_time=run_time)


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
    alta = VGroup(*[
        nodo_commit(h, RAMA_FEATURE, RADIO, TAM_HASH).move_to([x, Y_ALTA, 0])
        for x, h in zip(X_ALTA, HASHES_ALTA)
    ])
    tronco = VGroup(arista(base[0], base[1], RAMA_MAIN, RADIO),
                    arista(base[1], base[2], RAMA_MAIN, RADIO))
    horquilla = arista(base[1], alta[0], RAMA_FEATURE, RADIO)
    rama_hilo = arista(alta[0], alta[1], RAMA_FEATURE, RADIO)

    p_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    p_main.next_to(base[-1], DOWN, buff=BUFF_PUNTERO)
    p_rama = puntero(RAMA, RAMA_FEATURE, TAM_PUNTERO)
    p_rama.next_to(alta[-1], UP, buff=BUFF_PUNTERO)
    p_head = puntero("HEAD", OK, TAM_PUNTERO)
    p_head.next_to(p_main, RIGHT, buff=BUFF_PUNTERO)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in [*base, *alta]],
                    lag_ratio=0.2),
        FadeIn(rotulo_ramas, shift=RIGHT * 0.15), run_time=1.1,
    )
    scene.play(
        LaggedStart(Create(tronco[0]), Create(tronco[1]), Create(horquilla),
                    Create(rama_hilo), lag_ratio=0.2),
        run_time=0.9,
    )
    scene.play(FadeIn(p_main, shift=UP * 0.1), FadeIn(p_rama, shift=DOWN * 0.1),
               FadeIn(p_head, shift=LEFT * 0.1), run_time=0.5)
    scene.play(Create(corte), FadeIn(rotulo_consola, shift=RIGHT * 0.15),
               run_time=0.6)
    scene.play(FadeIn(marco_consola), run_time=0.5)
    scene.next_slide()

    sesion = _sesion(0)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    _mudar(scene, p_head, p_rama)
    teclear(scene, VGroup(marco_consola, sesion), desde=1, hasta=2, ritmo=0.32)

    nuevos = VGroup(*[
        nodo_commit(h, AMBAR, RADIO, TAM_HASH).move_to([x, Y_BASE, 0])
        for x, h in zip(X_REBASE, HASHES_NUEVOS)
    ])
    scene.play(FadeOut(horquilla), run_time=0.4)
    scene.play(
        ReplacementTransform(alta, nuevos), FadeOut(rama_hilo), run_time=1.1,
    )
    hilos_nuevos = VGroup(arista(base[-1], nuevos[0], AMBAR, RADIO),
                          arista(nuevos[0], nuevos[1], AMBAR, RADIO))
    scene.play(Create(hilos_nuevos[0]), Create(hilos_nuevos[1]), run_time=0.7)
    _plantar(scene, p_rama, p_head, nuevos[-1])
    scene.play(
        LaggedStart(*[
            Flash(n, color=AMBAR, line_length=0.2, num_lines=12,
                  flash_radius=RADIO + 0.3) for n in nuevos
        ], lag_ratio=0.3),
        run_time=0.9,
    )
    teclear(scene, VGroup(marco_consola, sesion), desde=2, ritmo=0.35)
    scene.next_slide()

    main_nodos = VGroup(*[
        nodo_commit(h, RAMA_MAIN, RADIO, TAM_HASH).move_to([x, Y_BASE, 0])
        for x, h in zip(X_BASE, HASHES_BASE)
    ])
    otra = VGroup(*[
        nodo_commit(h, RAMA_FEATURE, RADIO, TAM_HASH).move_to([x, Y_ALTA, 0])
        for x, h in zip(X_OTRA, HASHES_OTRA)
    ])
    hilos = VGroup(
        arista(main_nodos[0], main_nodos[1], RAMA_MAIN, RADIO),
        arista(main_nodos[1], main_nodos[2], RAMA_MAIN, RADIO),
        arista(main_nodos[1], otra[0], RAMA_FEATURE, RADIO),
        arista(otra[0], otra[1], RAMA_FEATURE, RADIO),
        arista(otra[1], otra[2], RAMA_FEATURE, RADIO),
    )
    q_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    q_main.next_to(main_nodos[-1], DOWN, buff=BUFF_PUNTERO)
    q_otra = puntero(OTRA_RAMA, RAMA_FEATURE, TAM_PUNTERO)
    q_otra.next_to(otra[-1], UP, buff=BUFF_PUNTERO)
    q_head = puntero("HEAD", OK, TAM_PUNTERO)
    q_head.next_to(q_otra, RIGHT, buff=BUFF_PUNTERO)

    scene.play(
        FadeOut(base), FadeOut(nuevos), FadeOut(tronco),
        FadeOut(hilos_nuevos), FadeOut(p_main), FadeOut(p_rama),
        FadeOut(p_head), FadeOut(sesion), run_time=0.6,
    )
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in [*main_nodos, *otra]],
                    lag_ratio=0.15),
        run_time=1.1,
    )
    scene.play(
        LaggedStart(*[Create(h) for h in hilos], lag_ratio=0.15),
        run_time=0.9,
    )
    scene.play(FadeIn(q_main, shift=UP * 0.1), FadeIn(q_otra, shift=DOWN * 0.1),
               FadeIn(q_head, shift=LEFT * 0.1), run_time=0.5)
    scene.next_slide()

    sesion = _sesion(1)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    _mudar(scene, q_head, q_main)
    teclear(scene, VGroup(marco_consola, sesion), desde=1, ritmo=0.32)
    scene.play(Indicate(otra[ELEGIDO], color=OK, scale_factor=1.3),
               run_time=0.7)

    copia = nodo_commit(HASH_COPIA, OK, RADIO, TAM_HASH)
    copia.move_to([X_COPIA, Y_BASE, 0])
    hilo_copia = arista(main_nodos[-1], copia, OK, RADIO)
    scene.play(Create(hilo_copia), GrowFromCenter(copia), run_time=0.8)
    _plantar(scene, q_main, q_head, copia, direccion=DOWN)
    scene.play(
        Flash(copia, color=OK, line_length=0.2, num_lines=12,
              flash_radius=RADIO + 0.3),
        Indicate(q_otra, color=RAMA_FEATURE, scale_factor=1.12),
        run_time=0.8,
    )
    scene.wait(0.3)

    scene.next_slide()
