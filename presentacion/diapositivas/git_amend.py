from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedLine,
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

from componentes import (
    archivo,
    arista,
    aspa,
    enmarcar,
    nodo_commit,
    nodo_fantasma,
    puntero,
    texto,
)
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, ERROR, OK, RAMA_MAIN, SECUNDARIO

TITULO = "git commit --amend"

X_CADENA = (-4.3, -1.75, 0.8)
Y_CADENA = 0.75
Y_FANTASMA = 2.3
RADIO = 0.38
TAM_HASH = 15
HASHES = ("0e5f", "77ab", "9c1d")
NUEVO = "b41e"
TAM_PUNTERO = 15
BUFF_PUNTERO = 0.34
TAM_SELLO = 15

Y_CORTE = -0.35
X_ROTULO = -6.35
TAM_ROTULO = 15

MENSAJE_MALO = '"corrgie la tabla 2"'
MENSAJE_BUENO = '"corrige la tabla 2"'
ERRATA = {"[1:8]": ERROR}
TAM_MENSAJE = 21
Y_MENSAJE = -1.05
Y_ROTULO_ABAJO = -1.7

ARCHIVOS = ("informe.md", "datos.csv")
FUERA = 1
X_ARCHIVOS = (-1.5, 1.5)
Y_ARCHIVOS = -2.2
ALTO_ARCHIVO = 0.62
TAM_NOMBRE = 14

TAM_ORDEN = 20
Y_ORDEN = -3.1


def _orden(contenido, color=CLARO):
    return texto(contenido, TAM_ORDEN, color=color).move_to([0, Y_ORDEN, 0])


def _mensaje(contenido, color=CLARO, t2c=None):
    return texto(contenido, TAM_MENSAJE, color=color,
                 t2c=t2c).move_to([0, Y_MENSAJE, 0])


def _archivo(indice, color):
    icono = archivo(ARCHIVOS[indice], color=color, alto=ALTO_ARCHIVO,
                    tam=TAM_NOMBRE)
    return icono.move_to([X_ARCHIVOS[indice], Y_ARCHIVOS, 0])


def _sello():
    fila = VGroup(aspa(ERROR, tam=0.11, grosor=4),
                  texto("reemplazado", TAM_SELLO, color=ERROR))
    fila.arrange(RIGHT, buff=0.2)
    return VGroup(enmarcar(fila, margen=0.36, color=ERROR), fila)


def _relevo(fantasma, nuevo):
    linea = DashedLine(
        fantasma.get_bottom() + DOWN * 0.12,
        nuevo.get_top() + UP * 0.26,
        color=AMBAR, stroke_width=3.5, dash_length=0.13,
    )
    return linea.add_tip(tip_length=0.24, tip_width=0.22)


def construir(scene):
    encabezado = hacer_titulo(TITULO)

    nodos = VGroup(*[
        nodo_commit(h, RAMA_MAIN, RADIO, TAM_HASH).move_to([x, Y_CADENA, 0])
        for x, h in zip(X_CADENA, HASHES)
    ])
    aristas = VGroup(*[
        arista(nodos[i], nodos[i + 1], RAMA_MAIN, RADIO)
        for i in range(len(nodos) - 1)
    ])
    p_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    p_main.next_to(nodos[-1], RIGHT, buff=BUFF_PUNTERO)
    p_head = puntero("HEAD", OK, TAM_PUNTERO)
    p_head.next_to(p_main, RIGHT, buff=0.22)

    corte = Line([-6.6, Y_CORTE, 0], [6.6, Y_CORTE, 0],
                 color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.3)
    rotulo_rama = texto("la rama", TAM_ROTULO, color=SECUNDARIO)
    rotulo_rama.move_to([X_ROTULO, Y_CADENA, 0], LEFT)
    rotulo_commit = texto("el último commit", TAM_ROTULO, color=SECUNDARIO)
    rotulo_commit.move_to([X_ROTULO, Y_ROTULO_ABAJO, 0], LEFT)

    mensaje = _mensaje(MENSAJE_MALO, t2c=ERRATA)
    contenido = VGroup(_archivo(0, RAMA_MAIN), _archivo(FUERA, ERROR))
    cruz = aspa(ERROR, tam=0.2, grosor=6)
    cruz.move_to(contenido[FUERA][0].get_center())

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in nodos], lag_ratio=0.25),
        FadeIn(rotulo_rama, shift=RIGHT * 0.15), run_time=0.9,
    )
    scene.play(
        LaggedStart(*[Create(a) for a in aristas], lag_ratio=0.25),
        run_time=0.5,
    )
    scene.play(FadeIn(p_main, shift=LEFT * 0.1),
               FadeIn(p_head, shift=LEFT * 0.1), run_time=0.5)
    scene.play(Create(corte), FadeIn(rotulo_commit, shift=RIGHT * 0.15),
               run_time=0.6)
    scene.play(FadeIn(mensaje, shift=UP * 0.1), run_time=0.5)
    scene.play(
        LaggedStart(*[GrowFromCenter(f) for f in contenido], lag_ratio=0.3),
        run_time=0.7,
    )
    scene.play(GrowFromCenter(cruz),
               Indicate(mensaje, color=ERROR, scale_factor=1.06), run_time=0.7)
    scene.next_slide()

    add = _orden(f"git add {ARCHIVOS[FUERA]}")
    scene.play(FadeIn(add, shift=UP * 0.1), run_time=0.45)
    scene.play(
        FadeOut(cruz, scale=1.5),
        Transform(contenido[FUERA], _archivo(FUERA, AMBAR)),
        run_time=0.7,
    )
    scene.next_slide()

    orden = _orden(f"git commit --amend -m {MENSAJE_BUENO}")
    scene.play(FadeOut(add), FadeIn(orden, shift=UP * 0.1), run_time=0.6)

    fantasma = nodo_fantasma(HASHES[-1], ERROR, RADIO, TAM_HASH)
    fantasma.move_to([X_CADENA[-1], Y_FANTASMA, 0])
    scene.play(Transform(nodos[-1], fantasma), FadeOut(aristas[-1]),
               run_time=0.9)

    nuevo = nodo_commit(NUEVO, OK, RADIO, TAM_HASH)
    nuevo.move_to([X_CADENA[-1], Y_CADENA, 0])
    hilo = arista(nodos[-2], nuevo, OK, RADIO)
    relevo = _relevo(fantasma, nuevo)
    sello = _sello().next_to(fantasma, RIGHT, buff=0.5)

    scene.play(Create(hilo), GrowFromCenter(nuevo), run_time=0.7)
    scene.play(
        Create(relevo),
        FadeIn(sello, shift=LEFT * 0.15),
        Flash(nuevo, color=OK, line_length=0.22, num_lines=16,
              flash_radius=RADIO + 0.4),
        run_time=0.9,
    )
    scene.play(
        Transform(mensaje, _mensaje(MENSAJE_BUENO)),
        Transform(contenido[FUERA], _archivo(FUERA, RAMA_MAIN)),
        Indicate(p_main, color=RAMA_MAIN, scale_factor=1.12),
        Indicate(p_head, color=OK, scale_factor=1.12),
        run_time=0.9,
    )
    scene.play(Indicate(nodos[-1], color=AMBAR, scale_factor=1.15),
               run_time=0.8)

    scene.next_slide()
