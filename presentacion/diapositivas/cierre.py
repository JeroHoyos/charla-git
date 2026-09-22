import numpy as np
from manim import (
    DOWN,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Create,
    FadeIn,
    Group,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    RoundedRectangle,
    ShowPassingFlash,
    Succession,
    VGroup,
    there_and_back,
)

from animaciones import pulso
from componentes import (
    arista,
    cajon,
    carpeta,
    discos,
    imagen,
    nodo_commit,
    puntero,
    texto,
)
from estilo import (
    BLANCO,
    CLARO,
    FONT_TITULO,
    OK,
    PRIMARIO,
    RAMA_FEATURE,
    RAMA_MAIN,
    SECUNDARIO,
    STAGING,
    SUPERFICIE,
)

Y_GRACIAS = 3.18
TAM_GRACIAS = 48
ANCHO_MAX_GRACIAS = 10.4

COL = (-6.15, -4.9, -3.65, -2.4, -1.15, 0.1)
Y_MAIN = 0.15
Y_FEATURE = 1.35
R = 0.26
BUFF_PUNTERO = 0.24

X_QR = 4.25
Y_TARJETA = 0.55
LADO_TARJETA = 2.9
MARGEN_QR = 0.3
Y_PIE_QR = -1.35

Y_TIRA = -2.55
ANCHO_PAPEL, ALTO_PAPEL = 2.6, 1.30
BUFF_PAPEL = 0.32
ALTO_ICONO = 0.44
RADIO_MINI = 0.14

Y_FIRMA = -3.62


def _historial():
    a = nodo_commit(color=RAMA_MAIN, radio=R).move_to([COL[0], Y_MAIN, 0])
    b = nodo_commit(color=RAMA_MAIN, radio=R).move_to([COL[1], Y_MAIN, 0])
    d = nodo_commit(color=RAMA_MAIN, radio=R).move_to([COL[4], Y_MAIN, 0])
    m = nodo_commit(color=RAMA_MAIN, radio=R).move_to([COL[5], Y_MAIN, 0])
    f1 = nodo_commit(color=RAMA_FEATURE, radio=R).move_to([COL[2], Y_FEATURE, 0])
    f2 = nodo_commit(color=RAMA_FEATURE, radio=R).move_to([COL[3], Y_FEATURE, 0])

    ab = arista(a, b, RAMA_MAIN, R)
    bd = arista(b, d, RAMA_MAIN, R)
    dm = arista(d, m, RAMA_MAIN, R)
    salida = arista(b, f1, RAMA_FEATURE, R)
    f1f2 = arista(f1, f2, RAMA_FEATURE, R)
    vuelta = arista(f2, m, RAMA_FEATURE, R)

    p_main = puntero("main", RAMA_MAIN, 13).next_to(m, DOWN, buff=BUFF_PUNTERO)
    p_rama = puntero("feature", RAMA_FEATURE, 13)
    p_rama.next_to(f2, UP, buff=BUFF_PUNTERO)

    nodos = VGroup(a, b, f1, f2, d, m)
    hilos = VGroup(ab, salida, f1f2, bd, vuelta, dm)
    return nodos, hilos, VGroup(p_main, p_rama), m


def _desemboque(ultimo):
    borde = X_QR - LADO_TARJETA / 2
    tramo = (ultimo.get_center() + RIGHT * (R + 0.12),
             np.array([borde - 0.12, Y_MAIN, 0.0]))
    flecha = Arrow(
        *tramo, color=PRIMARIO, stroke_width=4, buff=0.0,
        max_tip_length_to_length_ratio=0.11,
    )
    return flecha, Line(*tramo)


def _crece(mob):
    mob.crece = True
    return mob


def _mini(x, y, color):
    return _crece(nodo_commit(color=color, radio=RADIO_MINI).move_to([x, y, 0]))


