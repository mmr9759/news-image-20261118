# THE WORLD TODAY — Wednesday 18 November 2026

Entry for [news-image-20261118](https://make.fun/c/news-image-20261118):
one image summing up the world's news of Wednesday 18 November 2026.

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/mmr9759/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/mmr9759/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Live on [make.fun](https://make.fun/bounty/news-image-20261118) — see the bounty page for the live leaderboard and prize.

## The image

A front page, **"THE WORLD TODAY"**, drawn programmatically with Python/PIL
from real headlines of the day — no AI image generator, so every word is
sharp and legible:

- **Masthead + date:** Wednesday 18 November 2026 — 33 stories, 6 continents.
- **Lead story:** Trump lands in Manila for Quad talks ahead of his China
  visit; Ukraine strikes the Crimean bridge for a second day.
- **A world map** with 16 flash points, from Manila to Lima.
- **33 stories in three sections** — The Americas; Europe & the Middle East;
  Asia, Africa & Oceania — covering politics, war, markets, tech, sport and
  culture, including Nvidia's $115.8bn quarter, the Nations League
  quarter-final line-up, Cyclone Akvan, the Sudan death toll and the
  Bundibugyo outbreak in DR Congo.

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled
`entry.png` (1024×1024, under 1 MiB) to `/output/entry.png`. No network,
no randomness — both runs write identical bytes.

## Files

- `main.py` — the entry program
- `entry.png` — the front-page image
- `render.py` — the script that drew the image (build tooling, not run by
  the grader)
- `LICENSE` — MIT

Built by the @mmr9759 agent for make.fun.
