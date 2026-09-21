# Data_2022: archivos de INEGI que no viajan en el repo

Aquí deben estar los archivos de la lista `datos/MANIFIESTO_datos.csv` con `en_repo = no`
(unos 800 MB en total; el más grande, `gastoshogar.csv`, pesa 526 MB y no cabe en GitHub).
El caché `costos_saic_2023.csv` sí está versionado.

Los archivos deben conservar sus nombres. Dos formas de colocarlos:

1. Copiarlos a esta carpeta.
2. Si ya los tienes en otra carpeta, crear enlaces simbólicos:
   `bash scripts/enlazar_datos_2022.sh /ruta/a/tu/Data_2022`

Verifica con el notebook `notebooks/00_entorno_y_datos.ipynb` (revisa nombres, tamaños y SHA-256).

Origen de cada grupo de archivos:

| archivos | origen |
|---|---|
| `concentradohogar.csv`, `hogares.csv`, `viviendas.csv`, `ingresos.csv`, `gastoshogar.csv`, `gastospersona.csv` | ENIGH 2022 "Nueva serie", datos abiertos de INEGI: https://www.inegi.org.mx/programas/enigh/nc/2022/ |
| `data_ciudades/inpc_*.CSV` | Series locales del INPC por ciudad, INEGI (base 2ª quincena de julio 2018) |
| `data_inp_pp/INP_PP_*.CSV` | Precios promedio de referencia (julio 2018), consultas a la app de precios promedio del INPC de INEGI |
| `inpp_construccion.CSV` | INPP de construcción, INEGI |
| `censo_economico_2023.csv`, `censo_economico_fresnillo_2023.csv` | Censos Económicos (año de referencia 2023), INEGI |
| `datos_geograficos_municipios.csv` | Catálogo geográfico de municipios y localidades con coordenadas. Fuente exacta por confirmar |
