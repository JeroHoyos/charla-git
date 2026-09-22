from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    LaggedStart,
    Transform,
    VGroup,
)

from animaciones import flecha
from componentes import barra, puntero, terminal, texto
from componentes import titulo as hacer_titulo
from estilo import CLARO, PRIMARIO, SECUNDARIO

TITULO_GRAFICA = "¿Y cómo lo usan?"
TITULO_ARBOL = "Rutas y carpetas"
TITULO_COMANDOS = "Comandos básicos"

INTERACCION = (
    ("línea de comandos", 83.57),
    ("editor de código", 54.49),
    ("la web del servicio", 28.44),
    ("app de escritorio", 26.37),
)
X_ETIQUETA = -2.8
X_BARRA = -2.5
LARGO_100 = 7.4
ALTO_TRAZO = 0.6
Y_PRIMERA_BARRA = 1.9
PASO_BARRA = 1.25
FUENTE = "Stack Overflow Developer Survey 2022"
Y_FUENTE = -2.95

ARBOL = (
    ("proyectos/", CLARO),
    ("├── charla-git/", PRIMARIO),
    ("│   ├── datos/", SECUNDARIO),
    ("│   ├── main.py", SECUNDARIO),
    ("│   └── README.md", SECUNDARIO),
    ("└── notas/", SECUNDARIO),
)
AQUI = 1
TAM_ARBOL = 32
BUFF_ARBOL = 0.06
X_ARBOL = -6.2
Y_ARBOL = 0.0
ATAJOS = (
    ("..", "la carpeta de arriba", 0),
    (".", "esta carpeta, la de ahora", AQUI),
)
LARGO_FLECHA = 1.1
X_GLOSA = 0.3
RUTA_PIE = "ruta absoluta:"
RUTA = "/c/Users/carmen/proyectos/charla-git"
Y_RUTA = -2.7

SESION = (
    ("pwd", "cmd"),
    ("/c/Users/carmen/proyectos", "out"),
    ("ls", "cmd"),
    ("charla-git/  notas/", "out"),
    ("mkdir git-101", "cmd"),
    ("ls", "cmd"),
    ("charla-git/  git-101/  notas/", "ok"),
    ("cd git-101", "cmd"),
    ("cd ..", "cmd"),
)
GLOSAS = (
    ("pwd", "¿dónde estoy?"),
    ("ls", "¿qué hay aquí?"),
    ("mkdir", "crear una carpeta"),
    ("cd", "moverte"),
)
PASOS = (
    (0, 2, None),
    (1, 4, None),
    (2, 7, None),
    (3, 8, "proyectos/git-101"),
    (None, 9, "proyectos"),
)
CARPETA = "proyectos"
X_FICHA = -6.4
X_QUE_HACE = -4.6
BUFF_GLOSAS = 0.85
X_SESION = 2.9
Y_SESION = 0.0
TAM_SESION = 19
NOTA = "en el cmd de Windows, ls se llama dir"
Y_NOTA = -3.05


def _grafica():
    filas = VGroup()
    for i, (nombre, porcentaje) in enumerate(INTERACCION):
        y = Y_PRIMERA_BARRA - i * PASO_BARRA
        destacado = i == 0
        color = PRIMARIO if destacado else SECUNDARIO
        etiqueta = texto(nombre, 21, color=CLARO if destacado else SECUNDARIO)
        etiqueta.move_to([X_ETIQUETA, y, 0], RIGHT)
        trazo = barra(LARGO_100 * porcentaje / 100, ALTO_TRAZO, color,
                      1.0 if destacado else 0.55)
        trazo.move_to([X_BARRA, y, 0], LEFT)
        valor = texto(f"{porcentaje:.2f} %".replace(".", ","), 21,
                      color=CLARO if destacado else SECUNDARIO)
        valor.next_to(trazo, RIGHT, buff=0.22)
        filas.add(VGroup(etiqueta, trazo, valor))

    fuente = texto(FUENTE, 17, color=SECUNDARIO).set_opacity(0.7)
    fuente.move_to([0, Y_FUENTE, 0])
    return filas, fuente


def _arbol():
    lineas = VGroup(*[
        texto(contenido, TAM_ARBOL, color=color) for contenido, color in ARBOL
    ]).arrange(DOWN, buff=BUFF_ARBOL, aligned_edge=LEFT)
    return lineas.move_to([X_ARBOL, Y_ARBOL, 0], LEFT)


