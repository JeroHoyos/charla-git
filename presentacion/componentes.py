import os

import numpy as np
from manim import (
    DOWN,
    DR,
    LEFT,
    NORMAL,
    ORIGIN,
    RIGHT,
    UP,
    Circle,
    CubicBezier,
    DashedVMobject,
    Dot,
    Ellipse,
    Group,
    ImageMobject,
    Line,
    ManimColor,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
    VMobject,
    config,
)
from PIL import Image, ImageDraw, ImageOps

from estilo import (
    AMBAR,
    ASSETS,
    BLANCO,
    CLARO,
    ERROR,
    FONDO,
    FONT,
    OK,
    PRIMARIO,
    RAMA_FEATURE,
    RAMA_MAIN,
    SECUNDARIO,
    STAGING,
    SUPERFICIE,
    TAM_TITULO,
    VERDE,
)
from estilo import FONT_TITULO


def marco():
    return Rectangle(
        width=config.frame_width - 0.22,
        height=config.frame_height - 0.22,
        stroke_color=PRIMARIO,
        stroke_width=8,
        fill_opacity=0,
    )


PRESETS_GRAFO = (
    (9, 1.6, 2, 7, SECUNDARIO, 0.16),
    (12, -1.9, 3, 13, PRIMARIO, 0.13),
    (7, 2.2, 2, 21, SECUNDARIO, 0.18),
    (14, -1.4, 3, 34, SECUNDARIO, 0.11),
    (10, 1.1, 2, 55, PRIMARIO, 0.15),
)


def grafo_decorativo(indice=0):
    n, y0, n_ramas, semilla, color, op = PRESETS_GRAFO[indice % len(PRESETS_GRAFO)]
    rng = np.random.default_rng(semilla)
    w = config.frame_width / 2 - 0.25
    xs = np.linspace(-w, w, n)
    grupo = VGroup()

    tronco = Line([xs[0], y0, 0], [xs[-1], y0, 0],
                  color=color, stroke_width=1.2, stroke_opacity=op)
    grupo.add(tronco)
    for x in xs:
        grupo.add(Dot([x, y0, 0], radius=0.05, color=color, fill_opacity=op * 2.0))

    for _ in range(n_ramas):
        i = int(rng.integers(0, n - 3))
        j = min(i + int(rng.integers(2, 4)), n - 1)
        dy = float(rng.choice([-1.0, 1.0])) * float(rng.uniform(0.85, 1.7))
        salida, entrada = np.array([xs[i], y0, 0]), np.array([xs[j], y0, 0])
        cima = (salida + entrada) / 2 + np.array([0, dy, 0])
        curva = VMobject(color=color, stroke_width=1.2)
        curva.set_points_smoothly([salida, cima, entrada])
        curva.set_stroke(opacity=op)
        grupo.add(curva)
        for t in (0.35, 0.65):
            grupo.add(Dot(curva.point_from_proportion(t), radius=0.045,
                          color=color, fill_opacity=op * 2.0))
    return grupo


