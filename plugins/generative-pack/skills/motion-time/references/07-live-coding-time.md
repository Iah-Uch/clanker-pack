# Live coding and time as material

Verified against each repo on 2026-10-15.

## Principle

When timing is the medium, code is the instrument. Patterns and loops are edited while they run.

## Sonic Pi (sonic-pi-net/sonic-pi)

- License and status: GitHub reports no classification, 12k stars, last push Oct 2026. The LICENSE file is multi-part: the main source (the `app/` directory except `app/web/`) is MIT; other parts have their own terms.
- Technique: a complete open-source programming environment for writing music as code, live, aimed to be simple, joyful and powerful.
- Mechanism (literature; I did not read the source): code runs in loops on separate threads that advance a virtual clock with `sleep`; sound events are sent to the audio engine with a timestamp slightly in the future, so playback timing does not depend on how fast the code runs. Editing a loop takes effect on its next iteration.
- Reach for it when: you want to learn or teach live-coded music, or prototype rhythm and sequencing ideas quickly.
- Watch out: read the LICENSE section for each directory before reusing anything outside `app/`.

## Tidal Cycles (tidalcycles/Tidal)

- License and status: GPL-3.0. The GitHub repo is archived; development moved to Codeberg (`uzu/tidal`).
- Technique: described in its repo as a pattern language. I did not read further than the README, which only carries the move notice and license.
- Watch out: its README states that ports and projects using Tidal source as a reference for algorithms or types are derivative works bound by the same license. Use it as a tool; do not port its code or algorithms.
