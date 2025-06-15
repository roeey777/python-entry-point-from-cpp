def hello(raw: bytes) -> bytes:
    print(f"Got {len(raw)} bytes!")
    print(f"They are: {raw}")
    return raw[::-1]