_EXTENSIONES = (".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".bmp")


def ruta_asset(nombre):
    if not nombre.lower().endswith(_EXTENSIONES):
        nombre = f"{nombre}.png"
    return os.path.join(ASSETS, nombre)


def imagen(nombre, escala=1.0):
    return ImageMobject(ruta_asset(nombre)).scale(escala)


def imagen_circular(nombre, diametro=3.2, relleno=BLANCO, ocupacion=0.86):
    original = Image.open(ruta_asset(nombre)).convert("RGBA")

    lado = max(original.size)
    foto = ImageOps.contain(
        original, (int(lado * ocupacion),) * 2, Image.LANCZOS
    )
    disco = Image.new("RGBA", (lado, lado), (*ManimColor(relleno).to_int_rgb(), 255))
    disco.alpha_composite(
        foto, ((lado - foto.width) // 2, (lado - foto.height) // 2)
    )

    mascara = Image.new("L", (lado * 4, lado * 4), 0)
    ImageDraw.Draw(mascara).ellipse((0, 0, lado * 4 - 1, lado * 4 - 1), fill=255)
    disco.putalpha(mascara.resize((lado, lado), Image.LANCZOS))

    mob = ImageMobject(np.array(disco)).scale_to_fit_width(diametro)
    mob.receta_circular = (nombre, diametro, relleno, ocupacion)
    return mob


def imagen_recortada(nombre, ancho=2.0, radio=0.1):
    original = Image.open(ruta_asset(nombre)).convert("RGBA")
    w, h = original.size

    mascara = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(mascara).rounded_rectangle(
        (0, 0, w * 4 - 1, h * 4 - 1), radius=int(min(w, h) * 4 * radio), fill=255,
    )
    original.putalpha(mascara.resize((w, h), Image.LANCZOS))

    mob = ImageMobject(np.array(original)).scale_to_fit_width(ancho)
    mob.receta_recorte = (nombre, ancho, radio)
    return mob


def fotografia(nombre, ancho=3.0, pie=None, giro=-0.045):
    foto = imagen(nombre).scale_to_fit_width(ancho)
    margen = ancho * 0.055
    margen_pie = ancho * 0.2 if pie else margen
    papel = RoundedRectangle(
        width=ancho + 2 * margen,
        height=foto.height + margen + margen_pie,
        corner_radius=0.06, stroke_width=0,
    ).set_fill(BLANCO, opacity=1.0)

    foto.move_to(papel.get_top() + DOWN * (margen + foto.height / 2))
    grupo = Group(papel, foto)
    if pie:
        rotulo = texto(pie, ancho * 5.6, color=FONDO)
        rotulo.move_to(papel.get_bottom() + UP * margen_pie / 2)
        grupo.add(rotulo)
    return grupo.rotate(giro)


def logo_esquina(ancho=0.8, buff=0.3):
    logo = imagen("aperture-eye-cyan")
    return logo.scale_to_fit_width(ancho).to_corner(DR, buff=buff)


def texto(contenido, tam, color=CLARO, weight=NORMAL, font=FONT, t2c=None):
    return Text(contenido, font=font, font_size=tam, color=color, weight=weight,
                t2c=t2c or {})


def parrafo(lineas, buff=0.15, alinear=ORIGIN):
    textos = [texto(*linea) for linea in lineas]
    return VGroup(*textos).arrange(DOWN, buff=buff, aligned_edge=alinear)


def titulo(contenido):
    t = texto(contenido, TAM_TITULO, color=PRIMARIO, font=FONT_TITULO)
    ancho_max = config.frame_width - 1.8
    if t.width > ancho_max:
        t.scale(ancho_max / t.width)
    return t.to_edge(UP, buff=0.6)


def vinetas(textos, tam=26, buff=0.45, color=PRIMARIO):
    filas = VGroup()
    for contenido in textos:
        punto = Dot(radius=0.07, color=color)
        filas.add(VGroup(punto, texto(contenido, tam)).arrange(RIGHT, buff=0.25))
    return filas.arrange(DOWN, buff=buff, aligned_edge=LEFT)


def tarjeta(lineas, ancho_extra=0.7, alto_extra=0.4, color=PRIMARIO):
    textos = VGroup(*[
        texto(t, fs, color=FONDO, weight=w) for t, fs, w in lineas
    ]).arrange(DOWN, buff=0.1)
    fondo = RoundedRectangle(
        corner_radius=0.14,
        width=textos.width + ancho_extra,
        height=textos.height + alto_extra,
        fill_color=color,
        fill_opacity=1.0,
        stroke_width=0,
    )
    return VGroup(fondo, textos)


def burbuja(autor, mensaje, color=SECUNDARIO, tam=16, adjunto=False,
            cola=None):
    quien = texto(autor, 13, color=color)
    cuerpo = texto(mensaje, tam, color=CLARO)
    if adjunto:
        cuerpo = VGroup(
            archivo(color=color, alto=0.32), cuerpo,
        ).arrange(RIGHT, buff=0.18)
    dentro = VGroup(quien, cuerpo).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    globo = RoundedRectangle(
        width=dentro.width + 0.5, height=dentro.height + 0.32,
        corner_radius=0.18, stroke_color=color, stroke_width=2.5,
    ).set_fill(SUPERFICIE, opacity=1.0)

    piezas = [globo]
    if cola is not None:
        fuera = -1.0 if cola[0] < 0 else 1.0
        x = globo.get_left()[0] if fuera < 0 else globo.get_right()[0]
        y = globo.get_bottom()[1]
        arriba, abajo = y + 0.38, y + 0.15
        punta = np.array([x + fuera * 0.16, y + 0.04, 0])
        dentro_x = x - fuera * 0.05
        piezas.append(Polygon(
            np.array([dentro_x, arriba, 0]), punta,
            np.array([dentro_x, abajo, 0]), stroke_width=0,
        ).set_fill(SUPERFICIE, opacity=1.0))
        borde = VMobject(color=color, stroke_width=2.5)
        borde.set_points_as_corners([
            np.array([x, arriba, 0]), punta, np.array([x, abajo, 0]),
        ])
        piezas.append(borde)

    piezas.append(dentro.move_to(globo.get_center()))
    return VGroup(*piezas)


def avatar(inicial, nombre=None, radio=0.5, color=SECUNDARIO):
    circulo = Circle(radius=radio, color=color, stroke_width=2.5)
    circulo.set_fill(SUPERFICIE, opacity=1.0)
    cara = VGroup(circulo, texto(inicial, radio * 50).move_to(circulo))
    if nombre is None:
        return cara
    return VGroup(cara, texto(nombre, radio * 33, color=color)).arrange(
        DOWN, buff=radio * 0.38)


def globo_mudo(ancho, alto=0.32, color=SECUNDARIO):
    return RoundedRectangle(
        width=ancho, height=alto, corner_radius=min(0.16, alto / 2),
        stroke_color=color, stroke_width=1.5,
    ).set_fill(SUPERFICIE, opacity=1.0).set_stroke(opacity=0.55)


def telefono(ancho=4.1, alto=6.0, color=SECUNDARIO, rotulo=None, sub=None,
             hora="9:41"):
    radio = ancho * 0.12
    borde = 0.13
    cuerpo = RoundedRectangle(
        width=ancho, height=alto, corner_radius=radio,
        stroke_color=color, stroke_width=4,
    ).set_fill(FONDO, opacity=1.0)
    pantalla = RoundedRectangle(
        width=ancho - 2 * borde, height=alto - 2 * borde,
        corner_radius=radio - borde, stroke_width=0,
    ).set_fill(SUPERFICIE, opacity=0.6)

    arriba, abajo = pantalla.get_top()[1], pantalla.get_bottom()[1]
    izq, der = pantalla.get_left()[0], pantalla.get_right()[0]
    y_estado = arriba - 0.26

    isla = RoundedRectangle(
        width=ancho * 0.2, height=0.12, corner_radius=0.06, stroke_width=0,
    ).set_fill(FONDO, opacity=1.0).move_to([0, y_estado, 0])
    reloj = texto(hora, 11, color=color).move_to([izq + 0.36, y_estado, 0])
    pila = RoundedRectangle(width=0.3, height=0.15, corner_radius=0.05,
                            stroke_color=color, stroke_width=1.5)
    carga = RoundedRectangle(width=0.19, height=0.08, corner_radius=0.025,
                             stroke_width=0).set_fill(color, opacity=0.75)
    carga.align_to(pila, LEFT).shift(RIGHT * 0.045)
    pico = Line(UP * 0.03, DOWN * 0.03, color=color, stroke_width=2)
    pico.next_to(pila, RIGHT, buff=0.02)
    bateria = VGroup(pila, carga, pico).move_to([der - 0.4, y_estado, 0])
    adornos = VGroup(isla, reloj, bateria)

    if rotulo:
        avatar = Dot(radius=0.12, color=color).set_fill(color, opacity=0.35)
        nombre = VGroup(texto(rotulo, 13, color=CLARO))
        if sub:
            nombre.add(texto(sub, 10, color=color))
        nombre.arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        cabecera = VGroup(avatar, nombre).arrange(RIGHT, buff=0.16)
        adornos.add(cabecera.move_to([0, arriba - 0.8, 0]))

    y_division = arriba - 1.12
    adornos.add(Line([izq, y_division, 0], [der, y_division, 0],
                     color=color, stroke_width=1.5).set_stroke(opacity=0.4))
    adornos.add(RoundedRectangle(
        width=ancho * 0.32, height=0.07, corner_radius=0.035, stroke_width=0,
    ).set_fill(color, opacity=0.5).move_to([0, abajo + 0.22, 0]))

    techo, suelo = y_division - 0.18, abajo + 0.45
    lienzo = Rectangle(width=der - izq - 0.24, height=techo - suelo,
                       stroke_width=0, fill_opacity=0)
    lienzo.move_to([0, (techo + suelo) / 2, 0])

    return VGroup(VGroup(cuerpo, pantalla, adornos), lienzo)


def barra(largo, alto=0.42, color=PRIMARIO, opacidad=1.0):
    largo = max(largo, 0.03)
    return RoundedRectangle(
        width=largo, height=alto, corner_radius=min(0.09, largo / 2),
        stroke_width=0,
    ).set_fill(color, opacity=opacidad)


_COLOR_TIPO = {
    "cmd": CLARO,
    "out": SECUNDARIO,
    "txt": CLARO,
    "ok": OK,
    "err": ERROR,
    "avi": AMBAR,
    "alt": RAMA_FEATURE,
    "com": SECUNDARIO,
}


def linea_terminal(contenido, tipo="cmd", tam=17):
    if tipo == "sep":
        hueco = Rectangle(width=0.01, height=tam * 0.011,
                          stroke_width=0, fill_opacity=0)
        hueco.es_separador = True
        return hueco

    color = _COLOR_TIPO.get(tipo, CLARO)
    if tipo == "com":
        contenido = f"# {contenido}"

    t2c = {}
    if tipo == "cmd":
        contenido = f"$ {contenido}"
        t2c["[0:1]"] = OK
        partes = contenido.split()
        if len(partes) > 1:
            largo = len(partes[1])
            if partes[1] in ("git", "gh") and len(partes) > 2:
                largo += 1 + len(partes[2])
            t2c[f"[2:{2 + largo}]"] = PRIMARIO

    linea = Text(contenido, font=FONT, font_size=tam, color=color, t2c=t2c)
    if tipo == "com":
        linea.set_opacity(0.7)
    return linea


ALTO_BARRA = 0.42


def ventana(ancho, alto, nombre=None, tam=15, barra=True, color=PRIMARIO):
    caja = RoundedRectangle(
        width=ancho, height=alto, corner_radius=0.16,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    chrome = VGroup(caja)
    if not barra:
        return chrome

    y_barra = caja.get_top()[1] - ALTO_BARRA
    division = Line(
        [caja.get_left()[0], y_barra, 0], [caja.get_right()[0], y_barra, 0],
        color=color, stroke_width=2,
    ).set_stroke(opacity=0.45)
    semaforo = VGroup(*[
        Dot(radius=0.055, color=c, fill_opacity=0.8)
        for c in (ERROR, AMBAR, VERDE)
    ]).arrange(RIGHT, buff=0.13)
    semaforo.move_to([caja.get_left()[0] + 0.42, y_barra + ALTO_BARRA / 2, 0])
    chrome.add(division, semaforo)
    if nombre:
        rotulo = texto(nombre, tam, color=SECUNDARIO)
        rotulo.move_to([caja.get_center()[0], y_barra + ALTO_BARRA / 2, 0])
        chrome.add(rotulo)
    return chrome


def terminal(lineas, tam=17, ancho=None, margen=0.55, buff=0.24, barra=True,
             nombre=None):
    filas = VGroup(*[
        linea_terminal(c, t, tam) for c, t in lineas
    ]).arrange(DOWN, buff=buff, aligned_edge=LEFT)

    ancho = ancho or filas.width + margen * 2
    alto_barra = ALTO_BARRA if barra else 0.0
    alto = filas.height + margen * 2 + alto_barra

    chrome = ventana(ancho, alto, nombre, tam - 2, barra)
    filas.move_to(chrome[0].get_center() + DOWN * alto_barra / 2)
    filas.align_to(chrome[0].get_left() + RIGHT * margen, LEFT)
    return VGroup(chrome, filas)


def nodo_commit(etiqueta="", color=PRIMARIO, radio=0.32, tam=15):
    circulo = Circle(radius=radio, color=color, stroke_width=4)
    circulo.set_fill(SUPERFICIE, opacity=1.0)
    if not etiqueta:
        return VGroup(circulo)
    letras = texto(etiqueta, tam, color=color)
    if letras.width > radio * 1.7:
        letras.scale_to_fit_width(radio * 1.7)
    return VGroup(circulo, letras.move_to(circulo.get_center()))


def nodo_fantasma(etiqueta="", color=ERROR, radio=0.32, tam=15):
    relleno = Circle(radius=radio, stroke_width=0)
    relleno.set_fill(SUPERFICIE, opacity=1.0)
    borde = DashedVMobject(
        Circle(radius=radio, color=color, stroke_width=4),
        num_dashes=22, dashed_ratio=0.55,
    )
    nodo = VGroup(relleno, borde)
    if not etiqueta:
        return nodo
    letras = texto(etiqueta, tam, color=color)
    if letras.width > radio * 1.7:
        letras.scale_to_fit_width(radio * 1.7)
    return nodo.add(letras.move_to(nodo.get_center()))


def enlace(inicio, fin, color=PRIMARIO, grosor=3.5):
    inicio, fin = np.array(inicio, dtype=float), np.array(fin, dtype=float)
    if abs(inicio[1] - fin[1]) < 0.01:
        return Line(inicio, fin, color=color, stroke_width=grosor)
    medio = (inicio[0] + fin[0]) / 2
    return CubicBezier(
        inicio,
        np.array([medio, inicio[1], 0]),
        np.array([medio, fin[1], 0]),
        fin,
        color=color, stroke_width=grosor,
    )


def arista(a, b, color=PRIMARIO, radio=0.32, grosor=3.5):
    return enlace(a.get_center() + RIGHT * radio,
                  b.get_center() + LEFT * radio, color, grosor)


def puntero(nombre, color=PRIMARIO, tam=16, relleno=0.16):
    letras = texto(nombre, tam, color=color)
    caja = RoundedRectangle(
        width=letras.width + 0.3, height=letras.height + 0.22,
        corner_radius=0.08, stroke_color=color, stroke_width=2.5,
    ).set_fill(color, opacity=relleno)
    return VGroup(caja, letras.move_to(caja.get_center()))


def archivo(nombre="", color=SECUNDARIO, alto=0.7, tam=14):
    ancho = alto * 0.78
    d = alto * 0.26
    hoja = Polygon(
        [-ancho / 2, alto / 2, 0], [ancho / 2 - d, alto / 2, 0],
        [ancho / 2, alto / 2 - d, 0], [ancho / 2, -alto / 2, 0],
        [-ancho / 2, -alto / 2, 0],
        color=color, stroke_width=3,
    ).set_fill(color, opacity=0.10)
    doblez = Polygon(
        [ancho / 2 - d, alto / 2, 0], [ancho / 2, alto / 2 - d, 0],
        [ancho / 2 - d, alto / 2 - d, 0],
        color=color, stroke_width=2.5,
    ).set_fill(color, opacity=0.25)
    icono = VGroup(hoja, doblez)
    if not nombre:
        return icono
    etiqueta = texto(nombre, tam, color=color).next_to(icono, DOWN, buff=0.14)
    return VGroup(icono, etiqueta)


ANCHO_PAPEL = 0.98
MARGEN_PAPEL = 0.055
PIE_PAPEL = 0.19
ALTO_IMAGEN = 0.66
ALTO_HOJA = 0.44
GIRO_PAPEL = -0.05


def foto_proyecto(escala=1.0, color=SECUNDARIO, vacia=False):
    ancho_imagen = ANCHO_PAPEL - 2 * MARGEN_PAPEL
    papel = RoundedRectangle(
        width=ANCHO_PAPEL,
        height=ALTO_IMAGEN + MARGEN_PAPEL + PIE_PAPEL,
        corner_radius=0.05, stroke_width=0,
    ).set_fill(BLANCO, opacity=1.0)
    imagen = RoundedRectangle(
        width=ancho_imagen, height=ALTO_IMAGEN, corner_radius=0.03,
        stroke_width=0,
    ).set_fill(SUPERFICIE, opacity=1.0)
    imagen.move_to(papel.get_top() + DOWN * (MARGEN_PAPEL + ALTO_IMAGEN / 2))

    hoja = archivo("", color, ALTO_HOJA)
    if vacia:
        hoja = DashedVMobject(
            hoja[0].set_fill(opacity=0), num_dashes=22, dashed_ratio=0.55,
        ).set_stroke(color, width=2.5, opacity=0.5)
    hoja.move_to(imagen.get_center())

    izq, der = imagen.get_left()[0], imagen.get_right()[0]
    arriba, abajo = imagen.get_top()[1], imagen.get_bottom()[1]
    brillo = Polygon(
        [izq, arriba, 0], [izq + ancho_imagen * 0.36, arriba, 0],
        [izq + ancho_imagen * 0.12, abajo, 0], [izq, abajo, 0],
        stroke_width=0,
    ).set_fill(BLANCO, opacity=0.07)

    pie = Line(
        [-ancho_imagen * 0.22, 0, 0], [ancho_imagen * 0.22, 0, 0],
        color=color, stroke_width=2.2,
    ).set_stroke(opacity=0.45)
    pie.move_to(papel.get_bottom() + UP * PIE_PAPEL / 2)

    return VGroup(papel, imagen, brillo, hoja, pie).rotate(GIRO_PAPEL).scale(
        escala)


def zona(nombre, color=PRIMARIO, ancho=3.4, alto=2.6, tam=17, discontinua=True):
    caja = RoundedRectangle(
        width=ancho, height=alto, corner_radius=0.18,
        stroke_color=color, stroke_width=3,
    ).set_fill(color, opacity=0.05)
    if discontinua:
        borde = DashedVMobject(
            caja.copy().set_fill(opacity=0), num_dashes=42, dashed_ratio=0.6,
        )
        caja = VGroup(caja.set_stroke(opacity=0), borde)
    rotulo = texto(nombre, tam, color=color).next_to(caja, UP, buff=0.18)
    return VGroup(caja, rotulo)


def carpeta(alto=0.9, color=SECUNDARIO):
    ancho = alto * 1.22
    tapa = Polygon(
        [-ancho / 2, -alto / 2, 0], [-ancho / 2, alto / 2, 0],
        [-ancho * 0.10, alto / 2, 0], [-ancho * 0.02, alto / 2 - alto * 0.18, 0],
        [ancho / 2, alto / 2 - alto * 0.18, 0], [ancho / 2, -alto / 2, 0],
        color=color, stroke_width=3,
    ).set_fill(color, opacity=0.06)
    frente = Polygon(
        [-ancho / 2, -alto / 2, 0], [ancho / 2, -alto / 2, 0],
        [ancho / 2, alto * 0.14, 0], [-ancho / 2, -alto * 0.02, 0],
        color=color, stroke_width=3,
    ).set_fill(color, opacity=0.16)
    return VGroup(tapa, frente)


def cajon(alto=0.9, color=STAGING):
    ancho = alto * 1.16
    caja = RoundedRectangle(
        width=ancho, height=alto * 0.9, corner_radius=alto * 0.1,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    lado = alto * 0.18
    piezas = VGroup(*[
        Rectangle(width=lado, height=lado, color=color, stroke_width=2)
        .set_fill(color, opacity=0.35)
        for _ in range(4)
    ]).arrange_in_grid(rows=2, buff=lado * 0.4)
    piezas.move_to(caja.get_center() + LEFT * ancho * 0.12)
    sello = VGroup(
        Circle(radius=alto * 0.2, color=color, stroke_width=3)
        .set_fill(SUPERFICIE, opacity=1.0),
        visto(color=color, tam=alto * 0.1, grosor=4),
    ).move_to(caja.get_corner(DR))
    return VGroup(caja, piezas, sello)


def discos(alto=0.9, color=RAMA_MAIN, n=3):
    ancho = alto * 1.02
    alto_disco = ancho * 0.34
    salto = (alto - alto_disco) / (n - 1)
    ys = [alto / 2 - alto_disco / 2 - i * salto for i in range(n)]
    paredes = VGroup(*[
        Line([lado * ancho / 2, ys[0], 0], [lado * ancho / 2, ys[-1], 0],
             color=color, stroke_width=3)
        for lado in (-1, 1)
    ])
    tapas = VGroup(*[
        Ellipse(width=ancho, height=alto_disco, color=color, stroke_width=3)
        .set_fill(SUPERFICIE, opacity=1.0).move_to([0, y, 0])
        for y in reversed(ys)
    ])
    return VGroup(paredes, tapas)


def carriles(zonas, xs, y_icono=2.25, y_rotulo=1.45, y_linea=(1.08, -3.15),
             tam=19, grosor=7):
    grupo = VGroup()
    for (icono, nombre, color), x in zip(zonas, xs):
        rotulo = texto(nombre, tam, color=color).move_to([x, y_rotulo, 0])
        linea = Line([x, y_linea[0], 0], [x, y_linea[1], 0],
                     color=color, stroke_width=grosor)
        grupo.add(VGroup(icono.move_to([x, y_icono, 0]), rotulo, linea))
    return grupo


def robot(alto=1.6, color=SECUNDARIO):
    u = alto / 8.0
    cabeza = RoundedRectangle(
        width=u * 4.4, height=u * 3.4, corner_radius=u * 0.7,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    ojos = VGroup(*[
        Dot(radius=u * 0.42, color=color) for _ in range(2)
    ]).arrange(RIGHT, buff=u * 1.3).move_to(cabeza)

    antena = Line(cabeza.get_top(), cabeza.get_top() + UP * u,
                  color=color, stroke_width=3)
    bombilla = Dot(antena.get_end(), radius=u * 0.42, color=color)

    cuerpo = RoundedRectangle(
        width=u * 5.4, height=u * 3.2, corner_radius=u * 0.6,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0).next_to(cabeza, DOWN, buff=u * 0.35)
    brazos = VGroup(*[
        Line(cuerpo.get_edge_center(lado), cuerpo.get_edge_center(lado) + lado * u * 1.1,
             color=color, stroke_width=3)
        for lado in (LEFT, RIGHT)
    ])
    return VGroup(antena, bombilla, cabeza, ojos, cuerpo, brazos)


def descarga(alto=1.4, color=PRIMARIO):
    u = alto / 3.0
    asta = Line(UP * u * 1.5, DOWN * u * 0.15, color=color, stroke_width=9)
    punta = Polygon(
        [-u * 0.8, -u * 0.1, 0], [u * 0.8, -u * 0.1, 0], [0, -u * 1.15, 0],
        stroke_width=0,
    ).set_fill(color, opacity=1.0)
    bandeja = VMobject(color=color, stroke_width=9)
    bandeja.set_points_as_corners([
        [-u * 1.5, -u * 0.85, 0], [-u * 1.5, -u * 1.65, 0],
        [u * 1.5, -u * 1.65, 0], [u * 1.5, -u * 0.85, 0],
    ])
    return VGroup(asta, punta, bandeja)


def billete(ancho=1.9, color=OK):
    alto = ancho * 0.46
    papel = RoundedRectangle(
        width=ancho, height=alto, corner_radius=alto * 0.14,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    filete = RoundedRectangle(
        width=ancho - alto * 0.3, height=alto - alto * 0.3,
        corner_radius=alto * 0.1, stroke_color=color, stroke_width=1.5,
    ).set_stroke(opacity=0.55)
    simbolo = texto("$", alto * 40, color=color).move_to(papel)
    return VGroup(papel, filete, simbolo)


def aspa(color=ERROR, tam=0.14, grosor=5):
    return VGroup(
        Line(LEFT * tam + DOWN * tam, RIGHT * tam + UP * tam,
             color=color, stroke_width=grosor),
        Line(LEFT * tam + UP * tam, RIGHT * tam + DOWN * tam,
             color=color, stroke_width=grosor),
    )


def visto(color=OK, tam=0.14, grosor=5):
    return VGroup(
        Line(np.array([-tam * 1.15, 0.0, 0]), np.array([-tam * 0.3, -tam, 0]),
             color=color, stroke_width=grosor),
        Line(np.array([-tam * 0.3, -tam, 0]), np.array([tam * 1.3, tam * 1.2, 0]),
             color=color, stroke_width=grosor),
    )


def separador(largo=4.6, grosor=3, color=PRIMARIO):
    return Line(LEFT * largo, RIGHT * largo, color=color, stroke_width=grosor)


def enmarcar(mob, margen=0.12, color=PRIMARIO):
    return RoundedRectangle(
        width=mob.width + margen, height=mob.height + margen,
        corner_radius=0.14, stroke_color=color, stroke_width=5, fill_opacity=0,
    ).move_to(mob.get_center())
