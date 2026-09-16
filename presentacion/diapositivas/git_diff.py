"""Diapositiva 17 — ``git diff``: qué cambió.

La lupa. No cambia nada, así que se puede teclear sin miedo, y su lío viene
otra vez de las tres zonas: siempre mide el hueco **entre dos sitios**, y saber
cuáles son es todo el truco.

Esta no se explica, se hace. La pantalla es la de cualquiera que esté
trabajando —el archivo abierto a la izquierda, la terminal a la derecha— y las
dos ventanas no se mueven ni cambian de tamaño en toda la diapositiva: lo único
que pasa es que se edita el README y se van tecleando comandos, como en una
demostración en vivo. Por eso aquí casi no hay texto: lo que hay que leer está
dentro de las dos ventanas, y lo demás lo pone quien presenta.

El recorrido, paso a paso:

  * **el README que está en el commit** — el archivo, solo, sin tocar, y la
    terminal esperando.

  * **se edita y se pregunta** — se escribe el lema del semillero encima del
    que había y ``git diff`` contesta con un renglón rojo y tres verdes. El
    archivo está al lado: se ve de dónde sale cada uno.

  * **``git add`` y el silencio** — los renglones nuevos se ponen en ámbar (el
    color del staging en toda la charla), se vuelve a lanzar ``git diff`` y no
    contesta nada. No hace falta escribir que no imprime: el hueco entre un
    prompt y el siguiente es la respuesta. Ahí se corta, porque ese susto es la
    mitad de la diapositiva.

  * **``--cached``** — el que sí contesta, porque compara el otro par de
    sitios: el staging contra el último commit.

  * **``-w``** — en dos tiempos, que es lo que lo hace evidente: primero la
    lista de retos escrita a ras, tal y como está en el commit; y después se
    tabula entera y se le cambia el día a una. ``git diff`` saca seis
    renglones, sin distinguir el retoque que no cambia ni una letra del que sí.
    Entonces el comando se convierte en ``git diff -w`` y los cuatro que solo
    cambiaron en espacios se caen de la pantalla: queda el cambio de verdad,
    que era uno.

  * **entre dos commits** — que los dos sitios no tienen por qué ser zonas. A
    la izquierda el README tal y como era en ``3a1f2c4`` y a la derecha el
    hueco entre ese commit y el siguiente.

Sale justo detrás de ``git_ignore`` y antes de la tanda de deshacer
(``reset``, ``checkout``, ``revert``): es la última de las que solo miran, y la
que conviene tener en la mano antes de tocar nada.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    LaggedStart,
    Transform,
    VGroup,
)

from animaciones import teclear
from componentes import ALTO_BARRA, linea_terminal, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import SECUNDARIO, STAGING

TITULO = "git diff"

# --- El escenario ----------------------------------------------------------
# Dos ventanas del mismo tamaño que no se mueven en toda la diapositiva: la de
# la izquierda es el archivo abierto y la de la derecha la terminal. Lo único
# que cambia es lo que hay dentro, que es justo lo que pasa en una pantalla de
# verdad mientras alguien trabaja.
TAM = 16
ANCHO_PANEL = 6.4
ALTO_PANEL = 5.1
MARGEN = 0.4              # aire entre el borde de la ventana y las filas
BUFF = 0.2                # aire entre filas
X_ARCHIVO, X_TERMINAL = -3.5, 3.5
Y_PANEL = -0.25           # deja libre la esquina del indicador de avance
NOMBRE = "README.md"

# --- El archivo ------------------------------------------------------------
# El lema que está en el commit, y el de verdad, que se escribe encima. El de
# verdad va partido en tres renglones porque así cabe en el panel, y porque un
# README se escribe así: markdown junta en un solo párrafo los renglones
# seguidos, de modo que el archivo dice exactamente lo mismo.
LEMA_VIEJO = "*Aprendemos IA juntos.*"
README = (
    ("# Aperture", "txt"),
    ("", "sep"),
    ("### Semillero de Data Science e IA", "txt"),
    ("", "sep"),
    ("*No solo estudiamos la IA.", "txt"),
    ("La construimos y la llevamos", "txt"),
    ("a la realidad.*", "txt"),
)
FILAS_LEMA = (4, 5, 6)    # las tres que se escriben encima del lema viejo

# Más abajo en el mismo archivo: la lista de la pantalla de ``-w``, tal y como
# está en el commit —a ras, sin tabular— porque ahí se escribe delante de todo
# el mundo lo que se le hace después.
LISTA = (
    ("## Retos", "txt"),
    ("", "sep"),
    ("* Retos semanales", "txt"),
    ("* Sesiones los viernes", "txt"),
    ("* Proyecto final", "txt"),
)
FILAS_LISTA = (2, 3, 4)   # las tres que se tabulan
FILA_DIA = 3              # y la que además cambia de día
DIA_NUEVO = "* Sesiones los jueves"
SANGRIA = 2               # los espacios que se le meten delante al tabular

# Y el archivo tal y como era en el primer commit, para la última pantalla.
COMMITEADO = (
    ("# Aperture", "txt"),
    ("", "sep"),
    ("### Semillero de Data Science e IA", "txt"),
    ("", "sep"),
    (LEMA_VIEJO, "txt"),
)
VIEJO = "3a1f2c4"
NOMBRE_VIEJO = f"{NOMBRE} @ {VIEJO}"

# --- La terminal -----------------------------------------------------------
PROMPT = (("", "cmd"),)   # la terminal esperando, antes de tocar nada

DIFF = (
    ("git diff", "cmd"),
    ("@@ -5 +5,3 @@", "avi"),
    ("- *Aprendemos IA juntos.*", "err"),
    ("+ *No solo estudiamos la IA.", "ok"),
    ("+ La construimos y la llevamos", "ok"),
    ("+ a la realidad.*", "ok"),
)

# El add, el diff que no contesta y el --cached. Que no conteste no se escribe
# en ningún lado: se ve, porque entre ese prompt y el siguiente no hay nada.
STAGED = (
    ("git add README.md", "cmd"),
    ("", "sep"),
    ("git diff", "cmd"),
    ("", "sep"),
    ("git diff --cached", "cmd"),
    ("- *Aprendemos IA juntos.*", "err"),
    ("+ *No solo estudiamos la IA.", "ok"),
    ("+ La construimos y la llevamos", "ok"),
    ("+ a la realidad.*", "ok"),
)
TRAMOS_STAGED = ((0, 2), (2, 4), (4, 9))

# Tabular la lista y, de paso, cambiar un día: para git son seis renglones.
ESPACIOS = (
    ("git diff", "cmd"),
    ("@@ -7,3 +7,3 @@", "avi"),
    ("- * Retos semanales", "err"),
    ("- * Sesiones los viernes", "err"),
    ("- * Proyecto final", "err"),
    ("+   * Retos semanales", "ok"),
    ("+   * Sesiones los jueves", "ok"),
    ("+   * Proyecto final", "ok"),
)
RUIDO = (2, 4, 5, 7)      # las que solo cambiaron en espacios: las tacha -w
QUEDAN = (3, 6)           # el cambio de verdad, que era uno
CON_W = "git diff -w"

ENTRE_COMMITS = (
    ("git log --oneline", "cmd"),
    ("9c1d0e5 docs: el lema", "out"),
    ("3a1f2c4 docs: primer README", "out"),
    ("", "sep"),
    ("git diff 3a1f2c4 9c1d0e5", "cmd"),
    ("- *Aprendemos IA juntos.*", "err"),
    ("+ *No solo estudiamos la IA.", "ok"),
    ("+ La construimos y la llevamos", "ok"),
    ("+ a la realidad.*", "ok"),
)
TRAMOS_COMMITS = ((0, 4), (4, 9))


def _panel(lineas, x, nombre=None):
    """Una ventana del tamaño del panel con sus filas colgando de arriba.

    El tamaño es fijo —el mismo en las seis pantallas— para que las dos
    ventanas no se muevan nunca: lo único que cambia en toda la diapositiva es
    lo que hay dentro. Y las filas se anclan arriba, no centradas como hace
    ``componentes.terminal``, porque una sesión de terminal crece hacia abajo
    desde la primera línea.
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
    """Lo que ocupa un carácter, para poder tabular moviendo.

    Un ``Text`` no dibuja los espacios de la izquierda —su caja empieza en el
    primer glifo—, así que la sangría de la lista no se puede escribir: hay que
    correrla. Como la fuente es mono, un carácter mide siempre lo mismo y
    tabular es mover la fila tantos anchos como espacios se le metan.
    """
    return texto("mm", TAM).width - texto("m", TAM).width


