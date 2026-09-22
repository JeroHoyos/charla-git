from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
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

from componentes import archivo, nodo_commit, puntero, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, OK, RAMA_MAIN, SECUNDARIO

TITULO = "git checkout"

X_CADENA = (-4.6, -1.55, 1.55, 4.6)
Y_CADENA = 1.35
RADIO = 0.4
TAM_HASH = 16
HASHES = ("0e5f", "77ab", "9c1d", "3f2a")
DESTINO = 1
TAM_PUNTERO = 15
BUFF_PUNTERO = 0.4

Y_CORTE = -0.4
X_ROTULO = -6.35

ARCHIVOS = ("informe.md", "datos.csv", "notas.md")
X_ARCHIVOS = (-2.6, 0.0, 2.6)
Y_ARCHIVOS = -1.65
ALTO_ARCHIVO = 0.6
TAM_NOMBRE = 13
TAM_VERSION = 12

AL_DIA = ((HASHES[-1], RAMA_MAIN),) * 3
EN_PASADO = ((HASHES[DESTINO], AMBAR),) * 3

TAM_ORDEN = 20
TAM_ROTULO = 15
Y_ORDEN = -3.05


def _orden(contenido, color=CLARO):
    return texto(contenido, TAM_ORDEN, color=color).move_to([0, Y_ORDEN, 0])


def _archivo(indice, version, color):
    icono = archivo(ARCHIVOS[indice], color=color, alto=ALTO_ARCHIVO,
                    tam=TAM_NOMBRE)
    sello = texto(version, TAM_VERSION, color=color)
    sello.next_to(icono, DOWN, buff=0.16)
    return VGroup(icono, sello).move_to([X_ARCHIVOS[indice], Y_ARCHIVOS, 0])


def _carpeta(estados):
    return VGroup(*[
        _archivo(i, version, color)
        for i, (version, color) in enumerate(estados)
    ])


def construir(scene):
    encabezado = hacer_titulo(TITULO)

    nodos = VGroup(*[
        nodo_commit(h, RAMA_MAIN, RADIO, TAM_HASH).move_to([x, Y_CADENA, 0])
        for x, h in zip(X_CADENA, HASHES)
    ])
    aristas = VGroup(*[
        Line(nodos[i].get_center() + RIGHT * RADIO,
             nodos[i + 1].get_center() + LEFT * RADIO,
             color=RAMA_MAIN, stroke_width=4)
        for i in range(len(nodos) - 1)
    ])
    p_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    p_main.next_to(nodos[-1], DOWN, buff=BUFF_PUNTERO)
    p_head = puntero("HEAD", OK, TAM_PUNTERO)
    p_head.next_to(nodos[-1], UP, buff=BUFF_PUNTERO)

    corte = Line([-6.6, Y_CORTE, 0], [6.6, Y_CORTE, 0],
                 color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.3)
    rotulo_rama = texto("la rama", TAM_ROTULO, color=SECUNDARIO)
    rotulo_rama.move_to([X_ROTULO, Y_CADENA, 0], LEFT)
    rotulo_carpeta = texto("tu carpeta ahora", TAM_ROTULO, color=SECUNDARIO)
    rotulo_carpeta.move_to([X_ROTULO, Y_ARCHIVOS, 0], LEFT)

    carpeta = _carpeta(AL_DIA)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in nodos], lag_ratio=0.25),
        FadeIn(rotulo_rama, shift=RIGHT * 0.15), run_time=0.9,
    )
    scene.play(
        LaggedStart(*[Create(a) for a in aristas], lag_ratio=0.25),
        run_time=0.6,
    )
    scene.play(FadeIn(p_main, shift=UP * 0.1), FadeIn(p_head, shift=DOWN * 0.1),
               run_time=0.5)
    scene.play(Create(corte), FadeIn(rotulo_carpeta, shift=RIGHT * 0.15),
               run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(f) for f in carpeta], lag_ratio=0.25),
        run_time=0.9,
    )
    scene.next_slide()

    orden = _orden(f"git checkout {HASHES[DESTINO]}")
    scene.play(FadeIn(orden, shift=UP * 0.1), run_time=0.45)

    suelto = puntero("HEAD", AMBAR, TAM_PUNTERO)
    suelto.next_to(nodos[DESTINO], UP, buff=BUFF_PUNTERO)
    scene.play(Transform(p_head, suelto), run_time=1.0)

    mirilla = Circle(radius=RADIO + 0.18, color=AMBAR, stroke_width=3)
    mirilla.set_stroke(opacity=0.75).move_to(nodos[DESTINO].get_center())
    etiqueta = texto("detached HEAD", 14, color=AMBAR)
    etiqueta.next_to(p_head, LEFT, buff=0.3)
    scene.play(
        GrowFromCenter(mirilla),
        Flash(nodos[DESTINO], color=AMBAR, line_length=0.22, num_lines=16,
              flash_radius=RADIO + 0.4),
        Indicate(p_main, color=RAMA_MAIN, scale_factor=1.15),
        FadeIn(etiqueta, shift=RIGHT * 0.1),
        run_time=0.9,
    )

    viejos = _carpeta(EN_PASADO)
    scene.play(
        LaggedStart(*[Transform(carpeta[i], viejos[i]) for i in range(3)],
                    lag_ratio=0.2),
        run_time=1.0,
    )
    scene.next_slide()

    vuelta = _orden("git checkout main", color=OK)
    scene.play(FadeOut(orden), FadeOut(etiqueta),
               FadeIn(vuelta, shift=UP * 0.1), run_time=0.6)

    pegado = puntero("HEAD", OK, TAM_PUNTERO)
    pegado.next_to(nodos[-1], UP, buff=BUFF_PUNTERO)
    nuevos = _carpeta(AL_DIA)
    scene.play(Transform(p_head, pegado), FadeOut(mirilla), run_time=0.9)
    scene.play(
        LaggedStart(*[Transform(carpeta[i], nuevos[i]) for i in range(3)],
                    lag_ratio=0.2),
        Flash(nodos[-1], color=OK, line_length=0.22, num_lines=16,
              flash_radius=RADIO + 0.4),
        run_time=1.0,
    )
    scene.wait(0.3)

    scene.next_slide()
