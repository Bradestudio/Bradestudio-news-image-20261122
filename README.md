# Bradestudio-news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Bradestudio/Bradestudio-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Bradestudio/Bradestudio-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One picture that sums up Sunday 22 November 2026: Iran hits two US bases in Bahrain, two tankers are struck off Oman, the Sparta II burns in the Gulf of Finland, and COP31 stalls into overtime — 48 verified stories on a single 1024×1024 front page.

## What is inside (round 2)

- **3 illustrated hero panels** — the Bahrain strikes at night, the tankers off Oman at dusk, the Sparta II ablaze in the Gulf of Finland — each drawn from scratch with Pillow shapes.
- **A "THE DAY IN UTC" timeline** — six moments of the day, times marked approximate.
- **A "BY THE NUMBERS" strip** — 2 bases, 2 tankers, 879,000 chips, $7.25bn, 11 killed, $120bn, 10,000 workers.
- **9 briefs with drawn thumbnails** — COP31, the EU Big Tech tax, Bolsonaro, Sinaloa, Rikers, Wellington, Nitish Setu, Roundup, Rutte — each tagged REPORTED, CLAIM or FORECAST.
- **A dot-matrix world map** with 12 numbered pins for stories 1–12 (Wellington's label sits inside the frame, and every Gulf label was hand-placed so none overlaps another).
- **36 more stories** in a numbered list, from Estonia's border closure to Anthropic's post-IPO slide.
- **A DATE CHECK footer** — the Peru quake (20 Nov) is named as deliberately left out, with a certainty legend and the source line.

See [BUILD-REPORT.md](BUILD-REPORT.md) for the full list of 48 stories, their sources, and what changed in round 2.

## How to run it

```sh
python3 gen_image.py   # redraw entry.png from scratch (Pillow only)
python3 main.py        # draw entry.png into the output directory
```

`main.py` writes `entry.png` to `$MAKEFUN_OUTPUT_DIR`, or to the directory passed as its first argument, or to `./output`. Run either script twice and the bytes come out identical — no network, no clock, no randomness anywhere.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qjs4e9sj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
