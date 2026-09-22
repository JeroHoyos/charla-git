from manim import (
    BOLD,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Create,
    FadeIn,
    FadeOut,
    Flash,
    LaggedStart,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    VGroup,
)

from animaciones import flecha, pulso, teclear
from componentes import (
    ALTO_BARRA,
    archivo,
    cajon,
    carpeta,
    carriles,
    discos,
    linea_terminal,
    nodo_commit,
    tarjeta,
    texto,
    ventana,
    zona,
)
from componentes import titulo as hacer_titulo
from estilo import ERROR, OK, RAMA_MAIN, SECUNDARIO, STAGING, SUPERFICIE

TITULO = "Las tres zonas"

ZONAS = (
    ("directorio de trabajo", SECUNDARIO, False),
    ("staging", STAGING, True),
    ("repositorio", RAMA_MAIN, False),
)
ANCHO_ZONA = 9.4
ALTO_ZONA = 1.3
Y_ZONAS = (1.95, -0.1, -2.15)
TAM_ROTULO = 21
BUFF_ROTULO = 0.45

PASOS = (("git add", STAGING), ("git commit", RAMA_MAIN))
TAM_COMANDO = 19
N_ARCHIVOS = 3
ALTO_ARCHIVO = 0.72
BUFF_ARCHIVOS = 0.5
X_ARCHIVOS = 2.3
FANTASMA = 0.25
SELLO = "guardado"
X_SELLO = 4.15

X_CARRILES = (-3.4, 0.0, 3.4)
TAM_CARRIL = 19
ALTO_ICONO = 0.92

EJEMPLO = "i-use-arch.btw"
MENSAJE = "flexeando arch"
HASH = "7d3e"
Y_CARRIL_CORTO = -1.35
Y_EJEMPLO = -0.12
ALTO_EJEMPLO = 0.6
RADIO_NODO = 0.3
TAM_EJEMPLO = 15
BUFF_PARADA = 0.16
MARGEN_PARADA = (0.5, 0.4)

COLOR_PARADA = (ERROR, STAGING, RAMA_MAIN)

SESION = (
    (("git status", "cmd"),
     ("Untracked files:", "out"),
     (f"      {EJEMPLO}", "err")),
    ((f"git add {EJEMPLO}", "cmd"),
     ("git status", "cmd"),
     ("Changes to be committed:", "out"),
     (f"      new file:   {EJEMPLO}", "ok")),
    ((f'git commit -m "{MENSAJE}"', "cmd"),
     (f"[main {HASH}] {MENSAJE}", "out"),
     ("git status", "cmd"),
     ("nothing to commit, working tree clean", "ok")),
)
ANCHO_CONSOLA = 8.0
ALTO_CONSOLA = 2.15
Y_CONSOLA = -2.62
MARGEN_CONSOLA = 0.5
TAM_SESION = 15
BUFF_SESION = 0.17
Y_SESION = Y_CONSOLA + ALTO_CONSOLA / 2 - ALTO_BARRA - 0.2


def _zonas():
    cajas = []
    for (nombre, color, discontinua), y in zip(ZONAS, Y_ZONAS):
        caja = zona(nombre, color, ANCHO_ZONA, ALTO_ZONA, TAM_ROTULO,
                    discontinua)
        caja[0].move_to([0, y, 0])
        caja[1].move_to(
            caja[0].get_left() + RIGHT * (caja[1].width / 2 + BUFF_ROTULO))
        cajas.append(caja)
    return cajas


def _puentes(cajas):
    puentes = VGroup()
    for (comando, color), arriba, abajo in zip(PASOS, cajas, cajas[1:]):
        punta = flecha([0, arriba[0].get_bottom()[1], 0],
                       [0, abajo[0].get_top()[1], 0],
                       color=color, buff=0.08, grosor=4)
        etiqueta = texto(comando, TAM_COMANDO, color=color)
        etiqueta.next_to(punta, RIGHT, buff=0.3)
        puentes.add(VGroup(punta, etiqueta))
    return puentes


def _archivos():
    iconos = VGroup(*[
        archivo(color=SECUNDARIO, alto=ALTO_ARCHIVO) for _ in range(N_ARCHIVOS)
    ]).arrange(RIGHT, buff=BUFF_ARCHIVOS)
    return iconos.move_to([X_ARCHIVOS, Y_ZONAS[0], 0])


def carriles_zonas():
    iconos = (
        carpeta(ALTO_ICONO, SECUNDARIO),
        cajon(ALTO_ICONO, STAGING),
        discos(ALTO_ICONO, RAMA_MAIN),
    )
    zonas = [(icono, nombre, color)
             for icono, (nombre, color, _) in zip(iconos, ZONAS)]
    return carriles(zonas, X_CARRILES, tam=TAM_CARRIL)


def _parada(indice, color=None, fantasma=False):
    color = COLOR_PARADA[indice] if color is None else color
    pieza = (nodo_commit(HASH, color, RADIO_NODO, TAM_EJEMPLO - 1)
             if indice == len(X_CARRILES) - 1
             else archivo(color=color, alto=ALTO_EJEMPLO))
    contenido = VGroup(
        pieza, texto(EJEMPLO, TAM_EJEMPLO, color=color),
    ).arrange(DOWN, buff=BUFF_PARADA)
    caja = RoundedRectangle(
        width=contenido.width + MARGEN_PARADA[0],
        height=contenido.height + MARGEN_PARADA[1],
        corner_radius=0.14, stroke_color=color, stroke_width=2.5,
    ).set_fill(SUPERFICIE, opacity=1.0)
    caja.move_to(contenido.get_center())
    if fantasma:
        contenido.set_opacity(FANTASMA)
        caja.set_stroke(opacity=FANTASMA)
    return VGroup(caja, contenido).move_to([X_CARRILES[indice], Y_EJEMPLO, 0])


