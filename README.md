# HolyMP3

A pocket ESP32-S3 handheld: MP3 player, WiFi tool and game player, with a 2.8" touchscreen.

> ⚠️ **Known issue in r2:** the SD finger recess on the back shell cuts through the end wall, leaving a ~34 x 8 mm opening instead of a slot. A fixed r3 is coming; don't print `back-shell-r2.stl` yet.

![HolyMP3 case](images/iso-r2.png)

## Hardware
- ESP32-S3 N16R8 dev board (both USB-C ports exposed)
- 2.8" SPI TFT with touchscreen and built-in microSD reader (ILI9341-style module)
- PCM5100/PCM5102A I2S DAC with 3.5 mm headphone jack
- Wiring on a 70 x 30 mm perfboard
- Powered over USB-C (no battery in this revision)

## Case (r2)
- 92.2 x 69.4 x 21.5 mm, two parts: back shell + front bezel
- Print in PLA without supports: shell open side up, bezel face down; 0.2 mm layers, 3 walls, 20% infill
- 4x M2.5 x 8 mm self-tapping screws from the back (low-profile heads sit flush)
- USB-C x2 and the 3.5 mm jack on one end, microSD with a finger recess on the other

| Folder | Contents |
|---|---|
| `stl/` | Print-ready meshes |
| `step/` | STEP for each part + assembly |
| `cad/` | Parametric CadQuery source (`case.py`); all dimensions in one block at the top |
| `images/` | Renders |

**Fit notes:** component dimensions are typical values, not measured. Read [FIT.md](FIT.md) and adjust the parameter block in `cad/case.py` to your boards before printing. The screen window position has the least margin. Print the shell alone first as a fit test.

## Rebuild
```bash
pip install cadquery
python cad/case.py out/
```

## Roadmap
- Battery version (LiPo + USB-C charger, about 8 mm taller)
- Pinholes for BOOT/RESET once button positions are measured
- Firmware

## License
- Code (`cad/*.py`): [MIT](LICENSE)
- 3D models, renders and docs (`stl/`, `step/`, `images/`, `*.md`): [CC BY 4.0](LICENSE-CC-BY-4.0.txt). You can share and adapt them, including commercially, as long as you credit "HolyMP3 by nsumia" and link this repo.
