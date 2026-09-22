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
    Transform,
    VGroup,
)

from animaciones import pulso, teclear
from componentes import ALTO_BARRA, arista, linea_terminal, nodo_commit
from componentes import puntero, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, OK, RAMA_FEATURE, RAMA_MAIN, SECUNDARIO

TITULO = "git merge"

Y_BASE = 0.7
Y_ALTA = 1.85
RADIO = 0.33
TAM_HASH = 14
TAM_PUNTERO = 15
BUFF_PUNTERO = 0.28

X_FF_MAIN = (-4.8, -3.0)
X_FF_RAMA = (-1.2, 0.6)
HASHES_FF_MAIN = ("0e5f", "77ab")
HASHES_FF_RAMA = ("a3c1", "b8e2")

X_BASE = (-5.0, -3.3, -1.6)
X_ALTA = (-1.6, 0.1)
X_MERGE = 1.9
RADIO_MERGE = 0.38
HASHES_BASE = ("0e5f", "77ab", "c4f0")
HASHES_ALTA = ("a3c1", "b8e2")
HASH_MERGE = "m9d3"

RAMA = "experimento"

Y_CORTE = -0.55
X_ROTULO = -6.35
Y_ROTULO = 1.28
TAM_ROTULO = 15

ANCHO_CONSOLA = 7.4
ALTO_CONSOLA = 2.3
Y_CONSOLA = -2.1
MARGEN_CONSOLA = 0.5
TAM_SESION = 15
BUFF_SESION = 0.16
Y_SESION = Y_CONSOLA + ALTO_CONSOLA / 2 - ALTO_BARRA - 0.25

SESIONES = (
    ((f"git switch -c {RAMA}", "cmd"),
     ('git commit -m "arregla el pie"', "cmd"),
     ('git commit -m "y el margen"', "cmd")),
    (("git switch main", "cmd"),
     ("Switched to branch 'main'", "ok"),
     (f"git merge {RAMA}", "cmd"),
     ("Fast-forward", "ok")),
    (("git switch main", "cmd"),
     ("Switched to branch 'main'", "ok"),
     (f"git merge {RAMA}", "cmd"),
     ("Merge made by the 'ort' strategy.", "ok")),
    ((f"git merge --no-ff {RAMA}", "cmd"),
     ("Merge made by the 'ort' strategy.", "ok")),
)


X_NOFF_MERGE = 2.4
HASH_NOFF = "e7c2"
ORDEN_NOFF = f"git merge --no-ff {RAMA}"


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


