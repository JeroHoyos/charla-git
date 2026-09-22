from manim import (
    DOWN,
    LEFT,
    RIGHT,
    FadeIn,
    FadeOut,
    LaggedStart,
    VGroup,
)

from animaciones import teclear
from componentes import linea_terminal, puntero, terminal, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, OK, RAMA_MAIN, SECUNDARIO

from .mensajes_commit import AMBITO, DESCRIPCION, TIPO

TITULOS = (
    "Conventional Commits",
    "feat y fix",
    "El resto",
    "Cuerpo del commit",
)

FORMA = "<tipo>[ámbito]: <descripción>"
ORDEN_LINEA = f'git commit -m "{TIPO}{AMBITO}: {DESCRIPCION}"'
TAM_LINEA = 21
Y_LINEA = 1.35

PIEZAS = (
    (TIPO, "el tipo: qué clase de cambio es", OK),
    (AMBITO, "el ámbito: qué parte tocaste, opcional", AMBAR),
    ("entrena...", "la descripción: qué hace, en presente", CLARO),
)
X_PIEZA, X_QUE_ES = -6.0, -3.55
Y_PIEZAS = 0.1
PASO_PIEZA = 1.15
TAM_FORMA = 21

PRINCIPALES = (
    ("feat", OK, "introduce una funcionalidad nueva",
     'git commit -m "feat: anade el cargador de CSV"'),
    ("fix", RAMA_MAIN, "corrige un error en el código",
     f'git commit -m "{TIPO}: {DESCRIPCION}"'),
)
X_CHIP = -6.0
X_CUANDO = -5.0
TAM_CUANDO = 21
TAM_ORDEN = 21
Y_PRINCIPALES = (1.05, -1.2)
BAJADA_ORDEN = 0.8

SECUNDARIOS = (
    ("docs", "solo documentación"),
    ("style", "formato, sin tocar el código"),
    ("refactor", "otro código, mismo resultado"),
    ("perf", "lo mismo, pero más rápido"),
    ("test", "solo pruebas"),
    ("ci", "el pipeline, los workflows"),
    ("chore", "dependencias y limpieza"),
)
X_TIPO_RESTO, X_GLOSA_RESTO = -5.2, -2.9
Y_RESTO = 1.9
PASO_RESTO = 0.66
TAM_RESTO = 21
ORDEN_SECUNDARIO = 'git commit -m "chore: sube pandas a 2.2"'
Y_ORDEN_SECUNDARIO = -2.9

CORTE = "\\"
SESION = (
    (f'git commit -m "{TIPO}{AMBITO}: {DESCRIPCION}" {CORTE}', "cmd"),
    ('-m "Ajustaba con el conjunto de prueba y eso sesgaba la metrica."',
     "out"),
)
TAM_SESION = 17
MARGEN_SESION = 0.6
Y_SESION = 1.0
SANGRIA_SESION = 1.95

PARRAFOS = (
    ("el título resume el cambio en una línea", CLARO),
    ("el cuerpo explica por qué era necesario", SECUNDARIO),
)
X_PARRAFO = -5.2
BUFF_PARRAFO = 0.9
Y_PARRAFOS = -1.55
PASO_PARRAFO = 1.0
TAM_PARRAFO = 27


def _orden_despiezada():
    completa = f"$ {ORDEN_LINEA}"
    t2c = {"[0:1]": OK, "[2:12]": RAMA_MAIN}
    for trozo, color in ((TIPO, OK), (AMBITO, AMBAR)):
        i = completa.index(trozo)
        t2c[f"[{i}:{i + len(trozo)}]"] = color
    return texto(completa, TAM_LINEA, color=CLARO, t2c=t2c)


