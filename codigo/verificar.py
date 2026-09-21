"""Compara una corrida de congelado contra la referencia versionada.

Ignora `segundos` (tiempo de cómputo) y `_meta` (fecha, commit, entorno). Todo lo demás debe
coincidir. Con `tol` > 0 se aceptan diferencias numéricas pequeñas: sirve solo como prueba de
humo en otro sistema operativo o versión de numpy. El congelado canónico se compara con tol = 0.
"""
import json

IGNORAR = {'segundos', '_meta'}


def _numero(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _recorrer(a, b, ruta, acc, tol):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in IGNORAR:
                continue
            if k not in a or k not in b:
                acc['dif'].append((f'{ruta}/{k}', 'falta en la referencia' if k not in a else 'falta en la nueva', None))
                continue
            _recorrer(a[k], b[k], f'{ruta}/{k}', acc, tol)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            acc['dif'].append((ruta, f'longitudes {len(a)} vs {len(b)}', None))
            return
        for i, (x, y) in enumerate(zip(a, b)):
            _recorrer(x, y, f'{ruta}[{i}]', acc, tol)
    else:
        acc['n'] += 1
        if _numero(a) and _numero(b):
            d = abs(a - b)
            acc['max_abs'] = max(acc['max_abs'], d)
            if d > tol:
                acc['dif'].append((ruta, a, b))
        elif a != b:
            acc['dif'].append((ruta, a, b))


def comparar(ruta_ref, ruta_nueva, configs=None, tol=0.0):
    """Devuelve {'n_valores', 'max_abs', 'diferencias', 'configs'}."""
    ref = json.load(open(ruta_ref, encoding='utf-8'))
    nueva = json.load(open(ruta_nueva, encoding='utf-8'))
    configs = configs or [k for k in nueva if k not in IGNORAR]
    acc = {'n': 0, 'max_abs': 0.0, 'dif': []}
    for c in configs:
        if c not in ref:
            acc['dif'].append((f'/{c}', 'no está en la referencia', None))
            continue
        _recorrer(ref[c], nueva[c], f'/{c}', acc, tol)
    return {'configs': configs, 'n_valores': acc['n'], 'max_abs': acc['max_abs'],
            'diferencias': acc['dif']}


def informe(res, maximo=15):
    print(f"configuraciones comparadas: {', '.join(res['configs'])}")
    print(f"valores comparados: {res['n_valores']:,} | diferencia absoluta máxima: {res['max_abs']:.3g}")
    n = len(res['diferencias'])
    if n == 0:
        print('RESULTADO: 0 diferencias. La corrida reproduce el congelado.')
        return
    print(f'RESULTADO: {n} diferencias. Primeras {min(n, maximo)}:')
    for ruta, a, b in res['diferencias'][:maximo]:
        print(f'  {ruta}: referencia={a!r}  nueva={b!r}')
