from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Flash,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    RoundedRectangle,
    Transform,
    VGroup,
)

from componentes import archivo, aspa, nodo_commit, puntero, texto, visto
from componentes import titulo as hacer_titulo
from estilo import (
    AMBAR,
    ERROR,
    OK,
    RAMA_MAIN,
    SECUNDARIO,
    STAGING,
    SUPERFICIE,
)

from .tres_zonas import X_CARRILES, carriles_zonas

TITULO = "git reset"

BAJADA_MAPA = 0.45
Y_CARRIL = -2.05
Y_FICHA = 0.0
Y_BAJADA = -1.2
Y_NUEVO = 0.27
Y_VIEJO = -1.07
RADIO = 0.3
Y_MARCA = -2.5
Y_ORDEN = -3.2

HASH_NUEVO = "9c1d"
HASH_VIEJO = "77ab"
ALTO_ARCHIVO = 0.46
TAM_FICHA = 13

RESETS = (
    ("--soft", SECUNDARIO, ("intacto", "intacto", "retrocede"), 1),
    ("--mixed", AMBAR, ("intacto", "vacia", "retrocede"), 0),
    ("--hard", ERROR, ("borra", "borra", "retrocede"), None),
)

COLUMNAS = (
    ("directorio de trabajo", -2.9, SECUNDARIO),
    ("staging", 0.65, STAGING),
    ("repositorio", 3.95, RAMA_MAIN),
)
X_BANDERA = -6.4
Y_CABECERA = 1.25
Y_PRIMERA = 0.3
PASO_FILA = 0.95
Y_TABLA = -0.45


def _marca(estado, x, y):
    if estado == "intacto":
        icono, etiqueta, color = visto(OK, tam=0.13), "intacto", OK
    elif estado == "vacia":
        icono, etiqueta, color = texto("↓", 20, color=STAGING), "se vacía", STAGING
    elif estado == "borra":
        icono, etiqueta, color = aspa(ERROR, tam=0.13), "se pierde", ERROR
    else:
        icono, etiqueta, color = texto("←", 20, color=RAMA_MAIN), "retrocede", RAMA_MAIN
    fila = VGroup(icono, texto(etiqueta, 14, color=color))
    return fila.arrange(RIGHT, buff=0.22).move_to([x, y, 0])


def _ficha(nombre, color, carril, y):
    contenido = VGroup(
        archivo(color=color, alto=ALTO_ARCHIVO),
        texto(nombre, TAM_FICHA, color=color),
    ).arrange(DOWN, buff=0.14)
    caja = RoundedRectangle(
        width=contenido.width + 0.5, height=contenido.height + 0.34,
        corner_radius=0.14, stroke_color=color, stroke_width=2.5,
    ).set_fill(SUPERFICIE, opacity=1.0)
    caja.move_to(contenido.get_center())
    return VGroup(caja, contenido).move_to([X_CARRILES[carril], y, 0])


def _historial():
    nuevo = nodo_commit(HASH_NUEVO, RAMA_MAIN, RADIO, 14)
    nuevo.move_to([X_CARRILES[2], Y_NUEVO, 0])
    viejo = nodo_commit(HASH_VIEJO, RAMA_MAIN, RADIO, 14)
    viejo.move_to([X_CARRILES[2], Y_VIEJO, 0])
    punteros = VGroup(
        puntero("HEAD", OK, 13), puntero("main", RAMA_MAIN, 13),
    ).arrange(DOWN, buff=0.12).next_to(nuevo, RIGHT, buff=0.28)
    return nuevo, viejo, punteros


