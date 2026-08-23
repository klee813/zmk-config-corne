#!/usr/bin/env python3
"""Validate the resolved display configuration for both Corne halves."""

from pathlib import Path
import sys


def read_config(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if line.startswith("CONFIG_") and "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
        elif line.startswith("# CONFIG_") and line.endswith(" is not set"):
            values[line[2 : -11]] = "n"
    return values


def require(config: dict[str, str], key: str, expected: str, half: str) -> None:
    actual = config.get(key, "missing")
    if actual != expected:
        raise SystemExit(f"FAIL: {half} {key} expected {expected}, got {actual}")


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_display_config.py LEFT_CONFIG RIGHT_CONFIG")

    left = read_config(Path(sys.argv[1]))
    right = read_config(Path(sys.argv[2]))

    for half, config in (("left", left), ("right", right)):
        require(config, "CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM", "y", half)
        require(config, "CONFIG_LV_USE_THEME_MONO", "y", half)
        require(config, "CONFIG_LV_FONT_DEFAULT_MONTSERRAT_16", "y", half)
        require(config, "CONFIG_LV_FONT_MONTSERRAT_16", "y", half)
        require(config, "CONFIG_ZMK_WIDGET_BATTERY_STATUS", "y", half)
    left_pool_size = int(left.get("CONFIG_LV_Z_MEM_POOL_SIZE", "0"))
    if left_pool_size < 8192:
        raise SystemExit(
            "FAIL: left CONFIG_LV_Z_MEM_POOL_SIZE expected >=8192 for the extra Caps widget, "
            f"got {left_pool_size}"
        )

    right_pool_size = int(right.get("CONFIG_LV_Z_MEM_POOL_SIZE", "0"))
    if right_pool_size < 4096:
        raise SystemExit(
            f"FAIL: right CONFIG_LV_Z_MEM_POOL_SIZE expected >=4096, got {right_pool_size}"
        )

    require(left, "CONFIG_ZMK_WIDGET_OUTPUT_STATUS", "y", "left")
    require(left, "CONFIG_ZMK_WIDGET_LAYER_STATUS", "y", "left")
    require(left, "CONFIG_ZMK_HID_INDICATORS", "y", "left")

    require(right, "CONFIG_ZMK_WIDGET_PERIPHERAL_STATUS", "y", "right")

    print("PASS: both resolved Corne display configurations retain their required widgets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
