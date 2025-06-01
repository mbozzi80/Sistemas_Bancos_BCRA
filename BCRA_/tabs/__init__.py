"""
Módulo de tabs para la aplicación BCRA
"""

from . import tab_resumen
from . import tab_prestamos
from . import tab_titulos
from . import tab_depositos
from . import tab_ratios
from . import tab_descarga

__all__ = [
    'tab_resumen',
    'tab_prestamos', 
    'tab_titulos',
    'tab_depositos',
    'tab_ratios',
    'tab_descarga'
]