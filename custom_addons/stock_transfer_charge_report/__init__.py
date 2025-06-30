# __init__.py en la raíz del módulo

try:
    from . import models
except Exception as e:
    print("ERROR al importar models:", e)

try:
    from . import report
except Exception as e:
    print("ERROR al importar report:", e)
