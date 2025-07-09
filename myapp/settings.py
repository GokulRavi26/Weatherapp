import os
from pathlib import Path
from decouple import config, Csv  # ✅ Combined import with Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Correct static root setup for deployment
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ✅ Secure environment-based host configuration
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# (Keep the rest of your settings.py unchanged below this)
