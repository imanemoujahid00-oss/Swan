# Brand v2 — Complete colour replacement list

All 94 distinct old CSS hex values were removed from old theme token definitions and/or replaced in declarations with the entries below. The only remaining literal CSS colours are the requested palette in the canonical root token block. `#e4e1db` is also an old value, but remains valid as the requested new `--line` definition.

| Old hex | Replacement for direct declarations |
| --- | --- |
| `#000` | `var(--ink)` |
| `#0006` | `color-mix(in srgb, var(--ink) 40%, transparent)` |
| `#142b20` | `var(--ink)` |
| `#173c2c18` | `color-mix(in srgb, var(--accent-purple) 9%, transparent)` |
| `#191919` | `var(--ink)` |
| `#19402e` | `var(--plum)` |
| `#211410` | `var(--ink)` |
| `#235447` | `var(--focus)` |
| `#285a41` | `var(--hover)` |
| `#30271f` | `var(--ink)` |
| `#304330` | `var(--ink)` |
| `#342631` | `var(--ink)` |
| `#34263122` | `color-mix(in srgb, var(--ink) 13%, transparent)` |
| `#41594b` | `var(--ink)` |
| `#454725` | `var(--hover)` |
| `#47243a` | `var(--hover)` |
| `#49322528` | `color-mix(in srgb, var(--accent-purple) 16%, transparent)` |
| `#52324512` | `color-mix(in srgb, var(--accent-purple) 7%, transparent)` |
| `#60394f` | `var(--plum)` |
| `#626262` | `var(--muted)` |
| `#62632f` | `var(--plum)` |
| `#667f6e` | `var(--control)` |
| `#675346` | `var(--muted)` |
| `#695562` | `var(--muted)` |
| `#7faf88` | `var(--peach)` |
| `#847858` | `var(--control)` |
| `#894975` | `var(--focus)` |
| `#8a263d` | `var(--accent-red)` |
| `#92908d` | `var(--control)` |
| `#9e7d91` | `var(--control)` |
| `#a5c8a4` | `var(--peach)` |
| `#a73729` | `var(--focus)` |
| `#aa3426` | `var(--hover)` |
| `#b99b80` | `var(--peach)` |
| `#ba977c` | `var(--peach)` |
| `#c34432` | `var(--plum)` |
| `#c4d4c4` | `var(--line)` |
| `#c8ad93` | `var(--peach)` |
| `#c8e457` | `var(--accent-red)` |
| `#c9dec0` | `var(--peach)` |
| `#c9dec040` | `color-mix(in srgb, var(--peach) 25%, transparent)` |
| `#d2c4b1` | `var(--line)` |
| `#d7513d` | `var(--plum)` |
| `#dbece6` | `var(--peach)` |
| `#dce8d9` | `var(--peach)` |
| `#decbbc` | `var(--peach)` |
| `#dfccd5` | `var(--line)` |
| `#dfeddb` | `var(--peach)` |
| `#e0ecda` | `var(--peach)` |
| `#e4dfc9` | `var(--peach)` |
| `#e4e1db` | `var(--line)` |
| `#e7efdf` | `var(--peach)` |
| `#e9e6de88` | `color-mix(in srgb, var(--line) 53%, transparent)` |
| `#e9e7e3` | `var(--line)` |
| `#e9e7e4` | `var(--line)` |
| `#e9f2cb` | `var(--peach)` |
| `#ead4e3` | `var(--blush)` |
| `#eae9d6` | `var(--peach)` |
| `#ece4d5` | `var(--canvas)` |
| `#ede7d6` | `var(--canvas)` |
| `#edf3e5` | `var(--peach)` |
| `#edf3e6` | `var(--peach)` |
| `#eeded1` | `var(--blush)` |
| `#eee2d3` | `var(--blush)` |
| `#eee4d3` | `var(--peach)` |
| `#eee7d8` | `var(--canvas)` |
| `#eeece8` | `var(--canvas)` |
| `#f0e5e9` | `var(--blush)` |
| `#f0e7d7` | `var(--peach)` |
| `#f0f4e9` | `var(--canvas)` |
| `#f3e5eb` | `var(--blush)` |
| `#f5d4c1` | `var(--peach)` |
| `#f5d8c6` | `var(--peach)` |
| `#f5eaf0` | `var(--blush)` |
| `#f5eddf` | `var(--blush)` |
| `#f5f2ed` | `var(--canvas)` |
| `#f6dacf` | `var(--peach)` |
| `#f6e4ed` | `var(--blush)` |
| `#f6f3eb` | `var(--canvas)` |
| `#f8e2d4` | `var(--peach)` |
| `#f8f7f3` | `var(--canvas)` |
| `#f9fcf5` | `var(--paper)` |
| `#faf0f4` | `var(--blush)` |
| `#fbf6f2` | `var(--canvas)` |
| `#fcf0e8` | `var(--peach)` |
| `#ff634d` | `var(--plum)` |
| `#ff6d55` | `var(--plum)` |
| `#ff785f` | `var(--plum)` |
| `#ff826b` | `var(--hover)` |
| `#fff` | `var(--paper)` |
| `#fff5f1` | `var(--blush)` |
| `#fffaed` | `var(--paper)` |
| `#fffaf7` | `var(--blush)` |
| `#fffdfa` | `var(--paper)` |

Named CSS `white` becomes `var(--paper)`; named CSS `black` becomes `var(--ink)`, including gradient masks. No old RGB/RGBA literals existed. Transparent gradient stops remain transparent.

All previous assignments to `--canvas`, `--paper`, `--ink`, `--muted`, `--plum`, `--hover`, `--blush`, `--peach`, `--line`, `--control` and `--focus` were replaced by the single requested palette. The existing additional aliases `--coral` and `--lime` point to `--accent-red`. Radius, grid and image asset variables are preserved.

Final presentation rules set primary actions and selected controls to red, primary hover to `--hover`, small product labels and secondary shopping links to purple, secondary highlights to pale blue, supporting text to `--muted`, and errors to the darker `--hover` colour for small-text contrast.
