from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Create,
    FadeIn,
    Flash,
    GrowFromCenter,
    Square,
    VGroup,
)

from animaciones import pulso
from componentes import (
    arista,
    logo_esquina,
    nodo_commit,
    puntero,
    separador,
    texto,
)
from estilo import (
    CLARO,
    FONT_TITULO,
    PRIMARIO,
    RAMA_FEATURE,
    RAMA_MAIN,
    SECUNDARIO,
)

ANTETITULO = "Introducción a"
TITULO = "GIT Y GITHUB"
SUBTITULO = "Control de versiones y trabajo en equipo"
FIRMA = "Semillero de Data Science e IA"

TAM_TITULO_PORTADA = 46
ANCHO_MAX = 10.6
ECO = RIGHT * 0.09 + DOWN * 0.09

COL = (-4.4, -2.64, -0.88, 0.88, 2.64, 4.4)
Y_MAIN = -1.5
Y_FEATURE = -0.4
R = 0.3

Y_REGLA_PIE = -3.0


def _ajustar(mob, ancho=ANCHO_MAX):
    if mob.width > ancho:
        mob.scale(ancho / mob.width)
    return mob


def _regla_rombo(largo=1.9):
    rombo = Square(side_length=0.14, stroke_width=0)
    rombo.set_fill(PRIMARIO, opacity=1).rotate(PI / 4)
    return VGroup(
        separador(largo=largo, grosor=2),
        rombo,
        separador(largo=largo, grosor=2),
    ).arrange(RIGHT, buff=0.24)


def _cabecera():
    antetitulo = texto(ANTETITULO, 22, color=SECUNDARIO)
    titulo = _ajustar(texto(TITULO, TAM_TITULO_PORTADA, color=CLARO,
                            font=FONT_TITULO))
    eco = titulo.copy().set_color(PRIMARIO).set_opacity(0.45).shift(ECO)
    cabeza = VGroup(antetitulo, VGroup(eco, titulo))
    cabeza.arrange(DOWN, buff=0.18)

    filete = _regla_rombo()
    subtitulo = _ajustar(texto(SUBTITULO, 18, color=SECUNDARIO))

    bloque = VGroup(cabeza, filete, subtitulo)
    bloque.arrange(DOWN, buff=0.34).to_edge(UP, buff=0.75)
    return antetitulo, titulo, eco, filete, subtitulo


def _pie_de_cartel():
    logo = logo_esquina()
    firma = texto(FIRMA, 15, color=SECUNDARIO)
    firma.to_edge(LEFT, buff=0.75).set_y(logo.get_center()[1])

    izq, der = firma.get_left()[0], logo.get_right()[0]
    regla = separador(largo=(der - izq) / 2, grosor=2).set_opacity(0.3)
    regla.move_to([(izq + der) / 2, Y_REGLA_PIE, 0])
    return regla, firma, logo


def _historial(scene):
    a = nodo_commit("a1", RAMA_MAIN, R).move_to([COL[0], Y_MAIN, 0])
    b = nodo_commit("b2", RAMA_MAIN, R).move_to([COL[1], Y_MAIN, 0])
    d = nodo_commit("d4", RAMA_MAIN, R).move_to([COL[4], Y_MAIN, 0])
    m = nodo_commit("m5", RAMA_MAIN, R).move_to([COL[5], Y_MAIN, 0])
    f1 = nodo_commit("f1", RAMA_FEATURE, R).move_to([COL[2], Y_FEATURE, 0])
    f2 = nodo_commit("f2", RAMA_FEATURE, R).move_to([COL[3], Y_FEATURE, 0])

    ab = arista(a, b, RAMA_MAIN, R)
    bd = arista(b, d, RAMA_MAIN, R)
    dm = arista(d, m, RAMA_MAIN, R)
    salida = arista(b, f1, RAMA_FEATURE, R)
    f1f2 = arista(f1, f2, RAMA_FEATURE, R)
    vuelta = arista(f2, m, RAMA_FEATURE, R)

    p_feature = puntero("feature", RAMA_FEATURE, 15)
    p_feature.next_to(f2, UP, buff=0.24)
    p_main = puntero("main", RAMA_MAIN, 15).next_to(m, DOWN, buff=0.24)

    scene.play(GrowFromCenter(a), run_time=0.4)
    scene.play(Create(ab), run_time=0.3)
    scene.play(GrowFromCenter(b), run_time=0.4)

    scene.play(Create(salida), run_time=0.5)
    scene.play(GrowFromCenter(f1), run_time=0.35)
    scene.play(Create(f1f2), run_time=0.3)
    scene.play(GrowFromCenter(f2), run_time=0.35)
    scene.play(FadeIn(p_feature, shift=DOWN * 0.12), run_time=0.35)

    scene.play(Create(bd), run_time=0.5)
    scene.play(GrowFromCenter(d), run_time=0.35)

    scene.play(Create(dm), Create(vuelta), run_time=0.6)
    scene.play(
        GrowFromCenter(m),
        Flash(m, color=RAMA_MAIN, line_length=0.22, num_lines=14,
              flash_radius=R + 0.35),
        run_time=0.6,
    )
    scene.play(FadeIn(p_main, shift=UP * 0.12), run_time=0.35)

    scene.play(
        pulso(ab, CLARO, 0.5), pulso(salida, CLARO, 0.6),
        pulso(f1f2, CLARO, 0.5), pulso(bd, CLARO, 0.9),
        pulso(vuelta, CLARO, 0.6), pulso(dm, CLARO, 0.5),
        run_time=1.1,
    )


def construir(scene):
    antetitulo, titulo, eco, filete, subtitulo = _cabecera()
    regla_pie, firma, logo = _pie_de_cartel()

    scene.play(FadeIn(antetitulo, shift=DOWN * 0.1), run_time=0.4)
    eco.shift(-ECO)
    scene.play(FadeIn(eco, scale=1.05), FadeIn(titulo, scale=1.05),
               run_time=0.6)
    scene.play(eco.animate.shift(ECO), run_time=0.3)

    scene.play(
        Create(filete[0]), GrowFromCenter(filete[1]), Create(filete[2]),
        run_time=0.45,
    )
    scene.play(FadeIn(subtitulo, shift=UP * 0.1), run_time=0.45)

    _historial(scene)

    scene.play(Create(regla_pie), run_time=0.5)
    scene.play(FadeIn(firma, shift=UP * 0.08), FadeIn(logo), run_time=0.5)
    scene.wait(0.6)
    scene.next_slide()
