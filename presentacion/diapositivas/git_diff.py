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

TAM = 16
ANCHO_PANEL = 6.4
ALTO_PANEL = 5.1
MARGEN = 0.4
BUFF = 0.2
X_ARCHIVO, X_TERMINAL = -3.5, 3.5
Y_PANEL = -0.25
NOMBRE = "README.md"

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
FILAS_LEMA = (4, 5, 6)

LISTA = (
    ("## Retos", "txt"),
    ("", "sep"),
    ("* Retos semanales", "txt"),
    ("* Sesiones los viernes", "txt"),
    ("* Proyecto final", "txt"),
)
FILAS_LISTA = (2, 3, 4)
FILA_DIA = 3
DIA_NUEVO = "* Sesiones los jueves"
SANGRIA = 2

COMMITEADO = (
    ("# Aperture", "txt"),
    ("", "sep"),
    ("### Semillero de Data Science e IA", "txt"),
    ("", "sep"),
    (LEMA_VIEJO, "txt"),
)
VIEJO = "3a1f2c4"
NOMBRE_VIEJO = f"{NOMBRE} @ {VIEJO}"

PROMPT = (("", "cmd"),)

DIFF = (
    ("git diff", "cmd"),
    ("@@ -5 +5,3 @@", "avi"),
    ("- *Aprendemos IA juntos.*", "err"),
    ("+ *No solo estudiamos la IA.", "ok"),
    ("+ La construimos y la llevamos", "ok"),
    ("+ a la realidad.*", "ok"),
)

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
RUIDO = (2, 4, 5, 7)
QUEDAN = (3, 6)
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
    chrome = ventana(ANCHO_PANEL, ALTO_PANEL, nombre, TAM - 2)
    chrome.move_to([x, Y_PANEL, 0])
    filas = VGroup(*[linea_terminal(c, t, TAM) for c, t in lineas])
    if len(filas):
        filas.arrange(DOWN, buff=BUFF, aligned_edge=LEFT)
        filas.move_to(chrome[0].get_top() + DOWN * (ALTO_BARRA + MARGEN), UP)
        filas.align_to(chrome[0].get_left() + RIGHT * MARGEN, LEFT)
    return VGroup(chrome, filas)


def _paso():
    return texto("mm", TAM).width - texto("m", TAM).width


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    readme = _panel(README, X_ARCHIVO, NOMBRE)
    prompt = _panel(PROMPT, X_TERMINAL)
    marco_archivo, marco_consola = readme[0], prompt[0]

    nuevas = VGroup(*[readme[1][i] for i in FILAS_LEMA])
    viejo = linea_terminal(LEMA_VIEJO, "txt", TAM)
    viejo.move_to(readme[1][FILAS_LEMA[0]]).align_to(readme[1][0], LEFT)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(marco_archivo), FadeIn(marco_consola), run_time=0.6)
    teclear(scene, readme, 0, FILAS_LEMA[0], ritmo=0.26)
    scene.play(FadeIn(viejo, shift=RIGHT * 0.12),
               FadeIn(prompt[1][0]), run_time=0.35)
    scene.next_slide()

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

    staged = _panel(STAGED, X_TERMINAL)
    scene.play(FadeOut(diff[1]), run_time=0.25)
    teclear(scene, staged, *TRAMOS_STAGED[0], ritmo=0.3)
    scene.play(nuevas.animate.set_color(STAGING), run_time=0.6)
    teclear(scene, staged, *TRAMOS_STAGED[1], ritmo=0.3)
    scene.next_slide()

    teclear(scene, staged, *TRAMOS_STAGED[2], ritmo=0.28)
    scene.next_slide()

    lista = _panel(LISTA, X_ARCHIVO, NOMBRE)
    otro_prompt = _panel(PROMPT, X_TERMINAL)

    scene.play(FadeOut(readme[1]), FadeOut(staged[1]), run_time=0.4)
    teclear(scene, lista, ritmo=0.22)
    scene.play(FadeIn(otro_prompt[1][0]), run_time=0.3)
    scene.next_slide()

    tabulados = VGroup(*[lista[1][i] for i in FILAS_LISTA])
    espacios = _panel(ESPACIOS, X_TERMINAL)

    scene.play(tabulados.animate.shift(RIGHT * SANGRIA * _paso()), run_time=0.7)
    dia = linea_terminal(DIA_NUEVO, "txt", TAM).move_to(lista[1][FILA_DIA], LEFT)
    scene.play(Transform(lista[1][FILA_DIA], dia), run_time=0.6)
    scene.play(FadeOut(otro_prompt[1]), run_time=0.25)
    teclear(scene, espacios, ritmo=0.22)
    scene.next_slide()

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

    commiteado = _panel(COMMITEADO, X_ARCHIVO, NOMBRE_VIEJO)
    entre = _panel(ENTRE_COMMITS, X_TERMINAL)
    rotulo = texto(NOMBRE_VIEJO, TAM - 2, color=SECUNDARIO)
    rotulo.move_to(marco_archivo[3])
    vivas = VGroup(filas[0], filas[1], *[filas[q] for q in QUEDAN])

    scene.play(FadeOut(lista[1]), FadeOut(vivas),
               Transform(marco_archivo[3], rotulo), run_time=0.6)
    teclear(scene, commiteado, ritmo=0.22)
    teclear(scene, entre, *TRAMOS_COMMITS[0], ritmo=0.28)
    teclear(scene, entre, *TRAMOS_COMMITS[1], ritmo=0.26)
    scene.wait(0.3)
    scene.next_slide()
