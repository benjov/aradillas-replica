"""Ejecuta un notebook del proyecto en sitio, sin abrir Jupyter.

Uso (desde cualquier directorio):
    python3 codigo/run_nb.py 02_actualizacion_2022.ipynb
    python3 codigo/run_nb.py 03_comparacion_2014_2022.ipynb

Resuelve las dos trampas del entorno local (CLAUDE.md §9):
* los notebooks usan rutas relativas a la raíz del repo, así que el kernel
  corre con cwd = raíz del repo (cada notebook además lo resuelve solo);
* el kernelspec `python3` del sistema puede invocar un `python` inexistente, así
  que se registra un kernelspec temporal con ESTE intérprete (el que tiene
  numpy/pandas). No toca los kernels instalados.

Guarda el notebook ejecutado en notebooks/ejecutados/ (ignorado por git) y deja el original
limpio, sin salidas.
Requiere nbclient, nbformat e ipykernel.
"""
import json
import os
import sys
import tempfile
import time

import nbformat
from nbclient import NotebookClient

CODIGO = os.path.dirname(os.path.abspath(__file__))
PADRE = os.path.dirname(CODIGO)                      # raíz del repo
NOTEBOOKS = os.path.join(PADRE, 'notebooks')
EJECUTADOS = os.path.join(NOTEBOOKS, 'ejecutados')
KERNEL = 'aradillas-run-nb'


def kernelspec_temporal():
    """Crea un kernelspec que apunta a sys.executable y lo expone vía JUPYTER_PATH."""
    base = tempfile.mkdtemp(prefix='aradillas_kernel_')
    ruta = os.path.join(base, 'kernels', KERNEL)
    os.makedirs(ruta)
    with open(os.path.join(ruta, 'kernel.json'), 'w') as f:
        json.dump({'argv': [sys.executable, '-m', 'ipykernel_launcher',
                            '-f', '{connection_file}'],
                   'display_name': 'Python 3 (run_nb)', 'language': 'python'}, f)
    os.environ['JUPYTER_PATH'] = os.pathsep.join(
        [base] + [p for p in os.environ.get('JUPYTER_PATH', '').split(os.pathsep) if p])


def ejecutar(nombre):
    ruta = os.path.join(NOTEBOOKS, nombre)
    destino = os.path.join(EJECUTADOS, nombre)
    os.makedirs(EJECUTADOS, exist_ok=True)
    nb = nbformat.read(ruta, as_version=4)
    kernelspec_original = nb.metadata.get('kernelspec')
    t0 = time.time()
    cliente = NotebookClient(nb, kernel_name=KERNEL, timeout=None,
                             resources={'metadata': {'path': PADRE}})
    try:
        cliente.execute()
    finally:
        if kernelspec_original is not None:
            nb.metadata['kernelspec'] = kernelspec_original
        nbformat.write(nb, destino)

    codigo = [c for c in nb.cells if c.cell_type == 'code']
    errores = sum(any(o.get('output_type') == 'error' for o in c.get('outputs', []))
                  for c in codigo)
    avisos = sum(''.join(o.get('text', '')).count('Warning')
                 for c in codigo for o in c.get('outputs', []))
    print(f'{nombre}: {time.time() - t0:.0f} s | {len(codigo)} celdas de código | '
          f'{errores} con error | {avisos} advertencias')
    return errores


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    kernelspec_temporal()
    sys.exit(1 if sum(ejecutar(n) for n in sys.argv[1:]) else 0)
