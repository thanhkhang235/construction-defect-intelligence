from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
EXTRACTED_DATA_DIR = DATA_DIR / "extracted"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"
ENV_PATH = PROJECT_ROOT / ".env"


def load_environment() -> None:
    load_dotenv(dotenv_path=ENV_PATH)
