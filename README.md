# World News — 24 November 2026

This repository holds one 1024×1024 PNG poster that sums up the world news of **24 November 2026**. The date names the day in the largest type on the page, and beneath it the day's most consequential stories are laid out across six continents and several fields: Ukrainian sea drones sinking the Russian corvette *Merkury* at Benghazi, Russian refineries burning after Putin's vow of retaliation, the EU's 22nd sanctions package and NATO's AWACS deployment to Poland, COP31 closing in Antalya with no deal, Nvidia reinstating Jensen Huang as chief executive, a magnitude 7.6 earthquake and tsunami warning off Aomori, and a confectionery-factory fire in Banten that killed 24. Short labels and flat pictograms let a reader who missed the day follow each story, and an "ALSO TODAY" strip carries eight further briefs.

`main.py` is the standard-library-only entrypoint: it copies the committed `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`) byte-identically, refusing a missing or oversized source. `make_image.py` drew `entry.png` at build time with Pillow, asserting that every text run stays inside its card, that no run overlaps another run or a pictogram, and that no type falls below 19 px; the grader never runs it.

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/friederickemiddleton7/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/friederickemiddleton7/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

[![license: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Run: `MAKEFUN_OUTPUT_DIR=out python3 main.py`

Bounty page: https://make.fun/bounty/news-image-20261124
