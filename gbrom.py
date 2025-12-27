# Reference: https://gbdev.io/pandocs/The_Cartridge_Header.html
# Accessed: 2025-12-24

import sys
from constants import *


def main():
    if len(sys.argv) < 2:
        print("No file path provided")
        exit()

    path = sys.argv[1]

    with open(path, "rb") as file:
        rom = file.read()

        print()
        print_logo(rom)
        print()
        print("Logo:                    ", "PASS" if verify_logo(rom) else "FAIL")
        print("Title:                   ", parse_title(rom))
        print("Manufacturer code:       ", parse_manufacturer_code(rom))
        print("CBG flag:                ", hexpad(parse_cgb_flag(rom)))
        print("Publisher:               ", parse_publisher(rom))
        print("SGB flag:                ", hexpad(parse_cgb_flag(rom)))
        print("Cartridge type:          ", parse_cartridge_type(rom))
        print("ROM size:                ", parse_rom_size_details(rom))
        print("RAM size:                ", parse_ram_size_details(rom))
        print("Destination code:        ", parse_destination_code(rom))
        print("Mask ROM version number: ", hexpad(parse_mask_rom_version_number(rom)))
        print("Header checksum:         ", "PASS" if verify_header_checksum(rom) else "FAIL")
        print("Global checksum:         ", "PASS" if verify_global_checksum(rom) else "FAIL")
        print()


def hexpad(value: int, pad: str = "0", width: int = 2) -> str:
    template = "0x{:" + pad + str(width) + "x}"
    return template.format(value)


def high_nibble(byte: int) -> int:
    return byte >> 4


def low_nibble(byte: int) -> int:
    return byte & 0x0F


def print_nibble(nibble: int) -> str:
    for bit_pos in range(3, -1, -1):
        print("#" if (nibble >> bit_pos) & 0x01 else " ", end="")


def print_logo(rom: bytes) -> None:
    top_half = rom[0x0104 : 0x011B + 1]
    bottom_half = rom[0x011C : 0x0133 + 1]
    for tile_row in (top_half, bottom_half):
        for row in range(4):
            for tile in range(12):
                byte_0 = tile_row[tile * 2]
                byte_1 = tile_row[tile * 2 + 1]
                if row == 0:
                    print_nibble(high_nibble(byte_0))
                if row == 1:
                    print_nibble(low_nibble(byte_0))
                if row == 2:
                    print_nibble(high_nibble(byte_1))
                if row == 3:
                    print_nibble(low_nibble(byte_1))
            print()


def verify_logo(rom: bytes) -> bool:
    return rom[0x0104 : 0x0133 + 1] == BOOTROM_LOGO


def parse_title(rom: bytes) -> str:
    return rom[0x0134 : 0x0143 + 1].decode("utf-8", errors="replace")


def parse_manufacturer_code(rom: bytes) -> str:
    code = rom[0x013F : 0x0142 + 1].decode("utf-8")
    return "N/A" if code == "\0\0\0\0" else code


def parse_cgb_flag(rom: bytes) -> int:
    return rom[0x0143]


def parse_publisher(rom: bytes) -> str:
    old_licensee_code = rom[0x014B]
    if old_licensee_code == 0x33:
        new_licensee_code = rom[0x0144 : 0x0145 + 1].decode("utf-8")
        publisher = NEW_LICENSEE_CODES.get(new_licensee_code)
        return f"'{new_licensee_code}' - {publisher}"
    publisher = OLD_LICENSEE_CODES.get(old_licensee_code)
    return f"{hexpad(old_licensee_code)} - {publisher}"


def parse_sgb_flag(rom: bytes) -> int:
    return rom[0x0146]


def parse_cartridge_type(rom: bytes) -> str:
    return CARTRIDGE_TYPES.get(rom[0x0147])


def parse_rom_size_details(rom: bytes) -> str:
    return ROM_SIZES.get(rom[0x0148])


def parse_ram_size_details(rom: bytes) -> str:
    return RAM_SIZES.get(rom[0x0149])


def parse_destination_code(rom: bytes) -> str:
    code = rom[0x014A]
    destination = DESTINATION_CODES.get(code)
    return f"{hexpad(code)} - {destination}"


def parse_mask_rom_version_number(rom: bytes) -> int:
    return rom[0x014C]


def verify_header_checksum(rom: bytes) -> bool:
    target = rom[0x014D]
    checksum = 0
    for byte in rom[0x0134 : 0x014C + 1]:
        checksum = (checksum - byte - 0x01) & 0xFF
    return checksum == target


def verify_global_checksum(rom: bytes) -> bool:
    target = rom[0x014E] << 8 | rom[0x014F]
    checksum = (sum(rom) - rom[0x014E] - rom[0x014F]) & 0xFFFF
    return checksum == target


if __name__ == "__main__":
    main()
