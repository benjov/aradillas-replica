#!/usr/bin/env bash
# Enlaza (sin copiar) los archivos de ENIGH 2022 que ya tienes en otra carpeta.
# Uso: bash scripts/enlazar_datos_2022.sh /ruta/a/Data_2022
set -euo pipefail
ORIGEN="${1:?Uso: bash scripts/enlazar_datos_2022.sh /ruta/a/Data_2022}"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
DESTINO="$RAIZ/datos/Data_2022"
[ -d "$ORIGEN" ] || { echo "No existe la carpeta $ORIGEN" >&2; exit 1; }
ORIGEN="$(cd "$ORIGEN" && pwd)"
faltan=0
for nombre in $(awk -F, 'NR>1 && $1=="Data_2022" && $5=="no" {print $2}' "$RAIZ/datos/MANIFIESTO_datos.csv" | sed 's#/.*##' | sort -u); do
  if [ -e "$ORIGEN/$nombre" ]; then
    ln -sfn "$ORIGEN/$nombre" "$DESTINO/$nombre"
  else
    echo "FALTA: $nombre" >&2; faltan=$((faltan+1))
  fi
done
echo "Enlaces creados en $DESTINO. Faltantes: $faltan"
echo "Verifica con notebooks/00_entorno_y_datos.ipynb"
