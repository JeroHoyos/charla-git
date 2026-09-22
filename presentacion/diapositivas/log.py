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
    LaggedStart,
    Line,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    VGroup,
)

from animaciones import teclear
from componentes import (
    arista,
    foto_proyecto,
    linea_terminal,
    nodo_commit,
    texto,
    ventana,
)
from componentes import titulo as hacer_titulo
from estilo import AMBAR, RAMA_FEATURE, RAMA_MAIN, SECUNDARIO

from .que_es_un_commit import (
    COMMITS,
    RADIO,
    TAM_HASH,
    X_CADENA,
    cadena,
    mensajes,
)
from .tres_zonas import HASH, MENSAJE

TITULO = "git log"

Y_CADENA = 1.72
Y_FOTO = 2.45
ESCALA_FOTO = 0.6

ANCHO_TERM, ALTO_TERM = 9.8, 4.0
Y_TERM = -1.45
NOMBRE_TERM = "terminal"
TAM_TERM = 14
BUFF_TERM = 0.13
X_FILAS = -4.35
SANGRIA = 0.42
Y_ORDEN = 0.0
Y_SALIDA = -0.5
PASO_FILA = 0.33

HASH_LARGO = f"{HASH}8a1c4f2b9e07"
HASH_PREVIO = "9c1d04a7b3e5f168"
AUTOR = "carmen_electra <carmen.electra@unal.edu.co>"

FICHA_LARGA = (
    (f"commit {HASH_LARGO}", "out"),
    (f"Author: {AUTOR}", "out"),
    ("Date:   Fri Sep 5 18:20 2025", "out"),
    ("", "sep"),
    (f"    {MENSAJE}", "txt"),
)
FICHA_SIGUIENTE = (
    (f"commit {HASH_PREVIO}", "out"),
    (f"Author: {AUTOR}", "out"),
)
DESVANECIDO = (0.4, 0.2)
Y_SIGUIENTE = -2.15

ALTO_PAGER = 0.5
MARGEN_PAGER = 0.1

PEGATINA = "(HEAD -> main)"
BANDERAS = (
    ("--oneline", "cada commit en una sola línea"),
    ("--all", "los commits de todas las ramas"),
    ("--graph", "dibuja el grafo de ramas y fusiones"),
)
X_BANDERA, X_GLOSA = 0.1, 1.3
Y_GLOSA = -2.35
PASO_GLOSA = 0.46
TAM_GLOSA = 13

X_LINEAS = X_FILAS + 0.42
X_GRAFO = X_FILAS + 0.08
X_TRONCO = X_GRAFO + 0.06
HUECO_GRAFO = 0.08

RAMAS = (
    ("dotfiles", AMBAR, 2, None,
     (("c30b", "mis dotfiles", 3.4, 1),)),
    ("hyprland", RAMA_FEATURE, 1, 2,
     (("5f7d", "ajusta waybar", 0.5, 3),
      ("a91c", "cambio de wm", -0.6, 4))),
)
N_FILAS_RAMA = sum(len(commits) for *_, commits in RAMAS)

FILAS_TRONCO = (0, 2, 5, 6)
Y_NODO_RAMA = 1.05
SANGRIA_RAMA = 0.26
X_RAMA_COL = X_TRONCO + SANGRIA_RAMA


def _filas(lineas, y_arriba, tam=TAM_TERM, buff=BUFF_TERM, opacidades=None,
           x=X_FILAS):
    filas = VGroup(*[
        linea_terminal(c, t, tam) for c, t in lineas
    ]).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    filas.align_to([0, y_arriba, 0], UP)
    filas.align_to([x, 0, 0], LEFT)
    for fila, (contenido, _) in zip(filas, lineas):
        if contenido.startswith(" "):
            fila.shift(RIGHT * SANGRIA)
    if opacidades:
        for fila, op in zip(filas, opacidades):
            fila.set_opacity(op)
    return filas


def _tecla(letra, rotulo, color=AMBAR):
    letras = texto(letra, 14, color=color)
    tapa = RoundedRectangle(
        width=0.38, height=0.34, corner_radius=0.07,
        stroke_color=color, stroke_width=2.5,
    ).set_fill(color, opacity=0.14)
    letras.move_to(tapa.get_center())
    return VGroup(
        VGroup(tapa, letras), texto(rotulo, 13, color=color),
    ).arrange(RIGHT, buff=0.2)


