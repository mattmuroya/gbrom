import sys
from constants import BOOTROM_LOGO


def main():
    if len(sys.argv) < 2:
        print("No file path provided")
        exit()

    path = sys.argv[1]

    with open(path, "rb") as file:
        rom = file.read()

        print("Logo:", "PASS" if verify_logo(rom) else "FAIL")
        print("Title:", parse_title(rom))


def verify_logo(rom: bytes) -> bool:
    return rom[0x0104 : 0x0133 + 1] == BOOTROM_LOGO


def parse_title(rom: bytes) -> str:
    return rom[0x134 : 0x143 + 1].decode("utf-8")


if __name__ == "__main__":
    main()
