<!-- Copia INTEGRA y LITERAL del archivo de hechos medidos del orquestador de la
     sesion del 2026-09-15 para la Fase 4a (scratchpad efimero:
     hechos-fase-4a-papel.md, 4979 bytes, sha256
     2efbe4c10cbda88eda3382d607bc887008b9e5bfac7c6ec6c94d4e7e4b2bf300).
     No se corrigio ni se anadio nada a su contenido: el plan
     docs/planes/fase-4a-papel.md y el acta de cierre de la fase se escriben
     DESDE aqui, nunca de memoria.
     El log integro de la sonda que cita la seccion "Sonda con lectura fresca"
     (sonda-papel-2026-09-15.log, 603 lineas, 48980 bytes) vive solo en el
     scratchpad de esa sesion y NO esta en el repositorio: lo que se conserva
     aqui son las transiciones que el orquestador extrajo de el. -->

# Hechos medidos · Fase 4a (detección de papel agotado) · 2026-09-15

Fuente única para el plan y el acta de la Fase 4a. Horas = reloj de la Pi (Hermosillo).
Log íntegro de la sonda: `sonda-papel-2026-09-15.log` (mismo directorio; 603 líneas, muchas
son EOT1/EOT2 repetidas porque la clave de cambio incluía los conteos del histograma).

## Antecedentes (ya medidos)
- 2026-09-13 (workflow ruleta-diagnostico-poco-papel): la AOMU My-A1 repite sin parar por el
  endpoint IN el último byte de estado que fijó su firmware (~21 kB/s); leer 1 byte tras
  DLE EOT devuelve la respuesta a la pregunta ANTERIOR. Aviso "poco papel" = artefacto
  (0x16 = respuesta sana de DLE EOT 1 leída con la tabla de DLE EOT 4; máscara de 1 bit).
  Propuesta que sobrevivió al escéptico: igualdad de pareja en escpos.py:122 y __main__.py:355,
  goldens B1–B4, docs C1–C8 (texto íntegro en scratchpad `diag-poco-papel.txt`, sección
  "propuesta_final" del escéptico).
- 2026-09-15 13:29 (servicio active, sin papel): el programa emitió 00009 TEST 7, leyó solo
  "poco papel" (byte rezagado), escribió el boleto, lo dio por impreso; la impresora pitó con
  foco rojo y retuvo el trabajo; al reponer papel imprimió sola el 00009; 00010 salió normal.

## Sonda con lectura fresca (13:40:17–13:44:35, servicio detenido, /tmp/sonda-papel.py)
Método por comando: drenar (hasta 512 bytes / 10 ms por byte) → escribir el comando → leer
hasta 64 bytes (0.5 s el primero, 50 ms los siguientes) → resumen primero/último/valores.
Transiciones de (primero, último, valores distintos) por comando:

```
13:40:17.600 EOT4 primero=16 ultimo=12 valores=(12,16) drenados=0      ← con papel
13:40:17.628 EOT1 primero=12 ultimo=16 valores=(12,16) drenados=512
13:40:17.655 EOT2 primero=16 ultimo=12 valores=(12,16) drenados=512
13:40:17.683 GSr1 primero=12 ultimo=12 valores=(12,)   drenados=512
13:40:18.710 EOT4 primero=12 ultimo=12 valores=(12,)   drenados=512
13:43:43.149 EOT2 primero=16 ultimo=32 valores=(16,32) drenados=0      ← SIN PAPEL, tapa cerrada
13:43:43.177 GSr1 primero=32 ultimo=32 valores=(32,)   drenados=512
13:43:44.204 EOT4 primero=32 ultimo=12 valores=(12,32) drenados=512    ← EOT4 sigue diciendo "papel bien"
13:44:12.511 EOT2 primero=16 ultimo=12 valores=(12,16) drenados=0      ← papel repuesto
13:44:12.514 GSr1 primero=12 ultimo=12 valores=(12,)   drenados=0
13:44:13.541 EOT4 primero=12 ultimo=12 valores=(12,)   drenados=512
```
Secuencia del usuario (~20 s por paso, sin horas exactas): 1 sacar papel, 2 abrir tapa,
3 cerrar tapa sin papel, 4 reponer papel y cerrar. Solo hubo UNA transición de ida (13:43:43)
y una de vuelta (13:44:12): coincide con "tapa cerrada sin papel" y "papel repuesto".

## Lectura de los bytes (tabla EPSON)
- DLE EOT 4 (sensores de papel): último byte SIEMPRE 0x12 = bits 2-3 = 00 y bits 5-6 = 00
  ("papel suficiente y presente") incluso sin papel. → En este clon EOT4 NO sirve para
  detectar papel agotado. BITS_SIN_PAPEL (0x60) nunca se activará.
- DLE EOT 1 (estado de impresora): último byte 0x16 en todo momento (b2 = pin 3 cajón alto,
  b3 = 0 EN LÍNEA) incluso sin papel. → BIT_FUERA_DE_LINEA (0x08) nunca se activará.
- DLE EOT 2 (causa de fuera de línea): con papel 0x12; SIN PAPEL y tapa cerrada 0x32 =
  0b0011_0010 → bit 5 = 1 = "impresión detenida por fin de papel" (EPSON: b2 tapa abierta,
  b3 alimentación por botón, b5 fin de papel, b6 error). Vuelve a 0x12 al reponer papel.
  Tapa abierta (paso 2) NO produjo ningún cambio observable (bit 2 nunca se vio).
- GS r 1: nunca contesta; el "último" es siempre el valor del flujo (0x12 / 0x32). Inútil.
- Lectura fresca: el "último de 64" refleja la respuesta al comando recién enviado (p. ej.
  13:43:44 EOT4 primero=32 último=12: el flujo traía el 0x32 de EOT2 y cambió al 0x12 de EOT4).
  drenar() SIEMPRE topa en 512 bytes (el flujo no se vacía nunca).

## Consecuencia de diseño (para el plan de Fase 4a)
1. `_leer_estado` (ImpresoraArchivo y ImpresoraBluetooth) debe devolver la respuesta FRESCA:
   drenar con tope, escribir, leer hasta N bytes/tiempo tope y quedarse con el ÚLTIMO byte
   válido. En una impresora EPSON normal (1 byte de respuesta) el resultado es el mismo byte.
2. Añadir la consulta DLE EOT 2 y tratar bit 5 (0x20, fin de papel) y bit 6 (0x40, error)
   como "no imprimir" (ErrorConexion antes de mandar un byte); bit 2 (0x04, tapa abierta)
   también, aunque este clon no lo reporte. Mantener EOT4 bits 5-6 y EOT1 bit 3 como están.
3. Máscara estricta para "poco papel" (bits 2-3 == 11) como ya se propuso; el aviso sigue
   siendo warning.
4. Criterio de aceptación en vivo: repetir la jugada sin papel con el servicio activo → el
   journal debe decir que la impresora no tiene papel, el boleto debe REVERTIRSE (premio de
   vuelta, folio no reutilizado según la política actual) y nada debe quedar retenido en la
   impresora; al reponer papel, la siguiente jugada imprime normal.
