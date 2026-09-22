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
from componentes import aspa, linea_terminal, terminal, texto, visto
from componentes import titulo as hacer_titulo
from estilo import ERROR, OK

TITULOS = (
    "El mismo cambio, dos mensajes",
    "Crear un buen historial",
)

TIPO, AMBITO = "fix", "(modelo)"
DESCRIPCION = "entrena sin el conjunto de prueba"
MENSAJE = f"{TIPO}: {DESCRIPCION}"

ARCHIVO = "modelo.py"
DIFF = (
    ("@@ -18,7 +18,7 @@ def entrenar(datos):", "out"),
    ("-   modelo.fit(X_test, y_test)", "err"),
    ("+   modelo.fit(X_train, y_train)", "ok"),
)
TAM_DIFF = 21
MARGEN_DIFF = 0.5
Y_DIFF = 1.15

MENSAJES = (
    ('git commit -m "cambios"', False),
    (f'git commit -m "{MENSAJE}"', True),
)
TAM_MENSAJE = 21
Y_MENSAJES = (-1.3, -2.45)
X_MARCA = -6.2
BUFF_MARCA = 0.5
APAGADO = 0.5

LOG_MALO = (
    ("git log --oneline", "cmd"),
    ("3f2a cambios", "out"),
    ("9d1c update", "out"),
    ("7b0e asdf", "out"),
    ("1a4d ahora si", "out"),
)
LOG_BUENO = (
    ("git log --oneline", "cmd"),
    (f"3f2a {MENSAJE}", "out"),
    ("9d1c feat: anade el cargador de CSV", "out"),
    ("7b0e docs: explica como entrenar", "out"),
    ("1a4d test: cubre el caso vacio", "out"),
)
TAM_LOG = 14
ANCHO_LOG = 6.2
X_LOGS = (-3.4, 3.4)
Y_LOGS = -0.55
GLOSA_MALO = "no dice qué cambió ni por qué"
GLOSA_BUENO = "dice qué cambió y por qué"
TAM_GLOSA = 21
Y_GLOSA = 1.7


def _marcado(mob, vale):
    marca = (visto(OK, tam=0.13) if vale else aspa(ERROR, tam=0.13))
    marca.move_to([X_MARCA, mob.get_y(), 0])
    if not vale:
        mob.set_opacity(APAGADO)
    return VGroup(marca, mob)


def construir(scene):
    encabezado = hacer_titulo(TITULOS[0])

    diff = terminal(DIFF, tam=TAM_DIFF, nombre=ARCHIVO,
                    margen=MARGEN_DIFF)
    diff.move_to([0, Y_DIFF, 0])
    mensajes = VGroup(*[
        _marcado(
            linea_terminal(orden, "cmd", TAM_MENSAJE)
            .move_to([X_MARCA + BUFF_MARCA, y, 0], LEFT),
            vale,
        )
        for (orden, vale), y in zip(MENSAJES, Y_MENSAJES)
    ])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(diff[0]), run_time=0.5)
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.12) for f in diff[1]],
                    lag_ratio=0.35),
        run_time=1.1,
    )
    scene.play(FadeIn(mensajes[0], shift=UP * 0.12), run_time=0.6)
    scene.next_slide()
    scene.play(FadeIn(mensajes[1], shift=UP * 0.12), run_time=0.6)
    scene.next_slide()

    otro_encabezado = hacer_titulo(TITULOS[1])
    logs, glosas = VGroup(), VGroup()
    for lineas, x, glosa, color, marca in (
        (LOG_MALO, X_LOGS[0], GLOSA_MALO, ERROR, aspa(ERROR, tam=0.16)),
        (LOG_BUENO, X_LOGS[1], GLOSA_BUENO, OK, visto(OK, tam=0.16)),
    ):
        ventana = terminal(lineas, tam=TAM_LOG, ancho=ANCHO_LOG,
                           nombre="terminal")
        logs.add(ventana.move_to([x, Y_LOGS, 0]))
        rotulo = texto(glosa, TAM_GLOSA, color=color)
        glosas.add(VGroup(marca, rotulo).arrange(RIGHT, buff=0.25)
                   .move_to([x, Y_GLOSA, 0]))

    scene.play(
        FadeOut(diff), FadeOut(mensajes),
        FadeOut(encabezado), FadeIn(otro_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(*[FadeIn(v[0]) for v in logs], run_time=0.5)
    for ventana, glosa in zip(logs, glosas):
        teclear(scene, ventana, ritmo=0.22)
        scene.play(FadeIn(glosa, shift=DOWN * 0.1), run_time=0.5)
    scene.next_slide()