def _marco_consola():
    return ventana(ANCHO_CONSOLA, ALTO_CONSOLA, "terminal", 14).move_to(
        [0, Y_CONSOLA, 0])


def _sesion(indice):
    filas = VGroup(*[
        linea_terminal(c, t, TAM_SESION) for c, t in SESION[indice]
    ]).arrange(DOWN, buff=BUFF_SESION, aligned_edge=LEFT)
    filas.align_to([0, Y_SESION, 0], UP)
    return filas.align_to([-ANCHO_CONSOLA / 2 + MARGEN_CONSOLA, 0, 0], LEFT)


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    cajas = _zonas()
    puentes = _puentes(cajas)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[Create(caja[0]) for caja in cajas], lag_ratio=0.35),
        run_time=1.4,
    )
    scene.play(
        LaggedStart(*[FadeIn(caja[1], shift=RIGHT * 0.15) for caja in cajas],
                    lag_ratio=0.3),
        run_time=0.9,
    )
    scene.play(
        LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in puentes],
                    lag_ratio=0.4),
        run_time=1.0,
    )
    scene.next_slide()

    ficheros = _archivos()
    scene.play(
        LaggedStart(*[FadeIn(f, shift=UP * 0.12) for f in ficheros],
                    lag_ratio=0.25),
        run_time=0.9,
    )

    copias = ficheros.copy()
    scene.add(copias)
    scene.play(
        LaggedStart(*[
            copia.animate.move_to(
                [copia.get_center()[0], Y_ZONAS[1], 0]).set_color(STAGING)
            for copia in copias
        ], lag_ratio=0.3),
        ficheros.animate.set_opacity(FANTASMA),
        pulso(puentes[0][0], STAGING, run_time=1.2, ancho=9),
        run_time=1.4,
    )
    scene.next_slide()

    commit = nodo_commit("a1c9", RAMA_MAIN, 0.42, 16)
    commit.move_to([X_ARCHIVOS, Y_ZONAS[2], 0])
    sello = tarjeta([(SELLO, 22, BOLD)], color=OK).rotate(-0.16)
    sello.move_to([X_SELLO, Y_ZONAS[2], 0])

    scene.play(
        ReplacementTransform(copias, commit),
        pulso(puentes[1][0], RAMA_MAIN, run_time=1.0, ancho=9),
        run_time=1.1,
    )
    scene.play(
        Flash(commit, color=RAMA_MAIN, line_length=0.28, num_lines=18,
              flash_radius=0.9),
        FadeIn(sello, scale=1.9),
        ficheros.animate.set_opacity(1.0),
        run_time=0.7,
    )
    scene.wait(0.3)
    scene.next_slide()

    pistas = carriles_zonas()
    scene.play(
        FadeOut(puentes), FadeOut(ficheros), FadeOut(commit), FadeOut(sello),
        run_time=0.5,
    )
    scene.play(
        LaggedStart(*[
            AnimationGroup(
                ReplacementTransform(caja[0], pista[2]),
                ReplacementTransform(caja[1], pista[1]),
            )
            for caja, pista in zip(cajas, pistas)
        ], lag_ratio=0.25),
        run_time=1.4,
    )
    scene.play(
        LaggedStart(*[FadeIn(pista[0], shift=DOWN * 0.15) for pista in pistas],
                    lag_ratio=0.25),
        run_time=0.9,
    )
    scene.next_slide()

    scene.play(
        *[pista[2].animate.put_start_and_end_on(
            pista[2].get_start(), [x, Y_CARRIL_CORTO, 0])
          for pista, x in zip(pistas, X_CARRILES)],
        run_time=0.6,
    )

    marco_consola = _marco_consola()
    ejemplo = _parada(0)

    scene.play(FadeIn(marco_consola), FadeIn(ejemplo, shift=UP * 0.12),
               run_time=0.6)
    sesion = _sesion(0)
    teclear(scene, VGroup(marco_consola, sesion), ritmo=0.3)
    scene.next_slide()

    copia = ejemplo.copy()
    scene.add(copia)
    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(1)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.3)
    scene.play(
        Transform(copia, _parada(1)),
        Transform(ejemplo, _parada(0, fantasma=True)),
        run_time=1.0,
    )
    teclear(scene, VGroup(marco_consola, sesion), desde=1, ritmo=0.3)
    scene.next_slide()

    guardado = _parada(2)
    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(2)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.3)
    scene.play(ReplacementTransform(copia, guardado), run_time=1.0)
    scene.play(
        Flash(guardado[1][0], color=RAMA_MAIN, line_length=0.28, num_lines=18,
              flash_radius=0.9),
        Transform(ejemplo, _parada(0, color=SECUNDARIO)),
        run_time=0.6,
    )
    teclear(scene, VGroup(marco_consola, sesion), desde=1, ritmo=0.3)
    scene.wait(0.3)

    scene.next_slide()