def _glosa(i):
    bandera, que_hace = BANDERAS[i]
    y = Y_GLOSA + (1 - i) * PASO_GLOSA
    return VGroup(
        texto(bandera, TAM_GLOSA, color=RAMA_MAIN).move_to(
            [X_BANDERA, y, 0], LEFT),
        texto(que_hace, TAM_GLOSA, color=SECUNDARIO).move_to(
            [X_GLOSA, y, 0], LEFT),
    )


def _pager(marco):
    caja = marco[0]
    barra = RoundedRectangle(
        width=caja.width - 2 * MARGEN_PAGER - 0.16, height=ALTO_PAGER,
        corner_radius=0.09, stroke_color=AMBAR, stroke_width=1.5,
    ).set_fill(AMBAR, opacity=0.09)
    barra.set_stroke(opacity=0.4)
    barra.move_to([0, caja.get_bottom()[1] + MARGEN_PAGER + ALTO_PAGER / 2, 0])
    dos_puntos = texto(":", 16, color=AMBAR)
    dos_puntos.move_to(barra.get_left() + RIGHT * 0.42)
    salida = _tecla("q", "para salir")
    salida.next_to(barra.get_right(), LEFT, buff=0.35)
    return VGroup(barra, dos_puntos, salida)


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    nodos, aristas = cadena(Y_CADENA)
    fotos = VGroup(*[
        foto_proyecto(ESCALA_FOTO,
                      RAMA_MAIN if ultimo else SECUNDARIO, vacia=not ultimo)
        .move_to([x, Y_FOTO, 0])
        for x, ultimo in zip(X_CADENA, (False, False, False, True))
    ])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[
            LaggedStart(GrowFromCenter(nodo), FadeIn(foto), lag_ratio=0.4)
            for nodo, foto in zip(nodos, fotos)
        ], lag_ratio=0.35),
        run_time=1.4,
    )
    scene.play(
        LaggedStart(*[Create(a) for a in aristas], lag_ratio=0.3),
        run_time=0.7,
    )
    rotulos = mensajes(Y_CADENA)
    scene.play(
        *[Transform(foto, rotulo) for foto, rotulo in zip(fotos, rotulos)],
        run_time=0.8,
    )

    marco = ventana(ANCHO_TERM, ALTO_TERM, NOMBRE_TERM, TAM_TERM - 1)
    marco.move_to([0, Y_TERM, 0])
    orden = _filas((("git log", "cmd"),), Y_ORDEN)
    ficha = _filas(FICHA_LARGA, Y_SALIDA)
    ficha[0].set_color(RAMA_MAIN)
    siguiente = _filas(FICHA_SIGUIENTE, Y_SIGUIENTE, opacidades=DESVANECIDO)
    pager = _pager(marco)

    scene.play(FadeIn(marco), run_time=0.5)
    teclear(scene, VGroup(marco, orden), ritmo=0.3)
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.12) for f in ficha],
                    lag_ratio=0.3),
        run_time=1.1,
    )
    scene.play(
        LaggedStart(*[FadeIn(f) for f in siguiente], lag_ratio=0.3),
        run_time=0.8,
    )
    scene.play(FadeIn(pager, shift=UP * 0.12), run_time=0.5)
    scene.next_slide()

    def _orden(n):
        banderas = " ".join(bandera for bandera, _ in BANDERAS[:n])
        return _filas(((f"git log {banderas}".rstrip(), "cmd"),), Y_ORDEN)

    primera = _filas(((f"{HASH} {PEGATINA} {MENSAJE}", "out"),), Y_SALIDA,
                     x=X_LINEAS)
    scene.play(
        FadeOut(siguiente), FadeOut(pager),
        Transform(orden, _orden(1)), run_time=0.6,
    )
    scene.play(
        ReplacementTransform(ficha, primera),
        Flash(nodos[-1], color=RAMA_MAIN, line_length=0.18, num_lines=14,
              flash_radius=0.5),
        run_time=1.0,
    )

    lineas = VGroup(primera)
    for i, (corto, mensaje) in enumerate(reversed(COMMITS[:-1])):
        fila = _filas(((f"{corto} {mensaje}", "out"),),
                      Y_SALIDA - (i + 1) * PASO_FILA, x=X_LINEAS)
        lineas.add(fila)
        scene.play(
            FadeIn(fila, shift=RIGHT * 0.12),
            Flash(nodos[-2 - i], color=RAMA_MAIN, line_length=0.18,
                  num_lines=14, flash_radius=0.5),
            run_time=0.5,
        )
    prompt = _filas((("", "cmd"),), Y_SALIDA - len(COMMITS) * PASO_FILA)
    scene.play(FadeIn(prompt), FadeIn(_glosa(0), shift=RIGHT * 0.12),
               run_time=0.6)
    scene.next_slide()

    scene.play(
        Transform(orden, _orden(2)),
        *[fila.animate.shift(DOWN * (destino - i) * PASO_FILA)
          for i, (fila, destino) in enumerate(zip(lineas, FILAS_TRONCO))
          if destino != i],
        prompt.animate.shift(DOWN * N_FILAS_RAMA * PASO_FILA),
        run_time=0.8,
    )

    filas_rama, entradas, columnas = VGroup(), [], []
    for rama, color, i_padre, i_merge, commits in RAMAS:
        nodos_rama, filas, dibujo = VGroup(), VGroup(), VGroup()
        for j, (corto, mensaje, x, i_fila) in enumerate(commits):
            rotulo = f"{corto} {mensaje}"
            if j == 0:
                rotulo = f"{corto} ({rama}) {mensaje}"
            fila = _filas(((rotulo, "out"),), Y_SALIDA - i_fila * PASO_FILA,
                          x=X_LINEAS)
            filas.add(fila.set_color(color))
            nodos_rama.add(nodo_commit(corto, color, RADIO, TAM_HASH)
                           .move_to([x, Y_NODO_RAMA, 0]))
        filas_rama.add(*filas)
        columnas.append((filas, color, i_merge is not None))

        cadena_rama = [nodos[i_padre], *reversed(nodos_rama)]
        if i_merge is not None:
            cadena_rama.append(nodos[i_merge])
        for a, b in zip(cadena_rama, cadena_rama[1:]):
            dibujo.add(arista(a, b, color, RADIO))
        entradas.append(LaggedStart(
            *[Create(t) for t in dibujo],
            *[GrowFromCenter(n) for n in nodos_rama],
            *[FadeIn(f, shift=RIGHT * 0.12) for f in filas],
            lag_ratio=0.3,
        ))

    scene.play(LaggedStart(*entradas, lag_ratio=0.5), run_time=2.4)
    scene.play(FadeIn(_glosa(1), shift=RIGHT * 0.12), run_time=0.5)
    scene.next_slide()

    scene.play(Transform(orden, _orden(3)), run_time=0.5)
    scene.play(
        *[fila.animate.shift(RIGHT * SANGRIA_RAMA) for fila in filas_rama],
        run_time=0.5,
    )

    ys_tronco = [fila.get_y() for fila in lineas]
    filas_todas = sorted(
        [(y, True) for y in ys_tronco]
        + [(fila.get_y(), False) for fila in filas_rama],
        key=lambda par: -par[0],
    )
    tronco = VGroup(*[
        texto("*", TAM_TERM, color=RAMA_MAIN).move_to([X_TRONCO, y, 0])
        for y in ys_tronco
    ])
    for (y, propio), (y_sig, propio_sig) in zip(filas_todas, filas_todas[1:]):
        tronco.add(Line(
            [X_TRONCO, y - (HUECO_GRAFO if propio else 0), 0],
            [X_TRONCO, y_sig + (HUECO_GRAFO if propio_sig else 0), 0],
            color=RAMA_MAIN, stroke_width=2.5,
        ))

    grafo = VGroup()
    for filas, color, cerrada in columnas:
        ys = [fila.get_y() for fila in filas]
        columna = VGroup(*[
            texto("*", TAM_TERM, color=color).move_to([X_RAMA_COL, y, 0])
            for y in ys
        ])
        for y, y_sig in zip(ys, ys[1:]):
            columna.add(Line([X_RAMA_COL, y - HUECO_GRAFO, 0],
                             [X_RAMA_COL, y_sig + HUECO_GRAFO, 0],
                             color=color, stroke_width=2.5))
        columna.add(Line([X_RAMA_COL, ys[-1] - HUECO_GRAFO, 0],
                         [X_TRONCO, ys[-1] - PASO_FILA + HUECO_GRAFO, 0],
                         color=color, stroke_width=2.5))
        if cerrada:
            columna.add(Line([X_TRONCO, ys[0] + PASO_FILA - HUECO_GRAFO, 0],
                             [X_RAMA_COL, ys[0] + HUECO_GRAFO, 0],
                             color=color, stroke_width=2.5))
        grafo.add(columna)

    scene.play(FadeIn(tronco, shift=RIGHT * 0.1), run_time=0.7)
    scene.play(LaggedStart(*[FadeIn(c) for c in grafo], lag_ratio=0.35),
               run_time=1.1)
    scene.play(FadeIn(_glosa(2), shift=RIGHT * 0.12), run_time=0.5)
    scene.next_slide()
