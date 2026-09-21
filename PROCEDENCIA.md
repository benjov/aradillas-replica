# Procedencia de este repositorio

## Origen

Repositorio `benjov/Replica_COFECE`, rama `refactor-modulos`.

| qué | commit del repositorio original |
|---|---|
| código de `Codigo/` | `c956eeb` (sin cambios hasta `18ed46d`) |
| congelado (`resultados/`) | `18ed46d`, generado el 2026-09-21 00:07 (hora de México) con Python 3.9.6 y numpy 1.26.4 |

`resultados/resultados_congelados.json` y `resultados/RESULTADOS.md` son copias byte a byte de los de
`18ed46d` (verificado con `cmp`). Ese congelado tiene 0 diferencias numéricas contra el anterior
(`e1bcb71`), que se corrió con cambios sin commit.

## Qué es idéntico

Los módulos numéricos se copiaron sin modificar. SHA-256 en `procedencia/SHA256_modulos_numericos.txt`
(`aradillas_core.py`, `datos_base.py`, `datos_2014.py`, `datos_2022.py`, `costos_saic.py`,
`inpc_lista_productos.py`, `municipios.py`). También son copias los datos de `datos/Data_2014/`,
`datos/Data_auditoria/` y `datos/Data_2022/costos_saic_2023.csv`.

## Qué cambió

* **Rutas en tres scripts** (`congelar_resultados.py`, `diagnostico_ve_cero.py`, `run_nb.py`): la nueva
  estructura de carpetas, la variable de entorno `ARADILLAS_SALIDA` y la carpeta `notebooks/ejecutados/`.
  Ningún cálculo cambia. Diff completo en `procedencia/cambios_en_scripts.diff`.
* **Notebooks 01 a 04**: vienen de `aradillas_2014`, `aradillas_2022`, `comparacion_2014_2022` y
  `auditoria_precios`. Se les quitaron las salidas guardadas, se cambiaron las rutas y se agregó una celda
  de preparación. En 01 a 03 se corrigieron textos con cifras que no coincidían con el congelado, y se
  agregó una celda final de cotejo contra `resultados/`. Los notebooks 00, 05 y 06 son nuevos.
* **Nuevo**: `codigo/verificar.py`, `datos/MANIFIESTO_datos.csv`, `scripts/enlazar_datos_2022.sh`.

## Qué no se trajo

`reporte_hallazgos.ipynb` (superado por P2), `aradillas_2022_DOCUMENTADO.ipynb` (pipeline anterior, con
errores conocidos), `productos.py` y `datos_comparacion.py` (no los importa el pipeline), la bitácora
histórica, `CD/*.asc` (duplican `Data_2014`), el PDF del paper y los microdatos de 2022.

## Qué se verificó al armarlo (Linux aarch64, Python 3.10.12, numpy 1.26.4, pandas 2.2.3, scipy 1.13.1)

* Las cuatro configuraciones de 2014 (`replica_2014`, `replica_2014_13cat`, `comparable_2014`,
  `comparable_2014_13cat`): **0 diferencias en 2,966 valores** contra la referencia. `verificar.py` detecta
  una diferencia inducida de 0.0001.
* Notebooks 00, 01, 04, 05 y 06 (con `replica_2014`) ejecutan sin errores. En 01, 04 y 05 las cifras
  coinciden con el congelado y con P2 (§5.1 y §7).
* La carga de 2022 con solo los archivos del manifiesto da 57,552 hogares y 13 categorías, igual que el
  congelado.

## Verificación de 2022 en la máquina de los autores (21 de septiembre de 2026)

Entorno: macOS, procesador x86_64, Anaconda (`PythonData`), **Python 3.10.14, numpy 1.25.2, pandas 2.1.1,
scipy 1.9.3**. No es el entorno canónico del congelado (Python 3.9.6, numpy 1.26.4, pandas 2.2.3, scipy 1.13.1),
y el cuaderno 00 lo avisa.

* `06_congelar_resultados` con `comparable_2022`, `comparable_2022_12cat` y `trim_2022`, `TOLERANCIA = 0.0`:
  **0 diferencias en 1,441 valores** (diferencia absoluta máxima 0) contra `resultados/resultados_congelados.json`.
  Tiempo: 21.7 min (472 s, 363 s y 470 s).
* Cuadernos 00 a 05 ejecutados sin errores. En 01, 02 y 03 la celda de cotejo dice "Todo coincide con el
  congelado". El 04 reproduce la tabla de precios del Anexo B del informe y el 05 los porcentajes de §5.1.
* Notas de la corrida: `RuntimeWarning` de numpy sobre grados de libertad (`comparable_2022`, control `rama`) y de
  división en `regresividad` (`trim_2022`, control `ciudad`, donde la VE es 0.0 %). Ambos ya estaban en el congelado
  y no cambian ninguna cifra.
* `resultados/nueva_corrida/` (ignorada por git) trae `_meta.git.commit = null`; no es la referencia.

## Qué queda sin verificar

* La corrida completa (siete configuraciones) con el intérprete canónico (`/usr/bin/python3`, 3.9.6) usando este
  repositorio. El congelado se generó con él en el repositorio de trabajo; este repositorio se ha corrido en
  Linux (2014) y en Anaconda (2022), no en ese intérprete.
* Las cuatro configuraciones de 2014 con `06_congelar_resultados` en la máquina de los autores (allí solo se
  ejecutó el cuaderno 01, cuyo cotejo es a la precisión impresa).

## Autoría

Según `git shortlog -sn --all` del repositorio original: Víctor Camps Abarca, 27 commits (13 de julio al
4 de septiembre de 2026); benjov, 18 commits (23 de junio al 20 de septiembre de 2026).
