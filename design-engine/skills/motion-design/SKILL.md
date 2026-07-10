---
name: motion-design
description: Design and apply the brand's motion language — duration/easing tokens, signature animations, choreography, and reduced-motion policy. Use when defining motion for a brand, adding animation to surfaces, or auditing existing motion for consistency.
---

# Motion Design

Motion is a brand voice with physics. This skill owns the `motion` (and
glow/pulse parts of `elevation`) sections of `design-engine/brand.json`
and their application.

## The token contract
- `--dur-fast` (~80–120ms): state feedback — hovers, presses, toggles.
- `--dur-base` (~150–250ms): element transitions — reveals, fades, moves.
- `--dur-slow` (~200–400ms): spatial changes — panels, accordions.
- `--dur-drift` (500ms+): one signature ambient move, used at most once
  per view (a hero glow, an equalizer settle). This is where brand
  personality lives; everything else is utility.
- Easings: `--ease-standard` for most things; `--ease-enter`
  (decelerate) for things appearing; `--ease-exit` (accelerate) for
  things leaving; `--ease-spring` sparingly, for delight moments.
- Never a literal `0.15s` in component CSS — that's what the tokens are
  for, and what makes retuning the whole brand's tempo a one-line change.

## Principles
1. **Causality first.** Animate to show where something came from or what
   triggered it. If removing the animation loses no information and no
   affect, remove it.
2. **Enter slow, exit fast.** Things appearing can take `--dur-base`;
   things leaving should get out of the way in `--dur-fast`.
3. **Distance scales duration.** Small elements move on fast/base; large
   surfaces on slow. Nothing the user is waiting on may animate longer
   than base.
4. **One conductor per view.** Stagger related items (30–60ms steps), do
   not fire everything at once; but only one orchestrated sequence per
   page load.
5. **Reduced motion is a first-class theme.** The engine collapses
   `--dur-*` to 0ms under `prefers-reduced-motion` (and hosts typically
   also kill animations wholesale). Design so the zero-motion experience
   is complete: no information or state may exist only mid-animation.

## Method
- Defining: set durations/easings in brand.json → `tokens_build` emits
  them → demo on `tools/specimen.py`'s motion cards → operator gate.
- Applying: replace literal durations with tokens as you touch surfaces;
  keyframe animations belong in the host's component CSS but must take
  their timing from the tokens.
- Auditing: grep surfaces for `transition:` / `animation:` literals;
  report drift as a count, reduce it monotonically.