def _boceto_zonas():
    iconos = VGroup(
        carpeta(ALTO_ICONO, SECUNDARIO),
        cajon(ALTO_ICONO, STAGING),
        discos(ALTO_ICONO, RAMA_MAIN),
    ).arrange(RIGHT, buff=0.30)
    for icono in iconos:
        _crece(icono)
    return iconos


def _boceto_cadena():
    nodos = [_mini(x, 0, RAMA_MAIN) for x in (-0.72, 0.0, 0.72)]
    return VGroup(
        nodos[0], arista(nodos[0], nodos[1], RAMA_MAIN, RADIO_MINI),
        nodos[1], arista(nodos[1], nodos[2], RAMA_MAIN, RADIO_MINI),
        nodos[2],
    )


def _boceto_rama():
    a = _mini(-0.82, -0.22, RAMA_MAIN)
    m = _mini(0.82, -0.22, RAMA_MAIN)
    f = _mini(0.0, 0.30, RAMA_FEATURE)
    return VGroup(
        a, arista(a, m, RAMA_MAIN, RADIO_MINI), m,
        arista(a, f, RAMA_FEATURE, RADIO_MINI), f,
        arista(f, m, RAMA_FEATURE, RADIO_MINI),
    )


def _cajita(x, color):
    return _crece(RoundedRectangle(
        width=0.86, height=0.52, corner_radius=0.1,
        stroke_color=color, stroke_width=2.6,
    ).set_fill(SUPERFICIE, opacity=1.0).move_to([x, 0, 0]))


def _boceto_remoto():
    aqui, alla = _cajita(-0.85, OK), _cajita(0.85, PRIMARIO)
    ida = Arrow([-0.36, 0.14, 0], [0.36, 0.14, 0], color=OK, buff=0,
                stroke_width=2.6, max_tip_length_to_length_ratio=0.22)
    vuelta = Arrow([0.36, -0.14, 0], [-0.36, -0.14, 0], color=PRIMARIO, buff=0,
                   stroke_width=2.6, max_tip_length_to_length_ratio=0.22)
    return VGroup(aqui, alla, ida, vuelta)


def _vive_zonas(boceto):
    return LaggedStart(*[
        Indicate(icono, color=color, scale_factor=1.14)
        for icono, color in zip(boceto, (SECUNDARIO, STAGING, RAMA_MAIN))
    ], lag_ratio=0.45)


def _vive_cadena(boceto):
    return LaggedStart(*[
        pulso(boceto[i], CLARO, run_time=0.55, ancho=5) for i in (1, 3)
    ], lag_ratio=0.5)


def _vive_rama(boceto):
    return LaggedStart(
        pulso(boceto[3], RAMA_FEATURE, run_time=0.6, ancho=5),
        pulso(boceto[5], RAMA_FEATURE, run_time=0.6, ancho=5),
        Indicate(boceto[2], color=RAMA_MAIN, scale_factor=1.25),
        lag_ratio=0.45,
    )


def _vive_remoto(boceto):
    _, _, ida, vuelta = boceto
    return Succession(
        pulso(ida, OK, run_time=0.55, ancho=5),
        pulso(vuelta, PRIMARIO, run_time=0.55, ancho=5),
    )


REPASO = (
    (_boceto_zonas, _vive_zonas),
    (_boceto_cadena, _vive_cadena),
    (_boceto_rama, _vive_rama),
    (_boceto_remoto, _vive_remoto),
)


def _dibujarse(boceto, lag=0.3):
    return LaggedStart(*[
        GrowFromCenter(pieza) if getattr(pieza, "crece", False) else Create(pieza)
        for pieza in boceto
    ], lag_ratio=lag)


def _papel(dibujar):
    fondo = RoundedRectangle(
        width=ANCHO_PAPEL, height=ALTO_PAPEL, corner_radius=0.14,
        stroke_color=SECUNDARIO, stroke_width=1.6,
    ).set_fill(CLARO, opacity=0.03)
    fondo.set_stroke(opacity=0.3)
    return VGroup(fondo, dibujar().move_to(fondo.get_center()))