def construir(scene):
    # Los dos marcos se ponen una vez y ya no se tocan: cada pantalla cambia
    # solo las filas de dentro, que es lo que hace que esto se lea como una
    # pantalla de verdad y no como cuatro diapositivas seguidas.
    encabezado = hacer_titulo(TITULO)
    readme = _panel(README, X_ARCHIVO, NOMBRE)
    prompt = _panel(PROMPT, X_TERMINAL)
    marco_archivo, marco_consola = readme[0], prompt[0]

    # El lema viejo se pone justo en el renglón del primero de los nuevos: al
    # editar, ese se cambia en el sitio y los otros dos le salen debajo, que es
    # como se ve un párrafo creciendo en un editor de verdad.
    nuevas = VGroup(*[readme[1][i] for i in FILAS_LEMA])
    viejo = linea_terminal(LEMA_VIEJO, "txt", TAM)
    viejo.move_to(readme[1][FILAS_LEMA[0]]).align_to(readme[1][0], LEFT)

    # ---------------------- El README que está en el commit ----------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(marco_archivo), FadeIn(marco_consola), run_time=0.6)
    teclear(scene, readme, 0, FILAS_LEMA[0], ritmo=0.26)
    scene.play(FadeIn(viejo, shift=RIGHT * 0.12),
               FadeIn(prompt[1][0]), run_time=0.35)
    scene.next_slide()

    # ---------------------- Se edita y se pregunta -------------------------
    diff = _panel(DIFF, X_TERMINAL)
    scene.play(FadeOut(viejo, shift=LEFT * 0.15), run_time=0.4)
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.12) for f in nuevas],
                    lag_ratio=0.4),
        run_time=1.0,
    )
    scene.play(FadeOut(prompt[1]), run_time=0.25)
    teclear(scene, diff, ritmo=0.28)
    scene.next_slide()

    # ---------------------- git add, y el silencio -------------------------
    # Los renglones nuevos se ponen del color del staging, y el diff se queda
    # callado: los dos sitios que compara han pasado a ser el mismo. Aquí se
    # corta, con el prompt vacío en pantalla.
    staged = _panel(STAGED, X_TERMINAL)
    scene.play(FadeOut(diff[1]), run_time=0.25)
    teclear(scene, staged, *TRAMOS_STAGED[0], ritmo=0.3)
    scene.play(nuevas.animate.set_color(STAGING), run_time=0.6)
    teclear(scene, staged, *TRAMOS_STAGED[1], ritmo=0.3)
    scene.next_slide()

    # ---------------------- --cached ---------------------------------------
    teclear(scene, staged, *TRAMOS_STAGED[2], ritmo=0.28)
    scene.next_slide()

    # ---------------------- -w ---------------------------------------------
    # Primero la lista tal y como está en el commit: escrita a ras, sin tabular
    # y con el día viejo. Nada que preguntarle a git todavía.
    lista = _panel(LISTA, X_ARCHIVO, NOMBRE)
    otro_prompt = _panel(PROMPT, X_TERMINAL)

    scene.play(FadeOut(readme[1]), FadeOut(staged[1]), run_time=0.4)
    teclear(scene, lista, ritmo=0.22)
    scene.play(FadeIn(otro_prompt[1][0]), run_time=0.3)
    scene.next_slide()

    # Y ahora los dos retoques, en este orden y a la vista: se tabula la lista
    # entera —que no cambia ni una letra— y se cambia el día de una. Para git
    # las dos cosas pesan lo mismo: seis renglones.
    tabulados = VGroup(*[lista[1][i] for i in FILAS_LISTA])
    espacios = _panel(ESPACIOS, X_TERMINAL)

    scene.play(tabulados.animate.shift(RIGHT * SANGRIA * _paso()), run_time=0.7)
    dia = linea_terminal(DIA_NUEVO, "txt", TAM).move_to(lista[1][FILA_DIA], LEFT)
    scene.play(Transform(lista[1][FILA_DIA], dia), run_time=0.6)
    scene.play(FadeOut(otro_prompt[1]), run_time=0.25)
    teclear(scene, espacios, ritmo=0.22)
    scene.next_slide()

    # ``-w`` no lanza otro diff encima: tacha del que ya está los renglones que
    # solo cambiaron en espacios, y los que quedan suben a ocupar su sitio.
    filas = espacios[1]
    alturas = [f.get_y() for f in filas]
    orden = linea_terminal(CON_W, "cmd", TAM).move_to(filas[0], LEFT)
    scene.play(
        Transform(filas[0], orden),
        *[FadeOut(filas[i], shift=RIGHT * 0.25) for i in RUIDO],
        *[filas[q].animate.shift(UP * (alturas[d] - alturas[q]))
          for d, q in enumerate(QUEDAN, start=2)],
        run_time=1.0,
    )
    scene.next_slide()

    # ---------------------- Entre dos commits ------------------------------
    # Los dos sitios no tienen por qué ser zonas. A la izquierda el archivo tal
    # y como era en aquel commit —lo dice el rótulo de la ventana, que es lo
    # único que cambia del marco en toda la diapositiva— y a la derecha el
    # hueco entre ese commit y el siguiente.
    commiteado = _panel(COMMITEADO, X_ARCHIVO, NOMBRE_VIEJO)
    entre = _panel(ENTRE_COMMITS, X_TERMINAL)
    rotulo = texto(NOMBRE_VIEJO, TAM - 2, color=SECUNDARIO)
    rotulo.move_to(marco_archivo[3])
    # De la terminal solo se apaga lo que quedó vivo después del ``-w``: las
    # filas que ya se fueron no se vuelven a tocar, o reaparecerían de golpe.
    vivas = VGroup(filas[0], filas[1], *[filas[q] for q in QUEDAN])

    scene.play(FadeOut(lista[1]), FadeOut(vivas),
               Transform(marco_archivo[3], rotulo), run_time=0.6)
    teclear(scene, commiteado, ritmo=0.22)
    teclear(scene, entre, *TRAMOS_COMMITS[0], ritmo=0.28)
    teclear(scene, entre, *TRAMOS_COMMITS[1], ritmo=0.26)
    scene.wait(0.3)
    scene.next_slide()
