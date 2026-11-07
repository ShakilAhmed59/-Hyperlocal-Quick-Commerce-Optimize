from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parent


def load_env_file(filename: str = ".env") -> None:
    env_path = PROJECT_ROOT / filename
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///hyperlocal_qcommerce.db")
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8080")
WEATHER_API_URL = os.getenv("WEATHER_API_URL", "https://api.open-meteo.com/v1/forecast")
OSRM_API_URL = os.getenv("OSRM_API_URL", "https://router.project-osrm.org")
NOMINATIM_API_URL = os.getenv("NOMINATIM_API_URL", "https://nominatim.openstreetmap.org")

