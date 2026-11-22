# Build report — news-image-20261122

## What was built

Front-page image of Sunday 22 November 2026, 48 verified stories:

- 2 leads: Iran strikes two US bases in Bahrain (IRGC claim via Fars;
  civilian industrial site on fire, no injuries); two tankers hit by
  unknown projectiles off Khasab, Oman (UKMTO, Saturday; no casualties).
- 10 briefs: Sparta II ablaze in the Gulf of Finland (16 crew evacuated,
  Finland says Ukraine likely behind it); COP31 deadlocked into overtime,
  draft drops fossil fuels; EU mulls a Big Tech tax (Costa cuts €204bn);
  Bolsonaro in ICU with acute bowel obstruction; 11 killed in Sinaloa
  after El Chapo Isidro's arrest; Mamdani unveils plan to close Rikers
  Island; India 486/4, lead 118, Pant 128 on day four in Wellington;
  Modi opens Nitish Setu (Patna–Vaishali); judge approves Bayer's $7.25bn
  Roundup settlement; Rutte flies to Warsaw after the Poland strikes.
- 36 more stories in a numbered list, from Estonia's Russia border
  closure to Anthropic shares falling after its IPO.

## Sources (all first reported 21–22 Nov 2026)

Reuters (Sparta II, tankers, Bolsonaro, Bayer), Fars / Bahrain govt
(Bahrain strikes), UKMTO (Hormuz), AP via Bytes Europe (COP31), AFP via
Tech Xplore (EU Big Tech tax), House Foreign Affairs Committee via
Reuters (879,000 AI chips), Cricinfo (Wellington Test day 3–4),
Times of India / CDS News (22 Nov front pages), The Daily Jagran
(Modi, Akvan, Prince William).

## Date care

- The Peru M6.9 quake (20 Nov local / 21 Nov 00:09 UTC) was NOT used
  as a 22 Nov story.
- Japan GDP (-0.1% annualised, Q3) is dated by its 16 Nov release;
  Estonia's border closure by its 20 Nov announcement — both are
  live follow-ups in the 22 Nov news cycle, phrased as decisions,
  not as events of the 22nd.
- The Sparta II attack happened Saturday 21 Nov and was reported
  across 22 Nov front pages; the Bahrain strikes were Saturday night,
  21→22 Nov.

## What improved vs our own 21 Nov entry

- Map pins re-spread with leader lines for the crowded Gulf/Europe
  cluster (Bahrain, Khasab, Antalya, Warsaw, Brussels, Gulf of
  Finland): labels moved to separate rows instead of only nudging pins.
- Footer date corrected to 21–22 Nov (the first render still said
  20–21 Nov; caught on visual check).
- Brief bodies trimmed to fit two lines by construction; list items
  asserted single-line at build time.

## Checks

- `gen_image.py` run twice, byte-identical `entry.png`
  (sha256 `c311069874d4ffbd7798cf20fb9f10a87e886702dd01a980a371e068334fb0b3`,
  194,414 bytes, 1024x1024, PNG).
- `main.py` run twice with `MAKEFUN_OUTPUT_DIR`: identical output bytes.
- Kit check run on the exact commit to submit (see check log).
