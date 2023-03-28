from pathlib import Path
from typing import Dict

DATA_FOLDER_PATH = Path(__file__).resolve().parent / Path("data/")

ENCODE_DATA_TEST: Dict[Path, str] = {
    DATA_FOLDER_PATH / "coast.jpg": "IQgSLYZ6iHePh4h1eFeHh4dwgwg3",
    DATA_FOLDER_PATH / "fall.jpg": "HBkSHYSIeHiPiHh8eJd4eTN0EEQG",
    DATA_FOLDER_PATH / "field.jpg": "3OcRJYB4d3h/iIeHeEh3eIhw+j3A",
    DATA_FOLDER_PATH / "firefox.png": "YJqGPQw7sFlslqhFafSE+Q6oJ1h2iHB2Rw==",
    DATA_FOLDER_PATH / "mountain.jpg": "2fcZFIB3iId/h3iJh4aIYJ2V8g==",
    DATA_FOLDER_PATH / "opera.png": "mYqDBQQnxnj0JoLYdN7f8JhpuDeHiHdwZw==",
    DATA_FOLDER_PATH / "street.jpg": "VggKDYAW6lZvdYd6d2iZh/p4GE/k",
    DATA_FOLDER_PATH / "sunrise.jpg": "1QcSHQRnh493V4dIh4eXh1h4kJUI",
    DATA_FOLDER_PATH / "sunset.jpg": "3PcNNYSFeXh/d3eld0iHZoZgVwh2",
}
