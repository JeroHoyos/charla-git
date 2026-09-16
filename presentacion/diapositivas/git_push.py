"""Diapositiva 22b — ``git push``: subir lo que ya está confirmado.

El remoto ya está enlazado; esto es el viaje de ida, y se cuenta enseñándolo:
a la izquierda la terminal donde se va tecleando y a la derecha el dibujo —el
logo de GitHub con lo que ha llegado arriba, y tu rama abajo—. Nada de listas
de banderas: la línea larga se teclea **una vez** y a partir de ahí se ve
encogerse sola, que es exactamente lo que pasa en la vida real y lo único que
hay que recordar del ``-u``.

El recorrido son cinco tiempos, y los tres últimos son el mismo gesto repetido
a propósito, cada vez más corto y más rápido, para que quede como rutina:

  * **la foto de salida** — tres commits en tu máquina y GitHub sin nada. Un
    repositorio recién creado no tiene nada hasta que alguien sube.

  * **``git push -u origin main``** — la primera y única vez que se escribe
    entera. Los tres commits **suben sin irse**: aparecen arriba y siguen
    abajo, porque nada se mueve, todo se copia.

  * **``git commit``** — un commit nuevo abajo. Arriba se queda como estaba, y
    esa diferencia entre las dos filas es la razón de que haya que volver a
    subir.

  * **``git push``**, a secas — sube el nuevo. Aquí está el ``-u``: ya no hace
    falta decirle a dónde ni qué rama, porque se lo dijiste la primera vez.

  * **otra vez, y ya sin pensar** — ``commit`` y ``push`` seguidos, rápido. El
    día a día es este renglón y no el de arriba.

Y lo que se ve sin escribirlo: solo viajan los nodos. Lo que no has confirmado
no está en la fila de abajo, así que no puede subir.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    RoundedRectangle,
    TransformFromCopy,
    VGroup,
)

from animaciones import teclear
from componentes import ALTO_BARRA, arista, imagen_circular, linea_terminal
from componentes import nodo_commit, puntero, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import FONDO, OK, RAMA_MAIN, SECUNDARIO, SUPERFICIE

TITULO = "git push"

# --- Izquierda: la terminal ------------------------------------------------
TAM = 16
ANCHO_PANEL = 6.4
ALTO_PANEL = 5.1
MARGEN = 0.4              # aire entre el borde de la ventana y las filas
BUFF = 0.2                # aire entre filas
X_PANEL, Y_PANEL = -3.5, -0.25

PROMPT = (("", "cmd"),)
SESION = (
    ("git push -u origin main", "cmd"),
    ("", "sep"),
    ("git commit", "cmd"),
    ("git push", "cmd"),
    ("", "sep"),
    ("git commit", "cmd"),
    ("git push", "cmd"),
)
# Un tramo por tiempo: la orden larga, el commit, el push corto, y la rutina.
TRAMOS = ((0, 1), (1, 3), (3, 4), (4, 7))

# --- Derecha: el dibujo ----------------------------------------------------
# Un solo carril de x para las dos filas: cada commit sube en vertical, justo
# encima de sí mismo, y así el viaje se lee sin flechas que lo expliquen.
X_NODOS = (2.5, 3.4, 4.3, 5.2, 6.1)
RADIO = 0.28
TAM_HASH = 13
HASHES = ("0e5f", "77ab", "c4f0", "a3c1", "b8e2")
INICIALES = 3             # los que ya hay confirmados antes del primer push

Y_REMOTO = 1.55           # arriba: lo que ya está en GitHub
Y_LOCAL = -1.55           # abajo: tu máquina
# Los dos rótulos, uno por fila y en la misma columna: arriba el sitio de
# internet, abajo el tuyo. Sin ellos las dos filas se parecen demasiado.
X_ROTULO = 1.15
DIAMETRO_LOGO = 1.2
OCUPACION_LOGO = 0.7
ALTO_PORTATIL = 0.72
TAM_ROTULO = 16
TAM_PUNTERO = 14
BUFF_PUNTERO = 0.3


def _panel(lineas):
    """La ventana de la terminal, de tamaño fijo y con las filas desde arriba."""
    chrome = ventana(ANCHO_PANEL, ALTO_PANEL, None, TAM - 2)
    chrome.move_to([X_PANEL, Y_PANEL, 0])
    filas = VGroup(*[linea_terminal(c, t, TAM) for c, t in lineas])
    filas.arrange(DOWN, buff=BUFF, aligned_edge=LEFT)
    filas.move_to(chrome[0].get_top() + DOWN * (ALTO_BARRA + MARGEN), UP)
    filas.align_to(chrome[0].get_left() + RIGHT * MARGEN, LEFT)
    return VGroup(chrome, filas)


def _portatil(alto, color):
    """Un portátil de dibujo: la pantalla y la peana, y el rótulo debajo.

    Hace de pareja del logo de GitHub, en la misma columna y con la misma
    pinta de sello: arriba el sitio de internet, abajo tu máquina. Todas las
    medidas salen de ``alto``, así que se escala con un solo número.
    """
    ancho = alto * 1.4
    carcasa = RoundedRectangle(
        width=ancho, height=alto, corner_radius=alto * 0.1,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    # El marco por dentro: sin él la carcasa se lee como una caja cualquiera,
    # y con él se lee como una pantalla apagada.
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


def _fila(y, color):
    """Una fila de commits con sus aristas, en el carril de las x."""
    nodos = VGroup(*[
        nodo_commit(h, color, RADIO, TAM_HASH).move_to([x, y, 0])
        for x, h in zip(X_NODOS, HASHES)
    ])
    enlaces = VGroup(*[
        arista(nodos[i], nodos[i + 1], color, RADIO)
        for i in range(len(nodos) - 1)
    ])
    return nodos, enlaces


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    logo = imagen_circular("github.jpg", diametro=DIAMETRO_LOGO,
                           ocupacion=OCUPACION_LOGO)
    logo.move_to([X_ROTULO, Y_REMOTO, 0])
    maquina = _portatil(ALTO_PORTATIL, SECUNDARIO)
    maquina.move_to([X_ROTULO, Y_LOCAL, 0])
    arriba, enlaces_arriba = _fila(Y_REMOTO, OK)
    abajo, enlaces_abajo = _fila(Y_LOCAL, RAMA_MAIN)
    p_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    p_main.next_to(abajo[INICIALES - 1], DOWN, buff=BUFF_PUNTERO)

    prompt = _panel(PROMPT)
    consola = _panel(SESION)

    # ---------------------- La foto de salida ------------------------------
    # Tres commits tuyos y arriba nada: en GitHub todavía no hay nada.
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(logo), FadeIn(maquina), FadeIn(prompt[0]), run_time=0.6)
    scene.play(
        *[GrowFromCenter(abajo[i]) for i in range(INICIALES)],
        run_time=0.8,
    )
    scene.play(
        *[Create(enlaces_abajo[i]) for i in range(INICIALES - 1)],
        FadeIn(p_main, shift=UP * 0.1), run_time=0.6,
    )
    scene.play(FadeIn(prompt[1][0]), run_time=0.3)
    scene.next_slide()

    # ---------------------- La vez que se escribe entera -------------------
    # Suben sin irse: aparecen arriba y siguen abajo. Nada se mueve, se copia.
    scene.play(FadeOut(prompt[1]), run_time=0.25)
    teclear(scene, consola, *TRAMOS[0], ritmo=0.35)
    scene.play(
        *[TransformFromCopy(abajo[i], arriba[i]) for i in range(INICIALES)],
        run_time=1.2,
    )
    scene.play(
        *[Create(enlaces_arriba[i]) for i in range(INICIALES - 1)],
        run_time=0.5,
    )
    scene.next_slide()

    # ---------------------- Un commit más ----------------------------------
    # Arriba se queda como estaba, y esa diferencia es lo que pide otro push.
    nuevo = INICIALES
    teclear(scene, consola, *TRAMOS[1], ritmo=0.32)
    scene.play(
        GrowFromCenter(abajo[nuevo]),
        Create(enlaces_abajo[nuevo - 1]),
        p_main.animate.next_to(abajo[nuevo], DOWN, buff=BUFF_PUNTERO),
        run_time=0.8,
    )
    scene.next_slide()

    # ---------------------- Y ya solo git push -----------------------------
    # Aquí está el -u: ni a dónde ni qué rama, porque se lo dijiste una vez.
    teclear(scene, consola, *TRAMOS[2], ritmo=0.32)
    scene.play(TransformFromCopy(abajo[nuevo], arriba[nuevo]), run_time=1.0)
    scene.play(Create(enlaces_arriba[nuevo - 1]), run_time=0.4)
    scene.next_slide()

    # ---------------------- Otra vez, y ya sin pensar ----------------------
    ultimo = nuevo + 1
    teclear(scene, consola, *TRAMOS[3], ritmo=0.26)
    scene.play(
        GrowFromCenter(abajo[ultimo]),
        Create(enlaces_abajo[ultimo - 1]),
        p_main.animate.next_to(abajo[ultimo], DOWN, buff=BUFF_PUNTERO),
        run_time=0.6,
    )
    scene.play(TransformFromCopy(abajo[ultimo], arriba[ultimo]), run_time=0.8)
    scene.play(Create(enlaces_arriba[ultimo - 1]), run_time=0.35)
    scene.wait(0.3)
    scene.next_slide()