def _ruta():
    linea = VGroup(
        texto(RUTA_PIE, 20, color=SECUNDARIO),
        texto(RUTA, 20, color=PRIMARIO),
    ).arrange(RIGHT, buff=0.3)
    return linea.move_to([X_ARBOL, Y_RUTA, 0], LEFT)


def _atajos(lineas):
    x_salida = lineas.get_right()[0] + 0.25 + LARGO_FLECHA
    filas = VGroup()
    for simbolo, glosa, indice in ATAJOS:
        color = PRIMARIO if indice == AQUI else CLARO
        y = lineas[indice].get_center()[1]
        punta = flecha([x_salida, y, 0],
                       [lineas[indice].get_right()[0] + 0.2, y, 0],
                       color=color, buff=0.05)
        ficha = puntero(simbolo, color, 24).move_to([x_salida + 0.2, y, 0], LEFT)
        que_es = texto(glosa, 22, color=color).move_to([X_GLOSA, y, 0], LEFT)
        filas.add(VGroup(punta, ficha, que_es))
    return filas


def _comandos():
    sesion = terminal(SESION, tam=TAM_SESION, nombre=CARPETA, margen=0.5,
                      buff=0.16)
    sesion.move_to([X_SESION, Y_SESION, 0])

    glosas = VGroup()
    for comando, que_hace in GLOSAS:
        ficha = puntero(comando, PRIMARIO, 24).move_to([X_FICHA, 0, 0], LEFT)
        glosas.add(VGroup(
            ficha, texto(que_hace, 22).move_to([X_QUE_HACE, 0, 0], LEFT),
        ))
    glosas.arrange(DOWN, buff=BUFF_GLOSAS, aligned_edge=LEFT)
    glosas.move_to([X_FICHA, Y_SESION, 0], LEFT)

    nota = texto(NOTA, 17, color=SECUNDARIO).set_opacity(0.7)
    nota.move_to([X_FICHA, Y_NOTA, 0], LEFT)
    return sesion, glosas, nota


def construir(scene):
    encabezado = hacer_titulo(TITULO_GRAFICA)
    filas, fuente = _grafica()

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    for etiqueta, trazo, valor in filas:
        scene.play(
            FadeIn(etiqueta, shift=RIGHT * 0.1),
            GrowFromEdge(trazo, LEFT),
            run_time=0.55,
        )
        scene.play(FadeIn(valor, shift=LEFT * 0.1), run_time=0.25)
    scene.play(FadeIn(fuente), run_time=0.5)
    scene.next_slide()

    encabezado_arbol = hacer_titulo(TITULO_ARBOL)
    lineas = _arbol()
    atajos = _atajos(lineas)
    ruta = _ruta()

    scene.play(
        FadeOut(filas), FadeOut(fuente),
        FadeOut(encabezado), FadeIn(encabezado_arbol, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeIn(linea, shift=RIGHT * 0.12) for linea in lineas],
                    lag_ratio=0.3),
        run_time=1.3,
    )
    for fila in atajos:
        scene.play(FadeIn(fila, shift=LEFT * 0.12), run_time=0.6)
    scene.play(FadeIn(ruta, shift=UP * 0.1), run_time=0.5)
    scene.next_slide()

    encabezado_comandos = hacer_titulo(TITULO_COMANDOS)
    sesion, glosas, nota = _comandos()
    carpeta = sesion[0][3]

    scene.play(
        FadeOut(lineas), FadeOut(atajos), FadeOut(ruta),
        FadeOut(encabezado_arbol),
        FadeIn(encabezado_comandos, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(sesion[0]), run_time=0.5)

    desde = 0
    for paso, (glosa, hasta, destino) in enumerate(PASOS):
        entradas = [
            FadeIn(fila, shift=RIGHT * 0.12) for fila in sesion[1][desde:hasta]
        ]
        if glosa is not None:
            entradas.append(FadeIn(glosas[glosa], shift=RIGHT * 0.12))
        scene.play(LaggedStart(*entradas, lag_ratio=0.6),
                   run_time=0.45 * len(entradas) + 0.3)
        if destino is not None:
            rotulo = texto(destino, TAM_SESION - 2,
                           color=PRIMARIO if destino != CARPETA else SECUNDARIO)
            scene.play(Transform(carpeta, rotulo.move_to(carpeta)),
                       run_time=0.5)
        desde = hasta
        if paso < len(PASOS) - 1:
            scene.next_slide()

    scene.play(FadeIn(nota), run_time=0.5)
    scene.wait(0.3)

    scene.next_slide()
