"""Diapositiva 22a — ``git remote``: enlazar el repo local con el de GitHub.

Primer comando del tramo remoto, y el único que se teclea una sola vez en la
vida de un repositorio. Hasta aquí todo ha pasado dentro de la carpeta; esta
diapositiva es la que ata esa carpeta a una dirección de internet.

Va en dos tiempos:

  * **la idea** — y es lo único que hay que entender: *origin no es una palabra
    mágica de git, es un apodo*. El nombre corto que le pones a una dirección
    larguísima para no volver a escribirla nunca más. Podría llamarse ``pepe``;
    se llama ``origin`` porque es la convención, igual que la rama principal se
    llama ``main``. Por eso debajo del ``remote add`` va un ``remote -v``: es
    la libreta de apodos, con el nombre a la izquierda y la dirección a la
    derecha, y de paso se ve que hay dos renglones —uno para bajar y otro para
    subir— que en la práctica son el mismo.

  * **de dónde sale esa dirección** — la página que GitHub enseña nada más
    crear un repositorio vacío, con sus dos bloques de comandos. Es la pantalla
    que van a tener delante de verdad el día que lo hagan, así que sale tal
    cual, en su ventana de navegador y en inglés: lo que importa es que la
    reconozcan.

    Y las dos opciones no se cuentan, se ven. Primero sale la de arriba, la de
    empezar de cero, con sus siete comandos. Y para la segunda no se cambia de
    pantalla: se caen los cuatro primeros —``echo``, ``init``, ``add``,
    ``commit``— y quedan los tres de abajo. Ahí está todo dicho: la segunda
    opción es el final de la primera, y te la saltas entera porque esos cuatro
    comandos ya los hiciste el primer día. Los tres que siempre quedan son
    ``remote add``, ``branch -M main`` y ``push -u``.

  * **y al revés** — el acto de cierre, porque las dos opciones de arriba dan
    por hecho que el repositorio ya estaba en tu máquina. Cuando el que existe
    es el de GitHub no se hace nada de eso: ``git clone`` se lo trae entero. Y
    el remate se ve sin escribirlo, porque el ``git remote -v`` que sale
    después es exactamente el mismo de la primera pantalla: nadie ha tecleado
    un ``remote add`` y ``origin`` ya está puesto. Clonar te da el apodo hecho.

Sale detrás de ``local_remoto``, que es donde apareció GitHub por primera vez,
y delante de ``git_push``, que despieza el ``-u``.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    Transform,
    VGroup,
)

from animaciones import flecha, teclear
from componentes import ALTO_BARRA, imagen_circular, linea_terminal
from componentes import puntero, terminal, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import OK, SECUNDARIO

TITULO = "git remote"

USUARIO = "aperture"
REPO = "aperture_repo"
URL = f"https://github.com/{USUARIO}/{REPO}.git"

# --- Pantalla 1: origin es un apodo ----------------------------------------
SESION = (
    (f"git remote add origin {URL}", "cmd"),
    ("", "sep"),
    ("git remote -v", "cmd"),
    (f"origin  {URL} (fetch)", "out"),
    (f"origin  {URL} (push)", "out"),
)
TAM_SESION = 15
Y_SESION = 0.35

# El apodo y lo que hay detrás, que es toda la idea de la diapositiva.
APODO = "origin"
TAM_APODO = 21
TAM_DIRECCION = 17
SEPARACION_APODO = 1.15           # hueco para la flecha entre los dos
Y_APODO = -2.45

# --- Pantallas 2 y 3: la página que enseña GitHub --------------------------
# Tal y como sale al crear un repositorio vacío. La ventana es de tamaño fijo
# porque las dos opciones se cuentan sin cambiar de pantalla: la segunda es la
# primera con los cuatro primeros comandos caídos.
NAVEGADOR = f"github.com/{USUARIO}/{REPO}"
TAM_WEB = 16
ANCHO_WEB = 11.0
ALTO_WEB = 4.6
MARGEN_WEB = 0.42
BUFF_WEB = 0.2
# La ventana se corre a la derecha para dejarle sitio al logo, que va al
# lado y no encima: lo que se mira es la página, el logo solo dice de quién es.
X_WEB, Y_WEB = 0.9, 0.1
DIAMETRO_LOGO = 1.5
OCUPACION_LOGO = 0.7
X_LOGO = -5.8

NUEVO = (
    ("…or create a new repository on the command line", "out"),
    (f'echo "# {REPO}" >> README.md', "txt"),
    ("git init", "txt"),
    ("git add README.md", "txt"),
    ('git commit -m "first commit"', "txt"),
    ("git branch -M main", "txt"),
    (f"git remote add origin {URL}", "txt"),
    ("git push -u origin main", "txt"),
)
EXISTENTE = "…or push an existing repository from the command line"
SOBRAN = (1, 2, 3, 4)             # lo que ya hiciste el primer día
QUEDAN = (5, 6, 7)                # los tres que quedan siempre

# --- Pantalla 4: y al revés ------------------------------------------------
# Las dos opciones de GitHub son para un repo que ya tenías en tu máquina. Si
# el repositorio ya existe arriba, no se hace nada de eso: se clona. Y el
# ``remote -v`` de abajo es el mismo de la primera pantalla, con la diferencia
# de que aquí nadie ha escrito un ``remote add``.
TITULO_CLONE = "git clone"
CLONAR = (
    (f"git clone {URL}", "cmd"),
    (f"Cloning into '{REPO}'...", "out"),
    ("", "sep"),
    (f"cd {REPO}", "cmd"),
    ("git remote -v", "cmd"),
    (f"origin  {URL} (fetch)", "out"),
    (f"origin  {URL} (push)", "out"),
)
TRAMOS_CLONE = ((0, 3), (3, 7))


def _pagina(lineas, nombre=None):
    """La ventana del navegador, de tamaño fijo y con las filas desde arriba.

    Igual que los paneles de ``git_diff`` y ``conflictos``: el marco no cambia
    entre pantallas, solo lo que hay dentro, para que las dos opciones se
    puedan comparar sin que se mueva nada.
    """
    chrome = ventana(ANCHO_WEB, ALTO_WEB, nombre, TAM_WEB - 2)
    chrome.move_to([X_WEB, Y_WEB, 0])
    filas = VGroup(*[linea_terminal(c, t, TAM_WEB) for c, t in lineas])
    filas.arrange(DOWN, buff=BUFF_WEB, aligned_edge=LEFT)
    filas.move_to(chrome[0].get_top() + DOWN * (ALTO_BARRA + MARGEN_WEB), UP)
    filas.align_to(chrome[0].get_left() + RIGHT * MARGEN_WEB, LEFT)
    return VGroup(chrome, filas)


def construir(scene):
    # ---------------------- origin es un apodo -----------------------------
    encabezado = hacer_titulo(TITULO)
    consola = terminal(SESION, tam=TAM_SESION).move_to([0, Y_SESION, 0])

    # El apodo a la izquierda, la dirección a la derecha y la flecha entre
    # medias: se monta pegado y se centra después, ya como un bloque.
    etiqueta = puntero(APODO, OK, TAM_APODO)
    direccion = texto(URL, TAM_DIRECCION, color=SECUNDARIO)
    direccion.next_to(etiqueta, RIGHT, buff=SEPARACION_APODO)
    puente = flecha(
        etiqueta.get_right() + RIGHT * 0.1,
        direccion.get_left() + LEFT * 0.1,
        OK, buff=0.04,
    )
    apodo = VGroup(etiqueta, puente, direccion).move_to([0, Y_APODO, 0])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(consola[0]), run_time=0.5)
    teclear(scene, consola, ritmo=0.32)
    scene.play(FadeIn(etiqueta, shift=RIGHT * 0.12), run_time=0.5)
    scene.play(FadeIn(puente), FadeIn(direccion, shift=RIGHT * 0.12),
               run_time=0.6)
    scene.next_slide()

    # ---------------------- La página de GitHub ----------------------------
    # Lo que ves nada más crear el repositorio: de ahí sale esa dirección.
    pagina = _pagina(NUEVO, NAVEGADOR)
    logo = imagen_circular("github.jpg", diametro=DIAMETRO_LOGO,
                           ocupacion=OCUPACION_LOGO)
    logo.move_to([X_LOGO, Y_WEB, 0])
    scene.play(
        FadeOut(consola), FadeOut(apodo), run_time=0.6,
    )
    scene.play(FadeIn(logo, shift=RIGHT * 0.15), FadeIn(pagina[0]),
               run_time=0.6)
    teclear(scene, pagina, ritmo=0.26)
    scene.next_slide()

    # ---------------------- La otra opción ---------------------------------
    # No se cambia de pantalla: se caen los cuatro que ya hiciste el primer
    # día y quedan los tres de siempre. Eso es la segunda opción.
    filas = pagina[1]
    alturas = [f.get_y() for f in filas]
    otro = linea_terminal(EXISTENTE, "out", TAM_WEB).move_to(filas[0], LEFT)
    scene.play(
        Transform(filas[0], otro),
        *[FadeOut(filas[i], shift=LEFT * 0.2) for i in SOBRAN],
        *[filas[q].animate.shift(UP * (alturas[d] - alturas[q]))
          for d, q in enumerate(QUEDAN, start=1)],
        run_time=1.2,
    )
    scene.next_slide()

    # ---------------------- Y al revés: git clone --------------------------
    # Todo lo anterior es para un repo que ya tenías en tu máquina. Cuando el
    # que existe es el de arriba, no se hace nada de eso: se clona y ya.
    otro_encabezado = hacer_titulo(TITULO_CLONE)
    clonar = _pagina(CLONAR)
    # De la página solo se apaga lo que quedó vivo: las filas que ya se fueron
    # no se vuelven a tocar, o reaparecerían de golpe para irse otra vez.
    vivas = VGroup(filas[0], *[filas[q] for q in QUEDAN])

    scene.play(
        FadeOut(pagina[0]), FadeOut(vivas),
        FadeOut(encabezado), FadeIn(otro_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(clonar[0]), run_time=0.5)
    teclear(scene, clonar, *TRAMOS_CLONE[0], ritmo=0.3)
    scene.next_slide()

    # Y el remate: nadie ha escrito un remote add y origin ya está puesto. El
    # apodo no lo pones tú cuando clonas, viene de fábrica.
    teclear(scene, clonar, *TRAMOS_CLONE[1], ritmo=0.3)
    scene.wait(0.3)
    scene.next_slide()
