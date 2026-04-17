import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(path, *args, **kwargs):
        env_path = Path(path)
        if not env_path.exists():
            return False

        for line in env_path.read_text(encoding='utf-8').splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith('#') or '=' not in stripped:
                continue
            key, value = stripped.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())
        return True

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/1')
result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
timezone = 'Asia/Kolkata'
broker_connection_retry_on_startup = True