def _plantar(scene, cartel, p_head, nodo, direccion=UP, run_time=0.5):
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

    nodos = VGroup(*[
        nodo_commit(h, RAMA_MAIN, RADIO, TAM_HASH).move_to([x, Y_BASE, 0])
        for x, h in zip(X_FF_MAIN, HASHES_FF_MAIN)
    ])
    aristas = VGroup(arista(nodos[0], nodos[1], RAMA_MAIN, RADIO))
    p_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    p_main.next_to(nodos[-1], DOWN, buff=BUFF_PUNTERO)
    p_head = puntero("HEAD", OK, TAM_PUNTERO)
    p_head.next_to(p_main, RIGHT, buff=BUFF_PUNTERO)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in nodos], lag_ratio=0.25),
        FadeIn(rotulo_ramas, shift=RIGHT * 0.15), run_time=0.9,
    )
    scene.play(Create(aristas[0]), run_time=0.5)
    scene.play(FadeIn(p_main, shift=UP * 0.1), FadeIn(p_head, shift=LEFT * 0.1),
               run_time=0.5)
    scene.play(Create(corte), FadeIn(rotulo_consola, shift=RIGHT * 0.15),
               run_time=0.6)
    scene.play(FadeIn(marco_consola), run_time=0.5)
    scene.next_slide()

    sesion = _sesion(0)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    p_rama = puntero(RAMA, RAMA_FEATURE, TAM_PUNTERO)
    p_rama.next_to(nodos[-1], UP, buff=BUFF_PUNTERO)
    scene.play(FadeIn(p_rama, shift=DOWN * 0.12), run_time=0.5)
    _mudar(scene, p_head, p_rama, run_time=0.7)

    anterior = nodos[-1]
    rama_nodos, rama_aristas = VGroup(), VGroup()
    for i, (x, h) in enumerate(zip(X_FF_RAMA, HASHES_FF_RAMA)):
        teclear(scene, VGroup(marco_consola, sesion), desde=i + 1, hasta=i + 2,
                ritmo=0.32)
        nodo = nodo_commit(h, RAMA_FEATURE, RADIO, TAM_HASH)
        nodo.move_to([x, Y_ALTA, 0])
        ramal = arista(anterior, nodo, RAMA_FEATURE, RADIO)
        scene.play(Create(ramal), GrowFromCenter(nodo), run_time=0.7)
        _plantar(scene, p_rama, p_head, nodo)
        rama_nodos.add(nodo)
        rama_aristas.add(ramal)
        anterior = nodo
    scene.next_slide()

    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(1)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    _mudar(scene, p_head, p_main)
    teclear(scene, VGroup(marco_consola, sesion), desde=1, hasta=3, ritmo=0.32)

    bajados = VGroup(*[
        n.copy().move_to([x, Y_BASE, 0])
        for n, x in zip(rama_nodos, X_FF_RAMA)
    ])
    rectas = VGroup(
        arista(nodos[-1], bajados[0], RAMA_FEATURE, RADIO),
        arista(bajados[0], bajados[1], RAMA_FEATURE, RADIO),
    )
    scene.play(
        *[Transform(n, d) for n, d in zip(rama_nodos, bajados)],
        *[Transform(a, r) for a, r in zip(rama_aristas, rectas)],
        p_rama.animate.next_to(bajados[-1], UP, buff=BUFF_PUNTERO),
        run_time=1.1,
    )
    scene.play(*[pulso(a, RAMA_MAIN, 0.7) for a in rama_aristas], run_time=0.9)
    _plantar(scene, p_main, p_head, rama_nodos[-1], direccion=DOWN,
             run_time=1.0)
    teclear(scene, VGroup(marco_consola, sesion), desde=3, ritmo=0.32)
    scene.next_slide()

    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(3)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)

    subidos = VGroup(*[
        nodo_commit(h, RAMA_FEATURE, RADIO, TAM_HASH).move_to([x, Y_ALTA, 0])
        for x, h in zip(X_FF_RAMA, HASHES_FF_RAMA)
    ])
    horquilla = VGroup(
        arista(nodos[-1], subidos[0], RAMA_FEATURE, RADIO),
        arista(subidos[0], subidos[1], RAMA_FEATURE, RADIO),
    )
    scene.play(
        *[Transform(n, s) for n, s in zip(rama_nodos, subidos)],
        *[Transform(a, h) for a, h in zip(rama_aristas, horquilla)],
        p_rama.animate.next_to(subidos[-1], UP, buff=BUFF_PUNTERO),
        run_time=1.1,
    )

    mff = nodo_commit(HASH_NOFF, RAMA_MAIN, RADIO_MERGE, TAM_HASH)
    mff.move_to([X_NOFF_MERGE, Y_BASE, 0])
    padres_ff = VGroup(arista(nodos[-1], mff, RAMA_MAIN, RADIO),
                       arista(subidos[-1], mff, RAMA_FEATURE, RADIO))

    teclear(scene, VGroup(marco_consola, sesion), desde=1, ritmo=0.32)
    scene.play(Create(padres_ff[0]), Create(padres_ff[1]), run_time=0.8)
    scene.play(
        GrowFromCenter(mff),
        Flash(mff, color=AMBAR, line_length=0.25, num_lines=16,
              flash_radius=RADIO_MERGE + 0.35),
        run_time=0.8,
    )
    _plantar(scene, p_main, p_head, mff, direccion=DOWN, run_time=0.9)
    scene.next_slide()

    base = VGroup(*[
        nodo_commit(h, RAMA_MAIN, RADIO, TAM_HASH).move_to([x, Y_BASE, 0])
        for x, h in zip(X_BASE, HASHES_BASE)
    ])
    alta = VGroup(*[
        nodo_commit(h, RAMA_FEATURE, RADIO, TAM_HASH).move_to([x, Y_ALTA, 0])
        for x, h in zip(X_ALTA, HASHES_ALTA)
    ])
    hilos = VGroup(
        arista(base[0], base[1], RAMA_MAIN, RADIO),
        arista(base[1], base[2], RAMA_MAIN, RADIO),
        arista(base[1], alta[0], RAMA_FEATURE, RADIO),
        arista(alta[0], alta[1], RAMA_FEATURE, RADIO),
    )
    q_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    q_main.next_to(base[-1], DOWN, buff=BUFF_PUNTERO)
    q_rama = puntero(RAMA, RAMA_FEATURE, TAM_PUNTERO)
    q_rama.next_to(alta[-1], UP, buff=BUFF_PUNTERO)
    q_head = puntero("HEAD", OK, TAM_PUNTERO)
    q_head.next_to(q_rama, RIGHT, buff=BUFF_PUNTERO)

    scene.play(
        FadeOut(nodos), FadeOut(aristas), FadeOut(rama_nodos),
        FadeOut(rama_aristas), FadeOut(p_main), FadeOut(p_rama),
        FadeOut(p_head), FadeOut(sesion), FadeOut(mff), FadeOut(padres_ff),
        run_time=0.6,
    )
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in [*base, *alta]],
                    lag_ratio=0.22),
        run_time=1.1,
    )
    scene.play(
        LaggedStart(*[Create(h) for h in hilos], lag_ratio=0.22),
        run_time=0.9,
    )
    scene.play(FadeIn(q_main, shift=UP * 0.1), FadeIn(q_rama, shift=DOWN * 0.1),
               FadeIn(q_head, shift=LEFT * 0.1), run_time=0.5)
    scene.next_slide()

    sesion = _sesion(2)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    _mudar(scene, q_head, q_main)
    teclear(scene, VGroup(marco_consola, sesion), desde=1, hasta=3, ritmo=0.32)

    m = nodo_commit(HASH_MERGE, RAMA_MAIN, RADIO_MERGE, TAM_HASH)
    m.move_to([X_MERGE, Y_BASE, 0])
    padres = VGroup(arista(base[-1], m, RAMA_MAIN, RADIO),
                    arista(alta[-1], m, RAMA_FEATURE, RADIO))
    scene.play(Create(padres[0]), Create(padres[1]), run_time=0.8)
    scene.play(
        GrowFromCenter(m),
        Flash(m, color=RAMA_MAIN, line_length=0.25, num_lines=16,
              flash_radius=RADIO_MERGE + 0.35),
        run_time=0.8,
    )
    _plantar(scene, q_main, q_head, m, direccion=DOWN, run_time=0.8)
    scene.play(*[pulso(p, CLARO, 0.8) for p in padres], run_time=1.0)
    teclear(scene, VGroup(marco_consola, sesion), desde=3, ritmo=0.32)
    scene.next_slide()

    con_bandera = linea_terminal(ORDEN_NOFF, "cmd", TAM_SESION)
    con_bandera.move_to(sesion[2], LEFT)
    scene.play(Transform(sesion[2], con_bandera), run_time=0.9)
    scene.play(Indicate(m, color=RAMA_MAIN, scale_factor=1.12),
               *[pulso(p, RAMA_MAIN, 0.7) for p in padres], run_time=1.0)
    scene.wait(0.3)

    scene.next_slide()
