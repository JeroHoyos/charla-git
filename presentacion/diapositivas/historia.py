from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    Line,
    FadeOut,
    Flash,
    GrowFromCenter,
    GrowFromEdge,
    Group,
    LaggedStart,
    VGroup,
)

from componentes import barra, fotografia, puntero, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, ERROR, FONT_TITULO, PRIMARIO, SECUNDARIO

TITULO = "El origen"
TITULO_HOY = "El estándar"

X_FOTO = -4.55
Y_FOTO = -0.1
ANCHO_FOTO = 3.8

X_COL = -1.9
Y_COL = -0.1

TOP500 = "de los 500 supercomputadores del mundo"
FUENTE_TOP500 = "TOP500 · SQ Magazine"

ATASCO = (
    ("CVS · Subversion", "demasiado lentas"),
    ("BitKeeper", "de pago"),
)
X_PEGA = 4.5
GOLPE = "2005 · le retiran la licencia"

DIAS = 10
LADO_DIA = 0.34

ENCUESTA = (
    ("Git", 93.87),
    ("SVN", 5.18),
    ("no uso ninguno", 4.31),
    ("Mercurial", 1.13),
)
X_ETIQUETA = -3.9
X_BARRA = -3.6
LARGO_100 = 7.8
ALTO_BARRA = 0.6
Y_PRIMERA_BARRA = 1.55
PASO_BARRA = 1.15
FUENTE_ENCUESTA = "Stack Overflow Developer Survey 2022"


def _colocar(bloque):
    return bloque.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(
        [X_COL, Y_COL, 0], LEFT)


def _acto_linux():
    ficha = Group(
        fotografia("linux", 1.5, giro=0),
        texto("Linux · 1991", 26, color=CLARO),
    ).arrange(RIGHT, buff=0.5)
    return _colocar(Group(
        ficha,
        texto("100%", 64, color=PRIMARIO, font=FONT_TITULO),
        texto(TOP500, 22),
        texto(FUENTE_TOP500, 14, color=SECUNDARIO).set_opacity(0.7),
    ))


def _fila_atasco(nombre, pega):
    ficha = puntero(nombre, SECUNDARIO, 22, relleno=0.08)
    ficha.move_to([0, 0, 0], LEFT)
    tachon = Line(ficha.get_left() + RIGHT * 0.14,
                  ficha.get_right() + LEFT * 0.14,
                  color=ERROR, stroke_width=4)
    return VGroup(
        ficha, tachon,
        texto(pega, 22, color=ERROR).move_to([X_PEGA, 0, 0], LEFT),
    )


def _acto_atasco():
    cabecera = VGroup(
        texto("1.000", 40, color=CLARO),
        texto("personas, un kernel", 24, color=SECUNDARIO),
    ).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
    return _colocar(Group(
        cabecera,
        _fila_atasco(*ATASCO[0]),
        _fila_atasco(*ATASCO[1]),
        texto(GOLPE, 24, color=AMBAR),
    ))


def _acto_diez_dias():
    dias = VGroup(*[
        barra(LADO_DIA, LADO_DIA, PRIMARIO, 0.9) for _ in range(DIAS)
    ]).arrange(RIGHT, buff=0.16)
    remate = Group(
        texto("10", 64, color=PRIMARIO, font=FONT_TITULO),
        texto("días", 26, color=CLARO),
        fotografia("git", 2.3, giro=0),
    ).arrange(RIGHT, buff=0.45, aligned_edge=DOWN)
    return _colocar(Group(
        dias,
        remate,
        texto("y a los 4 meses, a la comunidad", 22, color=SECUNDARIO),
    ))


def _grafica():
    filas = VGroup()
    for i, (nombre, porcentaje) in enumerate(ENCUESTA):
        y = Y_PRIMERA_BARRA - i * PASO_BARRA
        destacado = i == 0
        color = PRIMARIO if destacado else SECUNDARIO
        etiqueta = texto(nombre, 22, color=CLARO if destacado else SECUNDARIO)
        etiqueta.move_to([X_ETIQUETA, y, 0], RIGHT)
        trazo = barra(LARGO_100 * porcentaje / 100, ALTO_BARRA, color,
                      1.0 if destacado else 0.55)
        trazo.move_to([X_BARRA, y, 0], LEFT)
        valor = texto(f"{porcentaje:.2f} %".replace(".", ","), 22,
                      color=CLARO if destacado else SECUNDARIO)
        valor.next_to(trazo, RIGHT, buff=0.22)
        filas.add(VGroup(etiqueta, trazo, valor))

    fuente = texto(FUENTE_ENCUESTA, 18, color=SECUNDARIO).move_to([0, -3.05, 0])
    return filas, fuente


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    retrato = fotografia("trovalds", ANCHO_FOTO, pie="Linus Torvalds")
    retrato.move_to([X_FOTO, Y_FOTO, 0])

    linux = _acto_linux()
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(retrato, scale=0.92), run_time=0.8)
    scene.play(
        LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in linux],
                    lag_ratio=0.35),
        run_time=1.4,
    )
    scene.next_slide()

    atasco = _acto_atasco()
    scene.play(FadeOut(linux), run_time=0.5)
    scene.play(
        LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in atasco[:-1]],
                    lag_ratio=0.4),
        run_time=1.3,
    )
    scene.play(FadeIn(atasco[-1], shift=UP * 0.12), run_time=0.5)
    scene.next_slide()

    diez = _acto_diez_dias()
    dias, remate, cierre = diez
    scene.play(FadeOut(atasco), run_time=0.5)
    scene.play(
        LaggedStart(*[GrowFromCenter(d) for d in dias], lag_ratio=0.35),
        run_time=1.5,
    )
    scene.play(FadeIn(remate[0], shift=UP * 0.12), FadeIn(remate[1]),
               run_time=0.5)
    scene.play(FadeIn(remate[2], scale=0.9), run_time=0.5)
    scene.play(
        Flash(remate[2], color=PRIMARIO, line_length=0.3, num_lines=18,
              flash_radius=1.3),
        run_time=0.7,
    )
    scene.play(FadeIn(cierre, shift=RIGHT * 0.15), run_time=0.5)
    scene.next_slide()

    encabezado_hoy = hacer_titulo(TITULO_HOY)
    filas, fuente = _grafica()

    scene.play(
        FadeOut(retrato), FadeOut(diez),
        FadeOut(encabezado), FadeIn(encabezado_hoy, shift=DOWN * 0.2),
        run_time=0.8,
    )
    for etiqueta, trazo, valor in filas:
        scene.play(
            FadeIn(etiqueta, shift=RIGHT * 0.1),
            GrowFromEdge(trazo, LEFT),
            run_time=0.55,
        )
        scene.play(FadeIn(valor, shift=LEFT * 0.1), run_time=0.25)
    scene.play(FadeIn(fuente), run_time=0.5)
    scene.wait(0.3)

    scene.next_slide()
