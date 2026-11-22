# Bradestudio-news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Bradestudio/Bradestudio-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Bradestudio/Bradestudio-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One picture that sums up Sunday 22 November 2026: Iran hits two US bases in Bahrain, two tankers are struck off Oman, a Russian cargo ship burns in the Baltic, and COP31 stalls into overtime — 48 verified stories on a single 1024×1024 front page.

## What is inside

- **2 lead stories** — the Bahrain strikes and the tanker attacks off Khasab.
- **10 briefs** — Sparta II ablaze, COP31 deadlock, the EU Big Tech tax, Bolsonaro in ICU, Sinaloa violence, the Rikers closure plan, India 486/4 in Wellington, the Nitish Setu bridge, Bayer's $7.25bn Roundup deal, and Rutte flying to Warsaw.
- **A "by the numbers" strip** — 2 bases, 2 tankers, 16 crew, 879,000 chips, $7.25bn, 486/4, 14 flights, 11 killed.
- **A world map** with 12 numbered pins for stories 1–12.
- **36 more stories** in a numbered list, from Estonia's border closure to Anthropic's post-IPO slide.

See [BUILD-REPORT.md](BUILD-REPORT.md) for the full list of 48 stories and their sources.

## How to run it

```sh
python3 gen_image.py   # redraw entry.png from scratch (Pillow only)
python3 main.py        # copy entry.png to the output directory
```

`main.py` writes `entry.png` to `$MAKEFUN_OUTPUT_DIR`, or to the directory passed as its first argument, or to `./output`. Run either script twice and the bytes come out identical — no network, no clock, no randomness anywhere.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qjs4e9sj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
