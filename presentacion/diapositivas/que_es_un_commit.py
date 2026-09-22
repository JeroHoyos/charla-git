from manim import (
    DOWN,
    UP,
    Create,
    CurvedArrow,
    FadeIn,
    FadeOut,
    Flash,
    GrowFromCenter,
    LaggedStart,
    Rectangle,
    Transform,
    TransformFromCopy,
    VGroup,
)

from componentes import (
    archivo,
    arista,
    foto_proyecto,
    linea_terminal,
    nodo_commit,
    texto,
    zona,
)
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, RAMA_MAIN, SECUNDARIO

from .tres_zonas import EJEMPLO, HASH, MENSAJE

TITULO = "Un commit es una foto"

COMMITS = (
    ("0e5f", "descargando arch"),
    ("77ab", "instalando arch"),
    ("9c1d", "se me desconfiguro arch"),
    (HASH, MENSAJE),
)

X_CADENA = (-4.5, -1.5, 1.5, 4.5)
RADIO = 0.32
TAM_HASH = 15
TAM_MENSAJE = 13
SOBRE_EL_NODO = 0.62
ESCALA_FOTO_MINI = 0.85
ESCALA_FOTO_GRANDE = 1.9

Y_CADENA = -2.05
Y_FOTO = -1.12

ANCHO_ZONA, ALTO_ZONA = 4.4, 2.1
Y_ZONA = 1.45
ROTULO_ZONA = "tu proyecto ahora"
ALTO_ARCHIVO = 1.1
TAM_ARCHIVO = 15
Y_ORDEN = -0.2
TAM_ORDEN = 17

I_VUELTA = 1


def cadena(y):
    nodos = VGroup(*[
        nodo_commit(corto, RAMA_MAIN, RADIO, TAM_HASH).move_to([x, y, 0])
        for x, (corto, _) in zip(X_CADENA, COMMITS)
    ])
    aristas = VGroup(*[
        arista(a, b, RAMA_MAIN, RADIO) for a, b in zip(nodos, nodos[1:])
    ])
    return nodos, aristas


def mensajes(y):
    return VGroup(*[
        texto(mensaje, TAM_MENSAJE, color=CLARO).move_to(
            [x, y + SOBRE_EL_NODO, 0])
        for x, (_, mensaje) in zip(X_CADENA, COMMITS)
    ])


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    caja = zona(ROTULO_ZONA, SECUNDARIO, ANCHO_ZONA, ALTO_ZONA, 17)
    caja.move_to([0, Y_ZONA, 0])
    archivos = archivo(EJEMPLO, SECUNDARIO, ALTO_ARCHIVO, TAM_ARCHIVO)
    archivos.move_to([0, Y_ZONA - 0.08, 0])
    orden = linea_terminal(f'git commit -m "{MENSAJE}"', "cmd", TAM_ORDEN)
    orden.move_to([0, Y_ORDEN, 0])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(caja), run_time=0.5)
    scene.play(FadeIn(archivos, shift=UP * 0.12), run_time=0.7)
    scene.play(FadeIn(orden, shift=DOWN * 0.1), run_time=0.5)

    destello = Rectangle(
        width=ANCHO_ZONA, height=ALTO_ZONA, stroke_width=0,
    ).set_fill(CLARO, opacity=0.55).move_to([0, Y_ZONA, 0])
    foto = foto_proyecto(ESCALA_FOTO_GRANDE, RAMA_MAIN).move_to([0, Y_ZONA, 0])
    scene.play(FadeIn(destello), run_time=0.14)
    scene.play(FadeOut(destello), FadeIn(foto), run_time=0.3)

    nodos, aristas = cadena(Y_CADENA)
    mini = foto_proyecto(ESCALA_FOTO_MINI, RAMA_MAIN)
    mini.move_to([X_CADENA[-1], Y_FOTO, 0])
    scene.play(Transform(foto, mini), GrowFromCenter(nodos[-1]), run_time=0.9)
    scene.next_slide()

    fotos = VGroup(*[
        foto_proyecto(ESCALA_FOTO_MINI, vacia=True).move_to([x, Y_FOTO, 0])
        for x in X_CADENA[:-1]
    ])
    scene.play(
        LaggedStart(*[
            LaggedStart(GrowFromCenter(nodo), FadeIn(vieja), lag_ratio=0.4)
            for nodo, vieja in zip(nodos[-2::-1], fotos[::-1])
        ], lag_ratio=0.45),
        run_time=1.6,
    )
    scene.play(
        LaggedStart(*[Create(a) for a in aristas[::-1]], lag_ratio=0.3),
        run_time=0.9,
    )
    scene.next_slide()

    vuelta = CurvedArrow(
        nodos[-1].get_bottom() + DOWN * 0.12,
        nodos[I_VUELTA].get_bottom() + DOWN * 0.12,
        angle=-0.6, color=AMBAR, stroke_width=4, tip_length=0.22,
    )
    restaurada = foto_proyecto(ESCALA_FOTO_GRANDE, AMBAR, vacia=True)
    restaurada.move_to([0, Y_ZONA, 0])

    scene.play(Create(vuelta), run_time=0.7)
    scene.play(
        Flash(nodos[I_VUELTA], color=AMBAR, line_length=0.2, num_lines=14,
              flash_radius=0.6),
        TransformFromCopy(fotos[I_VUELTA], restaurada),
        FadeOut(archivos),
        run_time=1.0,
    )
    scene.next_slide()
