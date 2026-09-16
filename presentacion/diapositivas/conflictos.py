"""Diapositiva 16 — conflictos: qué son y cómo se salen.

Un conflicto no es un error de git ni un castigo: es git diciendo "aquí no
puedo decidir por ti". Solo pasa cuando dos ramas tocaron **las mismas líneas
del mismo archivo**; si una tocó el principio y otra el final, git las junta
solo y ni te enteras.

Va con la misma pantalla que ``git_diff``, y por el mismo motivo: el archivo
abierto a la izquierda, la terminal a la derecha, las dos ventanas quietas toda
la diapositiva y el conflicto entero ocurriendo delante, paso a paso. Aquí eso
importa todavía más, porque lo que asusta de un conflicto es justo lo que no se
ve si se cuenta con viñetas: que git **te escribe dentro del archivo**.

El recorrido:

  * **el merge que falla**, que va despacio y en cuatro tiempos porque es el
    acto que hay que contar sin prisa: la función tal y como está en main con
    la terminal esperando; el ``switch`` y el ``merge`` —git lo intenta—; el
    ``CONFLICT`` —no puede—; y, solo entonces, los marcadores apareciendo
    dentro del archivo, con el ``return`` de antes descolgándose envuelto entre
    ellos. Ahí se ve de dónde salen: no los escribió nadie, los metió git.

  * **la salida de emergencia** — ``git merge --abort`` lo primero, antes de
    resolver nada. Saber que existe es lo que quita el miedo, y por eso va al
    principio y no al final: quien está perdido necesita saber que puede
    deshacerlo antes de escuchar cómo se arregla.

  * **``git status``** — el comando que contesta *qué* archivos están en
    conflicto. En un merge a medias dice algo que no dice nunca más:
    ``Unmerged paths``, y debajo ``both modified``.

  * **se edita como código normal** — y esta es la idea que hay que dejar
    clara: eso son líneas de texto en tu archivo. Se borran las que sobran y
    ya. No hay comando que resuelva un conflicto; lo resuelves tú, editando.

  * **``git add`` y commit** — ``git add`` es lo que le dice a git que ese
    archivo ya está, y el commit cierra el merge.

Sale detrás de ``merge``, que es donde se prometió que esto podía pasar.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    VGroup,
)

from animaciones import teclear
from componentes import ALTO_BARRA, linea_terminal, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import CLARO, ERROR

TITULO = "merge conflicts"

# --- El escenario ----------------------------------------------------------
# Las mismas dos ventanas de ``git_diff``, del mismo tamaño y en el mismo
# sitio: el archivo abierto y la terminal. No se mueven en toda la diapositiva.
TAM = 16
ANCHO_PANEL = 6.4
ALTO_PANEL = 5.1
MARGEN = 0.4              # aire entre el borde de la ventana y las filas
BUFF = 0.2                # aire entre filas
X_ARCHIVO, X_TERMINAL = -3.5, 3.5
Y_PANEL = -0.25           # deja libre la esquina del indicador de avance
NOMBRE = "media.py"
RAMA = "redondeo"

# --- El archivo ------------------------------------------------------------
# Una función de tres líneas: lo justo para que el conflicto quepa entero en
# pantalla y se lea de un vistazo. Las dos ramas tocaron el mismo ``return`` —
# una lo deja crudo y la otra lo redondea—, que es la única forma de que haya
# conflicto: las mismas líneas del mismo archivo.
CONFLICTO = (
    ("def media(datos):", "txt"),
    ("    m = sum(datos) / len(datos)", "txt"),
    ("<<<<<<< HEAD", "ok"),
    ("    return m", "ok"),
    ("=======", "out"),
    ("    return round(m, 2)", "alt"),
    (f">>>>>>> {RAMA}", "alt"),
)
SANGRIA_CONFLICTO = {1: 4, 3: 4, 5: 4}
ANTES = ("    return m", 4)   # el return de main, antes de que git lo envuelva
FILA_ANTES = 2                # el renglón donde está antes del merge
MARCAS = (2, 3, 4, 5, 6)      # lo que git mete en el archivo al fallar

# Al resolver se borra todo menos una versión. Se queda la de la rama, que es
# la que traía el redondeo: resolver no es "ganar", es elegir.
FUERA = (2, 3, 4, 6)
QUEDA = 5
SLOT_QUEDA = 2

# --- La terminal -----------------------------------------------------------
PROMPT = (("", "cmd"),)   # la terminal esperando, antes de pedir nada

# El merge que falla y, seguida, la salida de emergencia: van en la misma
# sesión porque en una terminal de verdad también irían seguidas. Y se teclea
# por tramos, con una pausa entre cada uno, porque este es el acto que hay que
# contar despacio: git lo intenta, no puede, y entra en tu archivo.
MERGE = (
    ("git switch main", "cmd"),
    ("", "sep"),
    (f"git merge {RAMA}", "cmd"),
    (f"Auto-merging {NOMBRE}", "out"),
    (f"CONFLICT: Merge conflict in {NOMBRE}", "err"),
    ("Automatic merge failed", "err"),
    ("", "sep"),
    ("git merge --abort", "cmd"),
)
TRAMOS_MERGE = ((0, 4), (4, 6), (6, 8))
FILA_ABORTA = 7

# Lo único que git dice distinto cuando hay un merge a medias.
STATUS = (
    ("git status", "cmd"),
    ("On branch main", "out"),
    ("You have unmerged paths.", "out"),
    ("", "sep"),
    ("Unmerged paths:", "out"),
    (f"  both modified:   {NOMBRE}", "err"),
)
SANGRIA_STATUS = {5: 2}
FILA_UNMERGED = 5

RESUELTO = (
    (f"git add {NOMBRE}", "cmd"),
    ("", "sep"),
    ("git commit", "cmd"),
    (f"[main 8f3a1c] Merge branch '{RAMA}'", "out"),
)
TRAMOS_RESUELTO = ((0, 2), (2, 4))


def _panel(lineas, x, nombre=None):
    """Una ventana del tamaño del panel con sus filas colgando de arriba.

    Igual que en ``git_diff``: el tamaño es fijo en todas las pantallas para
    que las dos ventanas no se muevan nunca, y las filas se anclan arriba
    porque una sesión de terminal —y un archivo— crecen hacia abajo.
    """
    chrome = ventana(ANCHO_PANEL, ALTO_PANEL, nombre, TAM - 2)
    chrome.move_to([x, Y_PANEL, 0])
    filas = VGroup(*[linea_terminal(c, t, TAM) for c, t in lineas])
    if len(filas):
        filas.arrange(DOWN, buff=BUFF, aligned_edge=LEFT)
        filas.move_to(chrome[0].get_top() + DOWN * (ALTO_BARRA + MARGEN), UP)
        filas.align_to(chrome[0].get_left() + RIGHT * MARGEN, LEFT)
    return VGroup(chrome, filas)


def _paso():
    """Lo que ocupa un carácter, para poder sangrar moviendo.

    Un ``Text`` no dibuja los espacios de la izquierda —su caja empieza en el
    primer glifo—, así que la sangría de la función no se puede escribir: hay
    que correrla. Como la fuente es mono, un carácter mide siempre lo mismo.
    """
    return texto("mm", TAM).width - texto("m", TAM).width


def _sangrar(panel, sangrias):
    """Mete la sangría que Pango se come, fila por fila."""
    paso = _paso()
    for fila, espacios in sangrias.items():
        panel[1][fila].shift(RIGHT * espacios * paso)


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    archivo = _panel(CONFLICTO, X_ARCHIVO, NOMBRE)
    _sangrar(archivo, SANGRIA_CONFLICTO)
    prompt = _panel(PROMPT, X_TERMINAL)
    consola = _panel(MERGE, X_TERMINAL)
    marco_archivo, marco_consola = archivo[0], prompt[0]

    # El ``return`` que hay en main ocupa el renglón donde git va a escribir el
    # ``<<<<<<<``: cuando salte el conflicto, se apaga y el de verdad aparece
    # un renglón más abajo, envuelto. Esa caída es toda la explicación.
    contenido, sangria = ANTES
    antes = linea_terminal(contenido, "txt", TAM)
    antes.move_to(archivo[1][FILA_ANTES], LEFT).shift(RIGHT * sangria * _paso())
    marcas = VGroup(*[archivo[1][i] for i in MARCAS])

    # ---------------------- La función, sin tocar --------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(marco_archivo), FadeIn(marco_consola), run_time=0.6)
    teclear(scene, archivo, 0, FILA_ANTES, ritmo=0.26)
    scene.play(FadeIn(antes, shift=RIGHT * 0.12),
               FadeIn(prompt[1][0]), run_time=0.35)
    scene.next_slide()

    # ---------------------- git lo intenta ---------------------------------
    # El ``switch`` primero, que es el paso que todo el mundo se salta: se
    # mezcla hacia la rama en la que estás.
    scene.play(FadeOut(prompt[1]), run_time=0.25)
    teclear(scene, consola, *TRAMOS_MERGE[0], ritmo=0.3)
    scene.next_slide()

    # ---------------------- y no puede -------------------------------------
    teclear(scene, consola, *TRAMOS_MERGE[1], ritmo=0.3)
    scene.next_slide()

    # ---------------------- lo que le hizo a tu archivo --------------------
    # El momento de la diapositiva: los marcadores no los escribió nadie, los
    # metió git, y el ``return`` de antes se descuelga envuelto entre ellos.
    scene.play(FadeOut(antes, shift=LEFT * 0.15), run_time=0.3)
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.12) for f in marcas],
                    lag_ratio=0.3),
        run_time=1.2,
    )
    scene.next_slide()

    # ---------------------- La salida de emergencia ------------------------
    # Antes de resolver nada: se puede deshacer entero.
    teclear(scene, consola, *TRAMOS_MERGE[2], ritmo=0.32)
    scene.play(Indicate(consola[1][FILA_ABORTA], color=ERROR,
                        scale_factor=1.08), run_time=0.8)
    scene.next_slide()

    # ---------------------- git status -------------------------------------
    status = _panel(STATUS, X_TERMINAL)
    _sangrar(status, SANGRIA_STATUS)
    scene.play(FadeOut(consola[1]), run_time=0.25)
    consola = status
    teclear(scene, consola, ritmo=0.3)
    scene.play(Indicate(consola[1][FILA_UNMERGED], color=ERROR,
                        scale_factor=1.06), run_time=0.8)
    scene.next_slide()

    # ---------------------- Se edita como código normal --------------------
    # No hay comando que resuelva esto: son renglones de texto en tu archivo.
    # Se borran los que sobran y el que queda sube a su sitio, ya sin color de
    # rama, porque a partir de ahora es código tuyo y punto.
    filas = archivo[1]
    alturas = [f.get_y() for f in filas]
    scene.play(
        *[FadeOut(filas[i], shift=LEFT * 0.2) for i in FUERA],
        filas[QUEDA].animate
        .shift(UP * (alturas[SLOT_QUEDA] - alturas[QUEDA]))
        .set_color(CLARO),
        run_time=1.1,
    )
    scene.next_slide()

    # ---------------------- git add y commit -------------------------------
    resuelto = _panel(RESUELTO, X_TERMINAL)
    scene.play(FadeOut(consola[1]), run_time=0.25)
    consola = resuelto
    teclear(scene, consola, *TRAMOS_RESUELTO[0], ritmo=0.3)
    teclear(scene, consola, *TRAMOS_RESUELTO[1], ritmo=0.3)
    scene.wait(0.3)
    scene.next_slide()
