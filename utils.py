def hexpad(value: int, pad: str = "0", width: int = 2) -> str:
    template = "0x{:" + pad + str(width) + "x}"
    return template.format(value)
