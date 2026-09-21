# Réplica y actualización de Aradillas López (2018) — repositorio de reproducibilidad

Réplica en Python del estudio de Aradillas López, A. (2018), *Estudio sobre el impacto que tiene el
poder de mercado en el bienestar de los hogares mexicanos* (COFECE), contrastada línea por línea con
el programa Gauss que lo produjo, y actualizada a la ENIGH 2022.

Este repositorio existe para una cosa: que cualquiera pueda **volver a correr todo con notebooks** y
comprobar que obtiene las cifras del reporte. Las cifras citables están congeladas en `resultados/`.

## Empezar (5 minutos, solo 2014)

```bash
git clone <este repo> aradillas-replica && cd aradillas-replica
/usr/bin/python3 -m pip install --user -r requirements.txt     # numpy 1.26.4, pandas 2.2.3, scipy 1.13.1, jupyter
jupyter notebook notebooks/00_entorno_y_datos.ipynb
```

Si Jupyter no encuentra el kernel (en macOS el del sistema puede invocar un `python` inexistente),
ejecuta cualquier notebook sin abrir Jupyter:

```bash
/usr/bin/python3 codigo/run_nb.py 01_replica_2014.ipynb        # deja el resultado en notebooks/ejecutados/
```

## Los notebooks, en orden

| notebook | qué hace | tiempo* | necesita |
|---|---|---|---|
| `00_entorno_y_datos` | verifica versiones, datos (nombre, tamaño, SHA-256) y muestra qué congelado es la referencia | segundos | — |
| `01_replica_2014` | réplica de fidelidad al Gauss (con recorte iterativo, 12 categorías) y cuadros contra el paper | ~35 s | Data_2014 |
| `02_actualizacion_2022` | mismo pipeline con ENIGH 2022, sin recorte | ~4 min | Data_2022 |
| `03_comparacion_2014_2022` | ambos años con tratamiento idéntico (sin recorte, ingreso corriente) | ~5 min | ambos |
| `04_auditoria_precios` | precios del estudio contra los niveles observados de INEGI | segundos | Data_2014, Data_2022, Data_auditoria |
| `05_diagnostico_ve_cero` | quién queda con pérdida cero al agregar Transporte foráneo (P2 §5.1) | ~35 s | Data_2014 |
| `06_congelar_resultados` | **regenera todas las cifras y las compara con la referencia, valor por valor** | ~2.5 min (2014) / ~15 min (todo) | según configuración |

\* En la Mac con la que se generó el congelado. Cada notebook termina con un cotejo contra `resultados/`.

## Qué es cada carpeta

| carpeta | contenido |
|---|---|
| `codigo/` | Módulos del pipeline (`aradillas_core.py`: cálculo; `datos_2014.py`, `datos_2022.py`: carga), `congelar_resultados.py`, `verificar.py` y `run_nb.py` |
| `notebooks/` | Los siete notebooks, sin salidas guardadas |
| `datos/` | `Data_2014/` y `Data_auditoria/` viajan en el repo. `Data_2022/` (unos 800 MB de INEGI) **no**: ver `datos/Data_2022/LEEME.md` y `datos/MANIFIESTO_datos.csv` |
| `referencia/` | `programa_ENIGH_2014.g` y `programa_ENIGH_2006.g`: el programa Gauss original, obtenido por solicitud de acceso a la información. Las referencias de línea (l.NNNN) del reporte son a este archivo |
| `resultados/` | `resultados_congelados.json` y `RESULTADOS.md`: **toda cifra citable**. No se editan a mano |
| `procedencia/` | De dónde viene cada archivo y qué se cambió respecto del repositorio original (ver `PROCEDENCIA.md`) |
| `scripts/` | `enlazar_datos_2022.sh`: enlaza sin copiar los archivos de 2022 que ya tengas en otra carpeta |

## Cómo se verifica una reproducción

`06_congelar_resultados` corre las configuraciones de `codigo/congelar_resultados.py`, escribe en
`resultados/nueva_corrida/` (no pisa la referencia) y compara **cada valor** del JSON con
`resultados/resultados_congelados.json`. Con el entorno del congelado (Python 3.9.6, numpy 1.26.4)
se esperan **0 diferencias**. Tiempos de cómputo y sello de fecha se ignoran.

Regla del proyecto: **si el código cambia, se vuelve a congelar antes de citar cifras.**

## Datos de 2022

Los microdatos de INEGI no caben en GitHub (`gastoshogar.csv` pesa 526 MB). Descárgalos como indica
`datos/Data_2022/LEEME.md`, o, si ya los tienes en otra carpeta:

```bash
bash scripts/enlazar_datos_2022.sh /ruta/a/tu/Data_2022
```

## Procedencia y autoría

Este repositorio empaqueta el trabajo de `Replica_COFECE` (código en el commit `c956eeb`, congelado en
el commit `18ed46d`). Los módulos numéricos son **idénticos byte a byte**; los cambios se limitan a rutas
y a los textos de los notebooks. Detalle y SHA-256 en `PROCEDENCIA.md`.

Autores: Benjamín Oliva (`benjov`) y Víctor Camps Abarca. La historia de commits individual vive en el
repositorio original.

Licencia: por definir.
