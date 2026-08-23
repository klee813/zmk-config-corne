# Sol/Luna Corne

This context describes the user-facing vocabulary for a portable split keyboard that also serves as a macOS-enhanced AI control surface.

## Language

**Portable core**:
The typing, numeric, navigation, and pointer behavior expected to remain useful on every paired device.
_Avoid_: Universal layer, normal mode

**AI control surface**:
The transient keyboard mode used to steer an AI-agent conversation through focus, dictation, navigation, cancellation, and deliberate submission.
_Avoid_: Vibe layer, macro pad

**AI/NPAD layer**:
The strictly momentary dual-thumb layer that presents the AI control surface on the left half and calculator-style numeric input on the right half.
_Avoid_: NPAD/SYS, system layer

**Semantic signal**:
A stable keyboard event that represents user intent while leaving application-specific behavior to the host.
_Avoid_: App shortcut, firmware automation

**Host action**:
A Mac-side automation that translates a semantic signal according to the active application and workflow.
_Avoid_: Keymap macro, keyboard command

**Host bridge**:
The repository-owned Raycast integration that receives semantic signals and runs host actions, with licensed BetterTouchTool reserved for capabilities Raycast cannot implement reliably.
_Avoid_: BetterTouchTool preset, keyboard driver

**Automation bus**:
The contiguous F18–F24 semantic-signal vocabulary shared by the firmware and host bridge.
_Avoid_: Function-key shortcuts, macro keys

**Mac enhancement**:
An AI-oriented host action available on a configured Mac while the portable core continues to work without it on other devices.
_Avoid_: Cross-device behavior, firmware feature

**Deliberate send**:
A submission initiated by its own intentional physical press, never as the final step of a content-producing macro.
_Avoid_: Auto-send, submit macro

**Focus Codex**:
A host action that restores the existing Codex window and most recently active task without creating a task or submitting content.
_Avoid_: Open Codex, new task

**Focus Hermes**:
A host action that opens the approved Hermes Discord channel, preserves its draft, and focuses the message composer without submitting content.
_Avoid_: Open Discord, message Hermes

**Dictate**:
A single host action that toggles speech-to-text at the current text cursor regardless of whether Codex or Discord is active.
_Avoid_: Codex voice, Discord voice

**Cancel**:
A safe Escape-style dismissal for the current interface or dictation state, not a promise to interrupt a running agent.
_Avoid_: Stop agent, abort task

**Prepare compact**:
A Codex-only host action that prepares the compact command for review without submitting it.
_Avoid_: Compact, run compact

**Host HUD**:
Immediate on-screen feedback from the Mac for an AI host action, distinct from the keyboard's layer and lock-state display.
_Avoid_: OLED status, agent telemetry

**Target composer**:
The currently focused, verified text-entry surface in Codex or the approved Hermes channel where AI instructions may be prepared or submitted.
_Avoid_: Text field, active app

**Guarded action**:
A host action that verifies its target application, channel, composer focus, and required content state before acting, otherwise preserving state and reporting why it was blocked.
_Avoid_: Conditional shortcut, safe macro
