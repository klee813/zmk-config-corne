#!/usr/bin/env python3
"""Small, dependency-free regression checks for the Sol/Luna Corne map."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_required(path: Path, description: str) -> str:
    require(path.is_file(), f"missing {description}: {path.relative_to(ROOT)}")
    return path.read_text()


def main() -> int:
    keymap = (ROOT / "config/corne.keymap").read_text()
    config = (ROOT / "config/corne.conf").read_text()
    build = (ROOT / "build.yaml").read_text()
    west = (ROOT / "config/west.yml").read_text()
    workflow = (ROOT / ".github/workflows/build.yml").read_text()
    module = read_required(ROOT / "zephyr/module.yml", "custom OLED module metadata")
    kconfig = read_required(ROOT / "Kconfig", "custom OLED Kconfig defaults")
    cmake = read_required(ROOT / "CMakeLists.txt", "custom OLED build file")
    caps_screen = read_required(ROOT / "src/caps_status_screen.c", "custom OLED source")

    for layer in ("BASE", "NAV", "NUM", "NPAD_SYS"):
        require(re.search(rf"^\s*{layer}\s*\{{", keymap, re.MULTILINE) is not None,
                f"missing layer {layer}")
    for display_name in ("BASE", "NAV", "NUM", "NPAD/SYS"):
        require(f'display-name = "{display_name}"' in keymap,
                f"missing display name {display_name}")

    require("&to " not in keymap, "persistent layer switching (&to) is present")
    require(keymap.count("&bt BT_SEL") == 5, "expected five direct Bluetooth profile bindings")
    require("&open_model_picker" in keymap, "model picker macro is missing")
    require("&kp SLASH &kp M &kp O &kp D &kp E &kp L" in keymap,
            "model picker macro must type /model")
    require("&prepare_compact" in keymap, "compact macro is missing")
    require("caps_lock_pulse: caps_lock_pulse" in keymap,
            "macOS-safe Caps Lock pulse macro is missing")
    require("tap-ms = <150>;" in keymap,
            "Caps Lock pulse must last 150 ms for macOS")
    require("tapping-term-ms = <300>;" in keymap,
            "Caps/Shift decision window must be 300 ms")
    require("&caps_shift LSHFT 0" in keymap,
            "BASE Caps/Shift key must use the delayed Caps Lock pulse")
    require("&lt 1 ESC" in keymap,
            "BASE NAV thumb must tap Escape and hold NAV")
    require("CONFIG_ZMK_HID_INDICATORS=y" in config,
            "host Caps Lock indicators must be enabled")
    require("CONFIG_LV_USE_LABEL=y" in config,
            "custom OLED text labels must be enabled")
    require("CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y" in config,
            "custom OLED status screen must be enabled")
    require("name: zmk-vfx-sol-corne-status" in module,
            "custom OLED module metadata is missing")
    require("kconfig: Kconfig" in module,
            "custom OLED Kconfig is not registered")
    for option in ("LV_USE_THEME_MONO", "ZMK_WIDGET_LAYER_STATUS",
                   "ZMK_WIDGET_BATTERY_STATUS", "ZMK_WIDGET_OUTPUT_STATUS",
                   "ZMK_WIDGET_PERIPHERAL_STATUS"):
        require(f"imply {option}" in kconfig,
                f"custom OLED Kconfig must retain {option}")
    require("default 8192" in kconfig and "default 4096" in kconfig,
            "custom OLED must provide central and peripheral LVGL memory pools")
    require("CONFIG_LV_FONT_DEFAULT_MONTSERRAT_16=y" in config,
            "custom OLED must use the status-symbol-capable default font")
    require("src/caps_status_screen.c" in cmake,
            "custom OLED status screen is not compiled")
    require("HID_INDICATOR_CAPS_LOCK" in caps_screen and '"CAPS"' in caps_screen,
            "custom OLED screen must render the host Caps Lock state")
    require("&kp F18" in keymap and "&kp F19" in keymap and "&kp F20" in keymap,
            "Codex/Hermes automation bus signals are incomplete")
    require("6e2ef41e022d555b10f116e395832913f71717b3" in west,
            "ZMK manifest is not pinned to the approved revision")
    require("build-user-config.yml@6e2ef41e022d555b10f116e395832913f71717b3" in workflow,
            "GitHub reusable build workflow is not pinned to the manifest revision")
    require(build.count("board: nice_nano//zmk") == 3,
            "build matrix must contain left, right, and settings-reset nice_nano//zmk entries")
    require("shield: corne_left" in build and "shield: corne_right" in build
            and "shield: settings_reset" in build,
            "build matrix is missing an expected shield")

    print("PASS: Corne map, Caps pulse/OLED, tap-Esc NAV, BT profiles, automation signals, pinned workflow, and build matrix")
    return 0


if __name__ == "__main__":
    sys.exit(main())
