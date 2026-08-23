# AI control surface v1.1 specification

Status: approved design; not implemented

## Goal

Extend the validated Sol/Luna Corne into a macOS-enhanced AI control surface while preserving its portable typing, numeric, navigation, pointer, Bluetooth, OLED, and Caps Lock behavior. The primary loop is Codex voice interaction, followed by Hermes voice interaction, Codex typed prompts, generic dictation, and Hermes typed prompts.

## Product boundary

- `BASE`, `NAV`, and `NUM` remain the portable core and must not change behavior.
- `AI/NPAD` is a strictly momentary layer active only while both middle thumbs are held.
- AI behavior is Mac-enhanced. On other paired devices, semantic signals may be unused but must not cause harmful behavior.
- Firmware emits stable semantic signals. A repository-owned Raycast extension translates them into guarded host actions.
- Licensed BetterTouchTool is a fallback only when a Raycast action fails the written reliability gate.
- The keyboard OLED shows `AI/NPAD`; live agent state remains a truthful event-based Mac HUD rather than keyboard telemetry.

## AI/NPAD keymap

The left half becomes:

| Position | Outer | Q/A/Z column | W/S/X column | E/D/C column | R/F/V column | T/G/B column |
| --- | --- | --- | --- | --- | --- | --- |
| Top | Cancel | BT 1 | BT 2 | BT 3 | BT 4 | BT 5 |
| Home | Deliberate Send | Previous | Volume Down | Play/Pause | Volume Up | Next |
| Bottom | Output Toggle | Focus Codex | Focus Hermes | Dictate | Model Picker | Prepare Compact |

The right half retains the currently validated calculator-style numpad without behavioral changes.

The RGB toggle is removed from daily key access. RGB remains off by default to prioritize battery life.

## Automation bus

| Signal | Meaning | Owner |
| --- | --- | --- |
| F18 | Focus Codex | Raycast |
| F19 | Focus Hermes | Raycast |
| F20 | Dictate | Existing Codex global Dictation Toggle; Raycast must not bind F20 |
| F21 | Deliberate Send | Raycast |
| F22 | Cancel | Raycast |
| F23 | Model Picker | Raycast |
| F24 | Prepare Compact | Raycast |

The Raycast extension exposes seven named no-view commands for a complete semantic vocabulary, but its Dictate command has no F20 hotkey. The physical F20 path remains directly owned by the already validated global Dictation Toggle.

## Host bridge

The local Raycast extension is stored in this repository and imported from source. It owns shared application detection, target-composer discovery, safety guards, HUD feedback, and testable decision logic.

The extension must not contain credentials, browser cookies, local license data, private messages, machine-specific absolute paths, or exported accessibility databases. A macOS setup guide must document required Raycast hotkeys and user-granted Accessibility/Automation permissions.

### Focus Codex

- Activate the existing application identified by bundle ID `com.openai.codex`.
- Restore the existing window and most recently active task.
- Place the cursor in the current composer.
- Never create a task or submit content.
- Show the event HUD `CODEX` after successful focus.

### Focus Hermes

- Target Chrome and the exact channel URL `https://discord.com/channels/1500874976410996886/1501230163860394167`.
- Activate an existing matching tab without reloading it; open the URL in Chrome only when no matching tab exists.
- Focus the accessible composer named `Message #war-room`.
- Preserve any existing draft and never submit it.
- Show the event HUD `HERMES` after successful focus.

### Dictate

- F20 continues to invoke the validated global Dictation Toggle directly.
- One physical action starts or stops speech-to-text at the current text cursor in Codex or Discord.
- Raycast must not claim F20 or present unverifiable persistent `LISTENING`/`STOPPED` state.
- Event feedback, when shown, is `DICTATE`.

### Deliberate Send

- Operate only when the target composer is focused in Codex or the exact Hermes channel.
- Require non-empty composer content.
- Submit only the existing content; never add text before submission.
- If the composer is empty, preserve state and show `NOTHING TO SEND`.
- If the target, channel, or composer cannot be verified, preserve state and show `SEND BLOCKED`.

### Cancel

- Produce safe Escape-style behavior in any active application.
- Close or dismiss the current picker, overlay, Raycast surface, or dictation UI when that application supports Escape.
- Do not promise to interrupt or terminate a running agent.
- Show the event HUD `CANCEL` only when doing so does not interfere with Escape delivery.

### Model Picker

- Operate only in Codex with the target composer focused and empty.
- Prepare `/model` without selecting a model or submitting content.
- If a draft is present, preserve it and show `DRAFT NOT EMPTY`.
- If Codex or its composer cannot be verified, preserve state and show `MODEL BLOCKED`.

### Prepare Compact

