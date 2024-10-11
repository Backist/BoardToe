# models/__init__.py

import importlib

DEBUG = True

# DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'  # O establece DEBUG de otra manera

if DEBUG:
    bot = importlib.import_module('src.models.botv2')
else:
    bot = importlib.import_module('src.models.bot')
