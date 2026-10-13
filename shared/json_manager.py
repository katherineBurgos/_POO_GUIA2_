"""Persistencia JSON sencilla para el CRUD de la guía."""
import json
from pathlib import Path


class GestorJSON:
    def __init__(self, archivo):
        self.archivo = Path(archivo)

    def leer(self):
        if not self.archivo.exists():
            self.guardar([])
        try:
            with self.archivo.open("r", encoding="utf-8") as f:
                datos = json.load(f)
            return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos):
        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        temporal = self.archivo.with_suffix(self.archivo.suffix + ".tmp")
        with temporal.open("w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        temporal.replace(self.archivo)