def _partida():
    return VGroup(
        _ficha("sin añadir", ERROR, 0, Y_FICHA),
        _ficha("añadido", STAGING, 1, Y_FICHA),
    )


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    pistas = carriles_zonas().shift(DOWN * BAJADA_MAPA)
    for pista, x in zip(pistas, X_CARRILES):
        pista[2].put_start_and_end_on(pista[2].get_start(), [x, Y_CARRIL, 0])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[FadeIn(pista[0], shift=DOWN * 0.15) for pista in pistas],
                    lag_ratio=0.25),
        run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeIn(pista[1]) for pista in pistas], lag_ratio=0.25),
        *[Create(pista[2]) for pista in pistas],
        run_time=0.9,
    )

    nuevo, viejo, punteros = _historial()
    fichas = _partida()
    scene.play(
        LaggedStart(GrowFromCenter(viejo), GrowFromCenter(nuevo),
                    lag_ratio=0.4),
        run_time=0.9,
    )
    scene.play(FadeIn(punteros, shift=LEFT * 0.15), run_time=0.5)
    scene.play(
        LaggedStart(*[GrowFromCenter(f) for f in fichas], lag_ratio=0.3),
        run_time=0.9,
    )
    scene.next_slide()

    for bandera, color, estados, destino in RESETS:
        orden = texto(f"git reset {bandera} HEAD~1", 20, color=color)
        orden.move_to([0, Y_ORDEN, 0])
        scene.play(FadeIn(orden, shift=UP * 0.1), run_time=0.45)

        marca_repo = _marca(estados[2], X_CARRILES[2], Y_MARCA)
        scene.play(
            punteros.animate.next_to(viejo, RIGHT, buff=0.28),
            nuevo.animate.set_opacity(0.28),
            FadeIn(marca_repo, shift=UP * 0.1),
            run_time=1.0,
        )

        marcas = VGroup(marca_repo)
        aspas = VGroup()
        for i, estado in enumerate(estados[:2]):
            marca = _marca(estado, X_CARRILES[i], Y_MARCA)
            if estado == "intacto":
                efecto = Indicate(fichas[i], color=OK, scale_factor=1.08)
            elif estado == "vacia":
                efecto = Transform(
                    fichas[i], _ficha("sin añadir", ERROR, 0, Y_BAJADA))
            else:
                cruz = aspa(ERROR, tam=0.34, grosor=7)
                cruz.move_to(fichas[i].get_center())
                aspas.add(cruz)
                efecto = LaggedStart(GrowFromCenter(cruz),
                                     fichas[i].animate.set_opacity(0.12),
                                     lag_ratio=0.4)
            scene.play(efecto, FadeIn(marca, shift=UP * 0.1), run_time=0.9)
            marcas.add(marca)

        if destino is not None:
            bulto = nodo_commit("", RAMA_MAIN, 0.15).move_to(nuevo.get_center())
            scene.add(bulto)
            scene.play(
                bulto.animate.move_to(fichas[destino].get_center()),
                run_time=0.8,
            )
            scene.play(
                FadeOut(bulto, scale=0.3),
                Flash(fichas[destino], color=color, line_length=0.16,
                      num_lines=12, flash_radius=0.75),
                run_time=0.5,
            )

        scene.next_slide()

        scene.play(
            FadeOut(orden), FadeOut(marcas), FadeOut(aspas),
            Transform(fichas, _partida()),
            punteros.animate.next_to(nuevo, RIGHT, buff=0.28),
            nuevo.animate.set_opacity(1.0),
            run_time=0.7,
        )

    cabeceras = VGroup(*[
        texto(nombre, 16, color=color).move_to([x, Y_CABECERA, 0])
        for nombre, x, color in COLUMNAS
    ])
    raya = Line([X_BANDERA - 0.2, Y_CABECERA - 0.4, 0],
                [4.95, Y_CABECERA - 0.4, 0],
                color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.4)

    filas = VGroup()
    for i, (bandera, color, estados, _destino) in enumerate(RESETS):
        y = Y_PRIMERA - i * PASO_FILA
        nombre = texto(f"git reset {bandera}", 17, color=color)
        nombre.move_to([X_BANDERA, y, 0], LEFT)
        marcas = VGroup(*[
            _marca(estado, x, y)
            for estado, (_, x, _c) in zip(estados, COLUMNAS)
        ])
        filas.add(VGroup(nombre, marcas))

    VGroup(cabeceras, raya, filas).move_to([0, Y_TABLA, 0])

    scene.play(
        FadeOut(pistas), FadeOut(nuevo), FadeOut(viejo),
        FadeOut(punteros), FadeOut(fichas),
        run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cabeceras],
                    lag_ratio=0.25),
        Create(raya), run_time=1.0,
    )
    for fila in filas:
        scene.play(FadeIn(fila[0], shift=RIGHT * 0.15), run_time=0.4)
        scene.play(
            LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in fila[1]],
                        lag_ratio=0.25),
            run_time=0.7,
        )
    scene.play(Indicate(filas[2][0], color=ERROR, scale_factor=1.12),
               run_time=0.6)
    scene.wait(0.3)

    scene.next_slide()
