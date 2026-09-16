"""Diseño de los boletos (premio, consuelo, inventario y prueba).

Cada función recibe un `Documento` recién creado y devuelve los bytes listos
para enviar a la impresora. La lógica de acomodo es independiente del
transporte, así se puede previsualizar en consola o probar sin hardware.
"""

from __future__ import annotations

import textwrap
from datetime import datetime

from . import __version__
from .config import Config
from .escpos import CODECS_TABLA, Documento
from .inventario import Boleto, Resumen, ResumenPremio

FORMATO_FECHA = "%d/%m/%Y %H:%M"
# Lo que se imprime cuando el kiosco arrancó sin poder confirmar la hora
# (pieza D, Fase 4d): la Pi no tiene batería RTC y del día dependen los topes
# diarios, las fechas de los premios y el reparto por horas.
AVISO_HORA = "HORA SIN CONFIRMAR: revisar fecha"


# --------------------------------------------------------------------------- #
# Utilidades de acomodo
# --------------------------------------------------------------------------- #

def ajustar_texto_grande(texto: str, chars_por_linea: int, tamanos=(4, 3, 2),
                         max_lineas: int = 3) -> tuple[int, list[str]]:
    """Elige el tamaño más grande con el que el texto cabe en `max_lineas`.

    Devuelve (multiplicador, líneas). Si no cabe ni en tamaño 2, usa 1 y
    recorta a max_lineas.
    """
    texto = " ".join(texto.split())
    for t in tamanos:
        ancho = max(1, chars_por_linea // t)
        if any(len(palabra) > ancho for palabra in texto.split()):
            continue
        lineas = textwrap.wrap(texto, width=ancho)
        if 0 < len(lineas) <= max_lineas:
            return t, lineas
    lineas = textwrap.wrap(texto, width=chars_por_linea) or [""]
    return 1, lineas[:max_lineas]


def envolver(texto: str, ancho: int) -> list[str]:
    return textwrap.wrap(texto, width=ancho) or [""]


def _dos_columnas(izq: str, der: str, ancho: int) -> str:
    espacio = ancho - len(izq) - len(der)
    if espacio < 1:
        izq = izq[: max(0, ancho - len(der) - 1)]
        espacio = 1
    return izq + " " * espacio + der


def renglones_de_liberacion(fila: ResumenPremio, ancho: int) -> list[str]:
    """Las líneas del reparto por horas de un premio, ya sangradas y partidas.

    Lista vacía si ese premio no se reparte (sin `tope_diario` y sin `franjas`).
    Función pura: todo lo que necesita ya viene calculado en la fila del
    resumen, incluida la hora, que nunca se lee aquí del reloj del sistema.
    """
    if fila.liberadas is None:
        return []
    partes = [f"hoy {fila.hoy}", f"liberadas {fila.liberadas}"]
    partes.append(f"sig {fila.proxima.strftime('%H:%M')}" if fila.proxima is not None
                  else "sin más hoy")
    return ["  " + l for l in envolver(" · ".join(partes), max(1, ancho - 2))]


def _cargar_logo(cfg: Config):
    ruta = cfg.ruta_logo()
    if ruta is None or not ruta.exists():
        return None
    try:
        from PIL import Image
        img = Image.open(ruta)
        img.load()
        return img
    except Exception:  # archivo corrupto, formato raro, Pillow ausente...
        return None


def _nuevo_documento(cfg: Config) -> Documento:
    imp = cfg.impresora
    return Documento(codepage=imp.codepage, codepage_n=imp.codepage_n,
                     chars_por_linea=imp.chars_por_linea, ancho_puntos=imp.ancho_puntos,
                     juego_internacional=imp.juego_internacional,
                     cancelar_modo_chino=imp.cancelar_modo_chino)


def _encabezado(doc: Documento, cfg: Config, con_logo: bool = True) -> None:
    doc.inicializar().alinear("centro")
    logo = _cargar_logo(cfg) if con_logo else None
    if logo is not None:
        doc.imagen(logo, ancho_max=min(cfg.negocio.logo_ancho, cfg.impresora.ancho_puntos),
                   tramado=cfg.negocio.logo_tramado, banda=cfg.impresora.banda_imagen)
        doc.linea()
    doc.negrita(True).tamano(2, 2)
    for l in envolver(cfg.negocio.nombre, doc.chars_linea_actual):
        doc.linea(l)
    doc.tamano(1, 1).negrita(False)


def _cierre(doc: Documento, cfg: Config) -> bytes:
    imp = cfg.impresora
    if imp.beep:
        doc.beep(2, 2)
    doc.cortar(imp.corte, imp.lineas_antes_corte)
    return doc.bytes()


# --------------------------------------------------------------------------- #
# Boletos
# --------------------------------------------------------------------------- #

def boleto_premio(cfg: Config, boleto: Boleto) -> bytes:
    assert boleto.premio is not None
    doc = _nuevo_documento(cfg)
    premio = boleto.premio
    _encabezado(doc, cfg)
    doc.separador()

    doc.alinear("centro").negrita(True).tamano(2, 2)
    doc.linea(cfg.negocio.titulo_premio)
    doc.tamano(1, 1).linea()

    mult, lineas = ajustar_texto_grande(premio.nombre.upper(), cfg.impresora.chars_por_linea)
    doc.tamano(mult, mult)
    for l in lineas:
        doc.linea(l)
    doc.tamano(1, 1).negrita(False)

    if premio.detalle:
        doc.linea()
        for l in envolver(premio.detalle, doc.chars_linea_actual):
            doc.linea(l)

    doc.linea().separador()
    doc.negrita(True).tamano(2, 2).linea(f"BOLETO {boleto.folio_texto}")
    doc.tamano(1, 1).negrita(False)
    doc.linea(boleto.momento.strftime(FORMATO_FECHA))
    doc.separador()

    doc.alinear("centro")
    for l in cfg.negocio.pie:
        for parte in envolver(l, doc.chars_linea_actual):
            doc.linea(parte)
    return _cierre(doc, cfg)


def boleto_consuelo(cfg: Config, boleto: Boleto) -> bytes:
    doc = _nuevo_documento(cfg)
    _encabezado(doc, cfg)
    doc.separador()
    doc.alinear("centro").negrita(True)
    mult, lineas = ajustar_texto_grande(cfg.juego.consuelo.titulo, cfg.impresora.chars_por_linea,
                                        tamanos=(3, 2))
    doc.tamano(mult, mult)
    for l in lineas:
        doc.linea(l)
    doc.tamano(1, 1).negrita(False).linea()
    for l in envolver(cfg.juego.consuelo.texto, doc.chars_linea_actual):
        doc.linea(l)
    doc.linea().separador()
    doc.linea(f"BOLETO {boleto.folio_texto}  {boleto.momento.strftime(FORMATO_FECHA)}")
    return _cierre(doc, cfg)


def boleto_inventario(cfg: Config, resumen: Resumen, motivo: str = "",
                      aviso_hora: bool = False) -> bytes:
    """Reporte de inventario: se imprime al arrancar y bajo pedido."""
    doc = _nuevo_documento(cfg)
    ancho = cfg.impresora.chars_por_linea
    doc.inicializar().alinear("centro").negrita(True).tamano(2, 2)
    doc.linea("INVENTARIO")
    doc.tamano(1, 1).negrita(False)
    doc.linea(cfg.negocio.nombre)
    doc.linea(resumen.momento.strftime(FORMATO_FECHA) + (f"  ({motivo})" if motivo else ""))
    doc.linea(f"Día operativo: {resumen.dia.strftime('%d/%m/%Y')}")
    if aviso_hora:
        doc.negrita(True)
        for l in envolver(AVISO_HORA, doc.chars_linea_actual):
            doc.linea(l)
        doc.negrita(False)
    doc.separador()

    doc.alinear("izq")
    # Columnas: nombre | restantes/total | hoy/tope | prob%
    col_rest, col_hoy, col_prob = 9, 7, 6
    col_nombre = max(1, ancho - col_rest - col_hoy - col_prob - 3)
    doc.negrita(True)
    doc.linea(f"{'PREMIO':<{col_nombre}} {'REST/TOT':>{col_rest}} {'HOY':>{col_hoy}} {'PROB':>{col_prob}}")
    doc.negrita(False)
    for fila in resumen.premios:
        p = fila.premio
        nombre = p.nombre if len(p.nombre) <= col_nombre else p.nombre[: col_nombre - 1] + "."
        if p.stock is None:
            rest = f"{fila.entregados}/inf"
        else:
            rest = f"{fila.restantes}/{p.stock}"
        hoy = f"{fila.hoy}/{p.tope_diario}" if p.tope_diario is not None else f"{fila.hoy}"
        prob = f"{fila.probabilidad:.1f}%" if fila.disponible else "--"
        doc.linea(f"{nombre:<{col_nombre}} {rest:>{col_rest}} {hoy:>{col_hoy}} {prob:>{col_prob}}")
        if not fila.disponible:
            doc.linea(f"  > no disponible: {fila.motivo}")
        # Renglón del reparto por horas (Fase 4d): entregadas hoy, piezas que el
        # reloj ya abrió y a qué hora se abre la siguiente. Solo para los premios
        # que se reparten; los que no tienen tope diario ni franjas no lo llevan.
        for l in renglones_de_liberacion(fila, ancho):
            doc.linea(l)
    # El boleto de consuelo compite como uno más cuando tiene peso (Fase 4c).
    # Sin peso no se menciona: solo sale cuando ya no queda ningún premio.
    if resumen.peso_consuelo > 0:
        doc.linea(_dos_columnas(
            f"{cfg.juego.consuelo.titulo} (consuelo)",
            f"peso {resumen.peso_consuelo} -> {resumen.probabilidad_consuelo:.1f}%", ancho))
    doc.separador()
    total_stock = sum(p.premio.stock for p in resumen.premios if p.premio.stock is not None)
    total_entregados = sum(p.entregados for p in resumen.premios)
    doc.linea(_dos_columnas("Premios entregados:", f"{total_entregados}/{total_stock}", ancho))
    doc.linea(_dos_columnas("Boletos emitidos hoy:", str(resumen.boletos_hoy), ancho))
    doc.linea(_dos_columnas("Último folio:", f"{resumen.folio_actual:05d}", ancho))
    doc.linea(_dos_columnas("Disponibles ahora:", str(sum(1 for p in resumen.premios if p.disponible)), ancho))
    doc.separador()
    if resumen.pendientes:
        doc.negrita(True).linea("REVISAR - boletos sin confirmar:").negrita(False)
        for l in envolver("Coteja estos folios con los boletos físicos. Si alguno NO salió, "
                          "devuelve su premio con: python3 -m ruleta liberar FOLIO", ancho):
            doc.linea(l)
        # "  FFFFF MM-DD HH:MM evento__ nombre" = 29 caracteres + nombre
        max_nombre = max(1, ancho - 29)
        for p in resumen.pendientes[-12:]:
            nombre = p.premio_nombre
            if len(nombre) > max_nombre:
                nombre = nombre[: max_nombre - 1] + "."
            doc.linea(f"  {p.folio_texto} {p.fecha_hora[5:16]} {p.evento:<8} {nombre}")
        if len(resumen.pendientes) > 12:
            doc.linea(f"  ... y {len(resumen.pendientes) - 12} más (ver datos/boletos.csv)")
        doc.separador()
    doc.alinear("centro").linea(f"Ruleta v{__version__} lista para jugar")
    return _cierre(doc, cfg)


def boleto_prueba(cfg: Config, tablas: tuple[int, ...] = (0, 2, 16, 19)) -> bytes:
    """Boleto de diagnóstico: acentos con varias tablas, tamaños, logo y corte.

    Para elegir `codepage_n`: la línea de acentos que salga bien indica el
    número de tabla que hay que poner en config.json.
    """
    doc = _nuevo_documento(cfg)
    muestra = "ñ Ñ á é í ó ú Á É Í Ó Ú ü ¿ ¡ º"
    doc.inicializar().alinear("centro").negrita(True).tamano(2, 2).linea("PRUEBA")
    doc.tamano(1, 1).negrita(False)
    doc.linea(f"Ruleta v{__version__}  {datetime.now().strftime(FORMATO_FECHA)}")
    doc.separador().alinear("izq")
    doc.linea("Acentos con cada tabla de caracteres:")
    for n in tablas:
        if not 0 <= n <= 255:
            raise ValueError(f"tabla de caracteres fuera de rango (0-255): {n}")
        codec = CODECS_TABLA.get(n, cfg.impresora.codepage)
        doc.crudo(b"\x1bt" + bytes([n]))
        # La etiqueta va en su propia línea y la muestra en la siguiente: juntas
        # pasaban de 48 columnas y la impresora las partía a media palabra.
        doc.linea(f"  ESC t {n} ({codec}):")
        original, doc.codepage = doc.codepage, codec
        doc.linea(muestra)
        doc.codepage = original
    doc.crudo(b"\x1bt" + bytes([cfg.impresora.codepage_n]))
    doc.linea(f"Configurado: codepage_n={cfg.impresora.codepage_n} ({cfg.impresora.codepage})")
    doc.separador()
    doc.linea("Regla de ancho (debe llenar la línea):")
    doc.linea("".join(str(i % 10) for i in range(cfg.impresora.chars_por_linea)))
    doc.separador().alinear("centro")
    for t in (1, 2, 3, 4):
        doc.tamano(t, t).linea(f"Tamaño {t}x")
    doc.tamano(1, 1)
    doc.negrita(True).linea("Negrita").negrita(False)
    doc.separador()
    logo = _cargar_logo(cfg)
    if logo is not None:
        doc.linea("Logo:")
        doc.imagen(logo, ancho_max=min(cfg.negocio.logo_ancho, cfg.impresora.ancho_puntos),
                   tramado=cfg.negocio.logo_tramado, banda=cfg.impresora.banda_imagen)
    else:
        doc.linea(f"(sin logo: no existe {cfg.ruta_logo()})")
    doc.separador()
    doc.linea("Si esto se cortó solo, el cortador funciona.")
    return _cierre(doc, cfg)
