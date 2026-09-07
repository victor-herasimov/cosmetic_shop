def read_secret(secret_name: str) -> str | None:
    try:
        with open(f"/run/secrets/{secret_name}", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
