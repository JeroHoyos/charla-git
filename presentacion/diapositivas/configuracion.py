from manim import (
    DOWN,
    RIGHT,
    UP,
    FadeIn,
    LaggedStart,
    RoundedRectangle,
    VGroup,
)

from animaciones import teclear
from componentes import terminal, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, PRIMARIO, SECUNDARIO

IDENTIDAD = (
    ("git config --global user.name carmen_electra", "cmd"),
    ("git config --global user.email carmen.electra@unal.edu.co", "cmd"),
    ("", "sep"),
    ("para que la rama inicial se llame main, el estándar actual", "com"),
    ("git config --global init.defaultBranch main", "cmd"),
    ("", "sep"),
    ("git config --list", "cmd"),
    ("user.name=carmen_electra", "out"),
    ("user.email=carmen.electra@unal.edu.co", "out"),
    ("init.defaultBranch=main", "out"),
)

NIVELES = (
    ("--system", "todo el equipo", SECUNDARIO),
    ("--global", "~/.gitconfig", PRIMARIO),
    ("--local", ".git/config", AMBAR),
)


def _nivel(bandera, donde, color):
    etiqueta = texto(bandera, 17, color=color)
    ruta = texto(donde, 13, color=SECUNDARIO)
    dentro = VGroup(etiqueta, ruta).arrange(DOWN, buff=0.12)
    caja = RoundedRectangle(
        width=dentro.width + 0.7, height=dentro.height + 0.45,
        corner_radius=0.12, stroke_color=color, stroke_width=2.5,
    ).set_fill(color, opacity=0.07)
    return VGroup(caja, dentro.move_to(caja.get_center()))


def construir(scene):
    encabezado = hacer_titulo("Configurar")

    consola = terminal(IDENTIDAD, tam=14, buff=0.12, margen=0.40)
    consola.move_to([0, 0.42, 0])

    niveles = VGroup(*[_nivel(*n) for n in NIVELES])
    niveles.arrange(RIGHT, buff=0.55).move_to([0, -2.60, 0])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(consola[0]), run_time=0.5)
    teclear(scene, consola, ritmo=0.4)
    scene.play(
        LaggedStart(*[FadeIn(n, shift=UP * 0.12) for n in niveles],
                    lag_ratio=0.3),
        run_time=1.0,
    )
    scene.next_slide()
