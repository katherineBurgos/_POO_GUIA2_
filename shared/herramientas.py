import locale


def _limpiar_texto(texto):
    texto = str(texto)
    encoding = locale.getpreferredencoding(False) or "utf-8"
    return texto.encode(encoding, errors="replace").decode(encoding)


def imprimir_titulo(titulo):
    titulo = _limpiar_texto(titulo)
    print("\n" + "=" * 60)
    print(f"{titulo:^60}")
    print("=" * 60)


def imprimir_exito(mensaje):
    print(f"[OK] {_limpiar_texto(mensaje)}")


def imprimir_error(mensaje):
    print(f"[ERROR] {_limpiar_texto(mensaje)}")


def imprimir_info(mensaje):
    print(f"[INFO] {_limpiar_texto(mensaje)}")


def confirmar(pregunta):
    pregunta = _limpiar_texto(pregunta)
    while True:
        respuesta = input(f"{pregunta} (s/n): ").strip().lower()
        if respuesta in ("s", "si", "yes", "y"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Respuesta inválida. Escriba 's' para sí o 'n' para no.")