def construir(scene):
    gracias = VGroup(
        texto("MUCHAS", TAM_GRACIAS, color=CLARO, font=FONT_TITULO),
        texto("GRACIAS", TAM_GRACIAS, color=PRIMARIO, font=FONT_TITULO),
    ).arrange(RIGHT, buff=0.5)
    if gracias.width > ANCHO_MAX_GRACIAS:
        gracias.scale(ANCHO_MAX_GRACIAS / gracias.width)
    gracias.move_to([0, Y_GRACIAS, 0])

    nodos, hilos, punteros, ultimo = _historial()
    salida, riel = _desemboque(ultimo)

    papel_qr = RoundedRectangle(
        width=LADO_TARJETA, height=LADO_TARJETA, corner_radius=0.2,
        stroke_color=PRIMARIO, stroke_width=3,
    ).set_fill(BLANCO, opacity=1.0).move_to([X_QR, Y_TARJETA, 0])
    codigo = imagen("qr_formulario")
    codigo.scale_to_fit_width(LADO_TARJETA - MARGEN_QR * 2)
    codigo.move_to(papel_qr.get_center())
    tarjeta = Group(papel_qr, codigo)

    pie_qr = VGroup(
        texto("Escanea el código", 15, color=CLARO),
        texto("Asistencia y material de la charla", 14, color=SECUNDARIO),
    ).arrange(DOWN, buff=0.12).move_to([X_QR, Y_PIE_QR, 0])

    tira = VGroup(*[_papel(dibujar) for dibujar, _ in REPASO])
    tira.arrange(RIGHT, buff=BUFF_PAPEL).move_to([0, Y_TIRA, 0])

    firma = texto("Semillero de Data Science e IA  ·  Aperture", 15,
                  color=SECUNDARIO).move_to([0, Y_FIRMA, 0])

    scene.play(FadeIn(gracias[0], shift=UP * 0.18), run_time=0.5)
    scene.play(FadeIn(gracias[1], shift=UP * 0.18), run_time=0.5)

    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in nodos], lag_ratio=0.3),
        run_time=1.1,
    )
    scene.play(
        LaggedStart(*[Create(h) for h in hilos], lag_ratio=0.25),
        run_time=1.1,
    )
    scene.play(FadeIn(punteros, shift=UP * 0.1), run_time=0.45)

    scene.play(
        LaggedStart(*[pulso(h, CLARO, run_time=0.7, ancho=7) for h in hilos],
                    lag_ratio=0.3),
        run_time=1.6,
    )
    scene.play(Create(salida), run_time=0.45)
    scene.play(
        LaggedStart(GrowFromCenter(papel_qr), FadeIn(codigo, scale=0.85),
                    lag_ratio=0.55),
        run_time=0.95,
    )
    scene.play(FadeIn(pie_qr, shift=UP * 0.1), run_time=0.4)

    scene.play(
        LaggedStart(*[
            Succession(FadeIn(fondo, shift=UP * 0.18), _dibujarse(boceto))
            for fondo, boceto in tira
        ], lag_ratio=0.42),
        run_time=2.8,
    )
    scene.play(FadeIn(firma, shift=UP * 0.1), run_time=0.4)

    if hasattr(scene, "_base_slide_config"):
        scene._base_slide_config.auto_next = True
    scene.next_slide(loop=True, indicador=False)
    scene.play(
        LaggedStart(
            *[pulso(h, CLARO, run_time=0.7, ancho=7) for h in hilos],
            AnimationGroup(
                ShowPassingFlash(riel.copy().set_stroke(PRIMARIO, 5.0, 1.0),
                                 time_width=0.4),
                tarjeta.animate(rate_func=there_and_back).scale(1.045),
                lag_ratio=0.55,
            ),
            lag_ratio=0.3,
        ),
        LaggedStart(*[
            vivir(papel[1]) for (_, vivir), papel in zip(REPASO, tira)
        ], lag_ratio=0.22),
        run_time=2.6,
    )

    scene.next_slide(indicador=False)
