# GB ROM Analyzer

CLI tool for decoding header data from Game Boy cartridge (ROM) files. Displays
cartridge metadata and performs boot logo/checksum validation.

Developed in reference to the
[cartridge header documentation](https://gbdev.io/pandocs/The_Cartridge_Header.html)
from the [Pan Docs](https://gbdev.io/pandocs/) maintained by the
[gbdev.io](https://gbdev.io/) Game Boy development community.

## Usage

```
$ python3 ./gbrom.py ./path/to/rom.gb
```

## Sample output

```
Logo:                     PASS
Title:                    TETRIS
Manufacturer code:        N/A
CBG flag:                 0x00
Publisher:                0x01 - Nintendo
SGB flag:                 0x00
Cartridge type:           ROM ONLY
ROM size:                 32 KiB - 2 ROM banks (no banking)
RAM size:                 0 - No RAM
Destination code:         0x00 - Japan (+ Overseas)
Mask ROM version number:  0x01
Header checksum:          PASS
Global checksum:          PASS
```

## Notes on boot logo

The Nintendo logo that displays when you turn on the Game Boy is hard-encoded
into the internal system
[boot ROM](https://codeberg.org/ISSOtm/gb-bootroms/src/commit/2dce25910043ce2ad1d1d3691436f2c7aabbda00/src/dmg.asm#L256-L269).
Game cartridges include a copy of this logo inside the header at memory at
address `0x0104` - `0x0133`. The boot ROM instructs the system to verify that
the cartridge logo matches the internal system logo, serving as a
legal/licensing validation.

The logo is represented by two rows of 12 4x4-pixel tiles. Each tile is encoded
using two bytes.

```
+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |   |   |  <-- Bytes 0x0104 - 0x011B (two bytes per tile)
+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |   |   |  <-- Bytes 0x011C - 0x0133 (two bytes per tile)
+---+---+---+---+---+---+---+---+---+---+---+---+
```

The first byte for each tile represents the top two pixel rows; each row four
bits across from MSB to LSB. The second byte represents the bottom two pixel
rows.

For example, the first two bytes of the sequence starting at memory address
`0x0104` are `0xCE` and `0xED`. Together, they encode the first 4x4-pixel tile:

```
0x0104: 0xCE = 0b11001110
0x0105: 0xED = 0b11101101

+---+---+---+---+
| 1 | 1 | 0 | 0 |  <-- High nibble (first four bits) of first byte (0xC)
+---+---+---+---+
| 1 | 1 | 1 | 0 |  <-- Low nibble (last four bits) of first byte (0xE)
+---+---+---+---+
| 1 | 1 | 1 | 0 |  <-- High nibble of second byte (0xE)
+---+---+---+---+
| 1 | 1 | 0 | 1 |  <-- Low nibble of second byte (0xD)
+---+---+---+---+
```

The resulting image of all 24 tiles (two rows of 12) looks like this (where 1 =
'#' and 0 = ' '):

```
##   ## ##                             ##         <--+
###  ## ##        ##                   ##            |
###  ##          ####                  ##            | Top tile row
## # ## ## ## ##  ##  ####  ## ##   #####  ####   <--+
## # ## ## ### ## ## ##  ## ### ## ##  ## ##  ##  <--+
##  ### ## ##  ## ## ###### ##  ## ##  ## ##  ##     | Bottom tile row
##  ### ## ##  ## ## ##     ##  ## ##  ## ##  ##     |
##   ## ## ##  ## ##  ##### ##  ##  #####  ####   <--+
```

More info:

-   [Pan Docs cartridge header documentation](https://gbdev.io/pandocs/The_Cartridge_Header.html#0104-0133--nintendo-logo)
-   [Disassembled Game Boy boot Rom source code](https://codeberg.org/ISSOtm/gb-bootroms/src/commit/2dce25910043ce2ad1d1d3691436f2c7aabbda00/src/dmg.asm#L256-L269)
-   [The Ultimate Game Boy Talk (YouTube video, timestamp 19:16)](https://youtu.be/HyzD8pNlpwI?si=t9YxNPQtvHEwPMvb&t=1156)
