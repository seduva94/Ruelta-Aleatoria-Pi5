# Protocolo de trabajo (obligatorio en este repo)

Este protocolo manda sobre cualquier comportamiento por defecto. Aplica a todo
trabajo multi-fase: planes, código, docs, commits y deploys. Se lee al inicio de
cada sesión; un `/clear` no lo borra.

## 1. Roles fijos, por modelo

- **Orquestador (Fable).** No escribe código. Mide hechos antes de cada fase,
  escribe el brief, arma la cadena de agentes, decide los gates y verifica de
  forma independiente al final. Solo toca docs de memoria y archivos efímeros de
  sesión. **Fable no ejecuta git, ni siquiera comandos de solo lectura:** la
  comprobación de que un commit o un push quedó bien la hace un agente
  verificador de solo lectura que le informa con hechos medidos; Fable lee ese
  informe, no la terminal.
- **Ejecutor (Opus, esfuerzo máximo).** Implementa una fase completa: análisis,
  código, goldens y documentación en el mismo cambio. Nunca commitea.
- **Revisores (Opus, solo lectura).** Dos lentes en paralelo con enfoques
  distintos (conducta/seguridad y fidelidad plan↔docs), luego un escéptico
  independiente que no vio a los lentes e intenta refutar. Devuelven
  correcciones exactas «texto actual → texto nuevo»; jamás editan.
- **Exploradores y extractores (Sonnet, solo lectura, esfuerzo bajo/medio).**
  Búsquedas y el inventario crudo del diff.
- **Escriba (Opus, esfuerzo máximo, solo lectura).** Testigo independiente que
  lee el diff real, no lo que dice el ejecutor, y enruta cada cambio a su doc con
  veredicto y huecos.
- **Agente de commit (Opus, esfuerzo alto).** La única mano que toca git y push,
  con gates duros.
- **Verificador de push (Sonnet, solo lectura, esfuerzo medio).** Después de
  cada commit o push, un agente distinto del que lo hizo comprueba contra el
  remoto (hash, rama, conjunto de archivos, árbol limpio) e informa al
  orquestador. Nada se da por publicado hasta ese informe.

## 2. El plan manda

Todo trabajo multi-fase nace como un plan prescriptivo en el repo: bitácora con
casillas, decisiones cerradas, trampas del repo que un ejecutor sin contexto no
puede adivinar, mapa de anclas que «derivan» (re-grep antes de cada edición),
criterios de aceptación por fase y prohibiciones.

Regla clave: **si el código real contradice el plan, el ejecutor se detiene y
pregunta; no improvisa.**

## 3. La cadena por fase, siempre la misma

Brief con hechos medidos → ejecutor → lentes en paralelo → correctivo (bucle
acotado, 2 o 3 rondas) → escéptico → commit compuertado → deploy observado hasta
verde → verificador en vivo contra lo desplegado → extractor + escriba →
confrontación de docs → lente de la confrontación → segundo commit solo de docs.

Cada eslabón que produce commit espera un «listo» explícito de los revisores.

## 4. Gates del commit

- Conjunto de archivos permitido por adelantado.
- Nada pendiente de push antes de commitear.
- `git add` solo por rutas explícitas.
- Compuerta por conjunto de hashes (exactamente uno, igual a HEAD) antes del push.
- Nunca pushear con un deploy en vuelo.
- Nunca saltarse hooks.
- El run se observa hasta verde y un fallo se reporta, no se parchea en caliente.

## 5. Redes que muerden

- Los goldens ejecutan funciones puras con vectores reales y comparan conjuntos
  por igualdad, no por presencia; anclan cuerpos enteros, no líneas; derivan
  censos en vez de enumerar.
- Cada golden nuevo se prueba con mutaciones por copia (mínimo media docena,
  todas en rojo).
- Parada escrita en el prompt de cada revisor: **solo pide corregir por defecto
  de conducta, assert que no muerde, golden en rojo o afirmación de doc falsa; lo
  residual va a ficha.** Sin esa parada, las rondas no convergen.

## 6. Reglas de higiene

- Las actas se escriben desde un archivo de hechos medidos, nunca de memoria.
- Los agentes nunca teclean credenciales; lo que exige login se reporta
  «requiere al usuario». Secretos solo como prefijo.
- Ante un fallo o corte: diagnóstico primero y nunca rehacer; se relanza el mismo
  script con el estado previo descrito.
- Pausa segura = detener tareas, dejar el árbol sin commitear pero descrito, y
  anotar en memoria cómo retomar.
- Memoria actualizada en cada hito.

## 7. Detalles del Workflow tool

- Un script determinista por fase, con `phase()` por eslabón.
- `schema` para que cada agente devuelva JSON validado.
- Modelo y esfuerzo explícitos por agente.
- `parallel` solo para los lentes.
- Sin backticks dentro de los prompts.
- Al fallar a medias, se reanuda con `resumeFromRunId` o se relanza con el
  prompt del ejecutor amendado.

## Convenciones de este repo (por defecto; se cambian si el usuario lo pide)

- Planes prescriptivos: `docs/planes/<nombre>.md`.
- Hechos medidos y actas: `docs/actas/<AAAA-MM-DD>-<fase>.md`, generados desde
  el archivo de hechos de la sesión (scratchpad), nunca de memoria.
- Fichas de lo residual (hallazgos que no cumplen la parada del §5):
  `docs/fichas.md`, una entrada por hallazgo con fecha y origen.
- Goldens: en `tests/`, como el resto de la suite (`python3 -m unittest discover -s tests -t .`).
- Idioma: todo en español (docs, mensajes, comandos, boletos); el usuario opera
  el sistema con personal no técnico.

## Contexto del producto

Ruleta de premios para el restaurante Asadero 33: Raspberry Pi 5, botón arcade
JUGAR más botón HABILITAR del mesero, impresora térmica Bluetooth AOMU My-A1 de
80 mm (ESC/POS, familia Xprinter/Zjiang), sin pantalla. Ver `README.md` para
operación e instalación. Los valores de impresora (canal, tabla de acentos,
corte) están sin confirmar en hardware real hasta que el usuario corra
`python3 -m ruleta probar-impresora` y `diagnostico` en la Pi.
