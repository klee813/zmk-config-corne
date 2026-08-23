# Sol/Luna personalized Corne configuration

This branch is the locally executed implementation of the approved Corne plan. It targets a 42-key foostan Corne with nice!nano-compatible controllers and a macOS-first workflow.

## Safety status

The configuration has been compiled and the normal left/right images have been flashed and validated. The settings-reset image has not been flashed; nothing has been pushed or erased, and the existing Bluetooth pairing was preserved. The original repository commit remains available as the rollback baseline.

The 2026-08-23 Caps/OLED revision described below has been flashed to both halves and validated on the physical keyboard. No settings reset or Bluetooth bond wipe was used.

Both halves have passed independent battery power and fully wireless split operation testing. The left half is the host-facing central; the right half is a peripheral and is not expected to connect directly to the computer.

## Layer access

- `BASE`: ordinary QWERTY. Left outer keys are Tab, tap Caps Lock/hold Left Shift, and Control. Right outer keys are Backspace, apostrophe/quote, and Right Shift. Caps/Shift uses a 300 ms decision window and sends a 150 ms Caps Lock pulse for macOS.
- `NAV`: tap the left middle thumb for Escape; hold it for NAV. Q/E are left/right click; W/A/S/D move the pointer; R/F scroll vertically; T/G scroll horizontally. The right half is a conventional navigation cluster.
- `NUM`: hold the right middle thumb. The top row is 1–5 on the left and 6–0 on the right; lower rows provide symbols.
- `NPAD/SYS`: hold both middle thumbs. The left side provides output selection, five direct Bluetooth profiles, media, RGB, Codex/Hermes/dictation signals, model picker, and `/compact`; the right side is a calculator-style keypad.

The displays use named layers (`BASE`, `NAV`, `NUM`, `NPAD/SYS`) so the active layer is explicit rather than only showing a numeric index. The left/central OLED also shows `CAPS` when the host confirms Caps Lock is active. The right/peripheral OLED remains limited to split connection and battery status.

## Caps/OLED revision acceptance

The revision passed these checks on the physical keyboard:

1. Tap Caps/Shift, then type `aaa`: output is `AAA` and the left OLED shows `CAPS`.
2. Tap Caps/Shift again, then type `aaa`: output is `aaa` and the `CAPS` badge disappears.
3. Hold Caps/Shift, tap `a`, release, then type `a`: output is `Aa` without toggling Caps Lock.
4. Repeat tap and hold cases 20 times without a wrong classification or stuck Shift.
5. Tap the left middle thumb: Escape closes Raycast. Hold it: NAV remains active and emits no Escape.
6. The right OLED continues to show a clean split-connection and battery display.

Both OLEDs also passed a dedicated post-flash check: no white screen, missing-symbol squares, or corrupted Wi-Fi/battery icons. The custom left screen uses an 8192-byte LVGL pool; the simpler right screen uses 4096 bytes.

## Codex/Hermes controls

While both middle thumbs are held:

- Z emits F18: reserved for a Mac-side “focus Codex” action.
- X emits F19: reserved for focusing the approved Hermes Discord channel.
- C emits F20: configure this as Codex global Dictation Toggle, then tap once to start and tap again to stop speech-to-text at the current cursor.
- V types `/model` to open the Codex model picker without confirming a selection.
- B types `/compact` only. Press the normal Enter thumb manually after confirming the composer is empty and the chat is idle.

F18/F19/F20 are intentionally only signals. Raycast or macOS Shortcuts must be configured separately, and no action should auto-send a message.

## Build-only verification

The repository uses the current ZMK board spelling `nice_nano//zmk`, whose default revision is 2.0.0. The pinned ZMK revision is recorded in `config/west.yml`, and the reusable GitHub build workflow is pinned to the same revision.

Run the static checks with:

```sh
python3 scripts/check_keymap.py
python3 scripts/check_display_config.py LEFT_ZEPHYR_CONFIG RIGHT_ZEPHYR_CONFIG
```

The GitHub Actions workflow can build the same three artifacts from `build.yaml`. Local build artifacts are kept outside this repository; nothing has been pushed to GitHub.

## Recovery boundary

Do not flash a left image to the right half. Do not remove or insert the inter-half cable while either controller is powered. A settings reset, if later required, must be flashed deliberately to both halves and followed by forgetting/re-pairing the host Bluetooth bond.