- Operate only in Codex with the target composer focused and empty.
- Prepare `/compact` without pressing Enter.
- Do not attempt unreliable agent-running detection; the user remains responsible for confirming that the task is idle.
- If a draft is present, preserve it and show `DRAFT NOT EMPTY`.
- If Codex or its composer cannot be verified, preserve state and show `COMPACT BLOCKED`.
- Show `COMPACT READY` after successful preparation.

## BetterTouchTool fallback

Do not bind an automation-bus signal in both Raycast and BetterTouchTool. A BetterTouchTool fallback may be added for one host action only after the Raycast version fails that action's reliability gate. The fallback and its exclusive hotkey ownership must be documented, then tested against the same criteria.

## Implementation plan

1. Update the ZMK layer name, left-half mappings, automation-bus signals, comments, README, and dependency-free regression checks. Preserve the other layers and the entire right-half numpad contract.
2. Build a local Raycast extension with seven named no-view commands, shared target detection, guarded-action decisions, Mac adapters, event HUDs, and automated tests. Leave F20 unbound in Raycast.
3. Add a macOS setup guide covering local extension import, F18/F19/F21–F24 hotkeys, the existing F20 Dictation Toggle, required permissions, Chrome/Hermes prerequisites, verification, rollback, and the BetterTouchTool fallback rule.
4. Produce left, right, and settings-reset build artifacts through CI, but do not flash the keyboard or reset Bluetooth settings.
5. Perform the human acceptance matrix. Add a BetterTouchTool fallback only for an action that fails its reliability gate, then repeat that matrix.

## Automated passing criteria

- [ ] Existing keymap and display regression checks pass.
- [ ] Regression checks assert `AI/NPAD`, the exact F18–F24 meanings, five direct Bluetooth profiles, removal of raw `/model` and `/compact` firmware macros, and removal of the RGB key binding.
- [ ] `BASE`, `NAV`, `NUM`, Caps/Shift, tap-Escape/hold-NAV, OLED widgets, central/peripheral roles, Bluetooth profiles, and right-half numpad behavior remain unchanged.
- [ ] GitHub Actions builds left, right, and settings-reset artifacts from the pinned ZMK revision.
- [ ] The Raycast extension installs dependencies reproducibly and passes its build, lint, type, and unit-test commands.
- [ ] Unit tests cover every guarded action across correct target, wrong app, wrong channel, missing composer, empty composer, non-empty draft, and action-adapter failure states.
- [ ] Tests prove that blocked actions preserve composer content and never invoke submission.
- [ ] No automation-bus hotkey is owned by both Raycast and BetterTouchTool.
- [ ] No credential, private message, browser state, license, or machine-specific absolute path is committed.

## Human passing criteria

- [ ] Focus Codex succeeds 20/20 times, restoring the current task and focusing its composer within one second.
- [ ] Focus Hermes succeeds 20/20 times with the matching Chrome tab already open, without reload or draft loss, focusing `Message #war-room` within one second.
- [ ] Focus Hermes succeeds 10/10 times when it must open the approved channel URL.
- [ ] F20 starts and stops dictation at the current cursor in both Codex and Hermes without a conflicting Raycast binding.
- [ ] Deliberate Send submits a non-empty draft in Codex and Hermes only after its own physical press.
- [ ] Empty, wrong-app, wrong-channel, and unfocused-composer Send attempts produce zero submissions and truthful blocked feedback.
- [ ] Model Picker prepares `/model` only in an empty Codex composer and never selects or submits.
- [ ] Prepare Compact prepares `/compact` only in an empty Codex composer and never submits.
- [ ] Model Picker and Prepare Compact preserve non-empty drafts and show `DRAFT NOT EMPTY`.
- [ ] Cancel safely dismisses Raycast and Codex pickers/overlays while ordinary tap-Escape behavior remains available.
- [ ] OLED displays `AI/NPAD`; Caps Lock, layer, output, split connection, and battery displays remain correct.
- [ ] The right-half numpad passes the existing calculator input test unchanged.
- [ ] There are zero accidental sends, draft losses, stuck layers, Bluetooth bond wipes, or settings resets during validation.

## Release and deployment boundary

- The physically validated firmware commit `b9de8408b43c898592a76950f02ad1815e6e4f69` is the immutable v1.0.0 baseline.
- v1.1 implementation is build-only until a human reviews filenames and checksums and explicitly performs each flash.
- An implementation agent must never flash either half, flash settings-reset, wipe Bluetooth bonds, merge its own implementation, or modify Mac permissions automatically.

## References

- [Vibe Coding Keyboard video](https://www.youtube.com/watch?v=8iwU9pEj7Fs)
- [Reference keyboard source](https://github.com/WellsWang/vckb)
- [Raycast local extension workflow](https://developers.raycast.com/basics/create-your-first-extension)
- [Raycast hotkeys](https://manual.raycast.com/command-aliases-and-hotkeys)
- [Raycast HUD API](https://developers.raycast.com/api-reference/feedback/hud)