def construir(scene):
    encabezado = hacer_titulo(TITULOS[0])
    forma = texto(FORMA, TAM_FORMA, color=RAMA_MAIN).move_to([0, 2.4, 0])
    linea = _orden_despiezada().move_to([0, Y_LINEA, 0])
    piezas = VGroup()
    for i, (trozo, que_es, color) in enumerate(PIEZAS):
        y = Y_PIEZAS - i * PASO_PIEZA
        piezas.add(VGroup(
            texto(trozo, TAM_LINEA, color=color).move_to(
                [X_PIEZA, y, 0], LEFT),
            texto(que_es, TAM_LINEA, color=SECUNDARIO).move_to(
                [X_QUE_ES, y, 0], LEFT),
        ))

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(forma, shift=DOWN * 0.1), run_time=0.5)
    scene.play(FadeIn(linea, shift=RIGHT * 0.15), run_time=0.7)
    for pieza in piezas:
        scene.play(FadeIn(pieza, shift=RIGHT * 0.12), run_time=0.6)
    scene.next_slide()

    tipos_encabezado = hacer_titulo(TITULOS[1])
    bloques = VGroup()
    for (tipo, color, cuando, orden), y in zip(PRINCIPALES, Y_PRINCIPALES):
        chip = puntero(tipo, color, 21).move_to([X_CHIP, y, 0])
        bloques.add(VGroup(
            chip,
            texto(cuando, TAM_CUANDO, color=CLARO).move_to(
                [X_CUANDO, y, 0], LEFT),
            linea_terminal(orden, "cmd", TAM_ORDEN).move_to(
                [X_CUANDO, y - BAJADA_ORDEN, 0], LEFT),
        ))

    scene.play(
        FadeOut(forma), FadeOut(linea), FadeOut(piezas),
        FadeOut(encabezado), FadeIn(tipos_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    for bloque in bloques:
        scene.play(
            LaggedStart(*[FadeIn(m, shift=RIGHT * 0.12) for m in bloque],
                        lag_ratio=0.4),
            run_time=1.2,
        )
    scene.next_slide()

    resto_encabezado = hacer_titulo(TITULOS[2])
    rejilla = VGroup()
    for i, (tipo, cuando) in enumerate(SECUNDARIOS):
        y = Y_RESTO - i * PASO_RESTO
        chip = puntero(tipo, SECUNDARIO, TAM_RESTO)
        chip.move_to([X_TIPO_RESTO, y, 0], LEFT)
        rejilla.add(VGroup(chip, texto(cuando, TAM_RESTO, color=CLARO)
                           .move_to([X_GLOSA_RESTO, y, 0], LEFT)))
    ejemplo = linea_terminal(ORDEN_SECUNDARIO, "cmd", TAM_RESTO)
    ejemplo.move_to([0, Y_ORDEN_SECUNDARIO, 0])

    scene.play(
        FadeOut(bloques),
        FadeOut(tipos_encabezado), FadeIn(resto_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.12) for f in rejilla],
                    lag_ratio=0.25),
        run_time=2.0,
    )
    scene.play(FadeIn(ejemplo, shift=DOWN * 0.1), run_time=0.5)
    scene.next_slide()

    ultimo_encabezado = hacer_titulo(TITULOS[3])
    anchos = [
        linea_terminal(c, t, TAM_SESION).width + (SANGRIA_SESION if i else 0)
        for i, (c, t) in enumerate(SESION)
    ]
    sesion = terminal(SESION, tam=TAM_SESION, margen=MARGEN_SESION,
                      ancho=max(anchos) + 2 * MARGEN_SESION, nombre="terminal")
    sesion.move_to([0, Y_SESION, 0])
    for fila in sesion[1][1:]:
        fila.shift(RIGHT * SANGRIA_SESION)

    parrafos = VGroup()
    for i, (que_es, color) in enumerate(PARRAFOS):
        y = Y_PARRAFOS - i * PASO_PARRAFO
        parrafos.add(VGroup(
            texto("-m", TAM_PARRAFO, color=color).move_to(
                [X_PARRAFO, y, 0], LEFT),
            texto(que_es, TAM_PARRAFO, color=CLARO).move_to(
                [X_PARRAFO + BUFF_PARRAFO, y, 0], LEFT),
        ))

    scene.play(
        FadeOut(rejilla), FadeOut(ejemplo),
        FadeOut(resto_encabezado), FadeIn(ultimo_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(sesion[0]), run_time=0.5)
    teclear(scene, sesion, ritmo=0.35)
    for parrafo in parrafos:
        scene.play(FadeIn(parrafo, shift=RIGHT * 0.12), run_time=0.5)
    scene.next_slide()
