from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    LaggedStart,
    VGroup,
)

from animaciones import teclear
from componentes import archivo, aspa, carpeta, terminal, texto, visto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, ERROR, OK, SECUNDARIO

TITULOS = (
    "Un proyecto de datos",
    ".gitignore",
    "Patrones y excepciones",
)

PROYECTO = (
    (True, "data/", False, "2.1 GB", AMBAR),
    (True, "models/", False, "480 MB", AMBAR),
    (True, "notebooks/", True, "", None),
    (True, "src/", True, "", None),
    (True, ".venv/", False, "se recrea con uv sync", SECUNDARIO),
    (False, ".env", False, "credenciales", ERROR),
    (False, "pyproject.toml", True, "", None),
    (False, "uv.lock", True, "", None),
    (False, "README.md", True, "", None),
)
X_ICONO, X_NOMBRE = -4.7, -4.1
X_MARCA, X_MOTIVO = -0.5, -0.05
Y_PRIMERO = 2.0
PASO_FILA = 0.62
ALTO_ICONO = 0.42
TAM_NOMBRE = 21
TAM_MOTIVO = 18
APAGADO = 0.55

IGNORE = (
    ("datos y modelos, que pesan gigas", "com"),
    ("data/", "txt"),
    ("models/", "txt"),
    ("", "sep"),
    ("el entorno se recrea con uv sync", "com"),
    (".venv/", "txt"),
    ("__pycache__/", "txt"),
    ("", "sep"),
    ("credenciales que no se suben nunca", "com"),
    (".env", "txt"),
)
TAM_IGNORE = 18
Y_IGNORE = -0.1
BUFF_IGNORE = 0.15
MATIZ = "si ya lo commiteaste, sácalo antes con git rm --cached"

PATRONES = (
    ("*.csv", "cualquier archivo .csv", True),
    ("models/", "la carpeta entera", True),
    ("/notas.txt", "solo el de la raíz", True),
    ("**/tmp/", "en cualquier nivel", True),
    ("!data/muestra.csv", "menos este, que sí sube", False),
)
X_PATRON, X_MARCA_PATRON, X_QUE_COGE = -5.6, -1.5, -1.0
Y_PATRONES = 1.5
PASO_PATRON = 0.78
TAM_PATRON = 21
TAM_QUE_COGE = 18
ORDEN = (
    "git lee el archivo de arriba abajo, regla por regla",
    "cuando dos se pisan, manda la última que coincide",
)
TAM_ORDEN = 21
Y_ORDEN = -2.5
BUFF_ORDEN = 0.28


def _fila(es_carpeta, nombre, sube, motivo, color, y):
    tinte = CLARO if sube else SECUNDARIO
    icono = (carpeta(ALTO_ICONO, tinte) if es_carpeta
             else archivo("", tinte, ALTO_ICONO))
    icono.move_to([X_ICONO, y, 0])
    etiqueta = texto(nombre, TAM_NOMBRE, color=tinte)
    etiqueta.move_to([X_NOMBRE, y, 0], LEFT)
    marca = visto(OK) if sube else aspa(ERROR)
    marca.move_to([X_MARCA, y, 0])
    fila = VGroup(icono, etiqueta, marca)
    if not sube:
        VGroup(icono, etiqueta).set_opacity(APAGADO)
        fila.add(texto(motivo, TAM_MOTIVO, color=color).move_to(
            [X_MOTIVO, y, 0], LEFT))
    return fila


def construir(scene):
    encabezado = hacer_titulo(TITULOS[0])
    filas = VGroup(*[
        _fila(*pieza, Y_PRIMERO - i * PASO_FILA)
        for i, pieza in enumerate(PROYECTO)
    ])
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.15) for f in filas],
                    lag_ratio=0.25),
        run_time=2.4,
    )
    scene.next_slide()

    otro_encabezado = hacer_titulo(TITULOS[1])
    fichero = terminal(IGNORE, tam=TAM_IGNORE, buff=BUFF_IGNORE,
                       nombre=".gitignore")
    fichero.move_to([0, Y_IGNORE, 0])
    matiz = texto(MATIZ, 16, color=SECUNDARIO).to_edge(DOWN, buff=0.6)

    scene.play(
        FadeOut(filas),
        FadeOut(encabezado), FadeIn(otro_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(fichero[0]), run_time=0.5)
    teclear(scene, fichero, ritmo=0.24)
    scene.play(FadeIn(matiz, shift=UP * 0.1), run_time=0.5)
    scene.next_slide()

    ultimo_encabezado = hacer_titulo(TITULOS[2])
    reglas = VGroup()
    for i, (patron, que_coge, ignora) in enumerate(PATRONES):
        y = Y_PATRONES - i * PASO_PATRON
        color = CLARO if ignora else OK
        marca = aspa(ERROR) if ignora else visto(OK)
        reglas.add(VGroup(
            texto(patron, TAM_PATRON, color=color).move_to(
                [X_PATRON, y, 0], LEFT),
            marca.move_to([X_MARCA_PATRON, y, 0]),
            texto(que_coge, TAM_QUE_COGE, color=SECUNDARIO).move_to(
                [X_QUE_COGE, y, 0], LEFT),
        ))
    orden = VGroup(*[
        texto(linea, TAM_ORDEN, color=AMBAR) for linea in ORDEN
    ]).arrange(DOWN, buff=BUFF_ORDEN).move_to([0, Y_ORDEN, 0])

    scene.play(
        FadeOut(fichero), FadeOut(matiz),
        FadeOut(otro_encabezado),
        FadeIn(ultimo_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in reglas],
                    lag_ratio=0.3),
        run_time=1.8,
    )
    scene.play(FadeIn(orden, shift=UP * 0.1), run_time=0.5)
    scene.next_slide()
