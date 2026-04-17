import os
from datetime import timedelta, datetime
from pathlib import Path
from flask_caching import Cache

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

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')
cache = Cache()

def _env_str(name, default=None):
    return os.environ.get(name, default)


def _env_int(name, default):
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"Invalid integer for {name}: {value}") from exc


def _env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def _validate_required(config_class, required_keys):
    missing = [key for key in required_keys if not getattr(config_class, key, None)]
    if missing:
        missing_csv = ', '.join(missing)
        raise RuntimeError(f"Missing required configuration values: {missing_csv}. Update backend/.env")


class Config:
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = _env_str('SQLALCHEMY_DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_JOIN_USER_ROLES = True
    SECURITY_TRACKABLE = True

    SECRET_KEY = _env_str('SECRET_KEY')
    SECURITY_PASSWORD_SALT = _env_str('SECURITY_PASSWORD_SALT')

    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    SECURITY_TOKEN_MAX_AGE = datetime.now() + timedelta(days=100)

    CACHE_TYPE = _env_str('CACHE_TYPE', 'SimpleCache')
    CACHE_REDIS_HOST = _env_str('CACHE_REDIS_HOST', 'localhost')
    CACHE_REDIS_PORT = _env_int('CACHE_REDIS_PORT', 6379)
    CACHE_DEFAULT_TIMEOUT = _env_int('CACHE_DEFAULT_TIMEOUT', 120)
    CACHE_REDIS_DB = _env_int('CACHE_REDIS_DB', 0)

    MAIL_SERVER = _env_str('MAIL_SERVER', 'localhost')
    MAIL_PORT = _env_int('MAIL_PORT', 1025)
    MAIL_DEFAULT_SENDER = _env_str('MAIL_DEFAULT_SENDER', 'no-reply@Pustakalay.com')


class DevConfig(Config):
    DEBUG = _env_bool('FLASK_DEBUG', True)


class ProdConfig(Config):
    DEBUG = _env_bool('FLASK_DEBUG', False)


def get_config_class():
    env = _env_str('APP_ENV', _env_str('FLASK_ENV', 'development')).lower()
    if env in {'prod', 'production'}:
        _validate_required(ProdConfig, ['SECRET_KEY', 'SECURITY_PASSWORD_SALT'])
        return ProdConfig

    _validate_required(DevConfig, ['SECRET_KEY', 'SECURITY_PASSWORD_SALT'])
    return DevConfig
    

