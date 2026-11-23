# Build report — news-image-20261122 (round 1b)

## The picture

A newspaper-style front page for Sunday 22 November 2026, drawn from
scratch by `gen_image.py` (Pillow only, no network, no clock). One
1024×1024 PNG holds all 48 stories: 2 leads, 10 briefs, a strip of 8
big numbers, a 12-pin world map, and a numbered list of the other 36.

## Why this is round 1b

Round 1 rendered fine but failed the kit's authorship check
(`thinking_reproduces` 12%, below the 30% floor, and
`thinking_revised` failed): the previous builder had copied
`gen_image.py` and `main.py` over from the 21 November entry, so most
lines counted as read rather than written. For this round both scripts
were written fresh from a blank file — new function breakdown, new
names, new layout numbers, new icon drawing — and each file was then
revised in later, separate edits (see the commit history). No file was
copied in from any other entry.

## The 48 stories

### Leads (1–2)

1. **Iran hits two US bases in Bahrain** — Iran's Revolutionary
   Guards say they hit US positions at Sheikh Isa and Juffair late on
   Saturday, in response to US drones entering Iranian airspace.
   Bahrain says a civilian industrial site caught fire; no one was
   hurt. *Fars / Bahrain govt.*
2. **Two tankers hit off Oman** — UK maritime agency UKMTO says two
   tankers were struck by unknown projectiles near Khasab on Saturday,
   one in the engine room, one in the stern. No casualties. Iran says
   a tanker hit a mine; it also claims a US MQ-9 downed.
   *UKMTO / Reuters.*

### Briefs (3–12)

3. **Russian cargo ship ablaze after drone hit** — The Sparta II,
   bound for Kaliningrad, caught fire after two drones hit it. Its 16
   crew evacuated safely. *Reuters.*
4. **Climate talks deadlocked into overtime** — Draft drops all
   fossil-fuel mentions and a $120bn target. A third draft is due
   Saturday as talks stall. *AP via Bytes Europe (COP31, Antalya).*
5. **EU mulls a Big Tech tax to fund budget** — Costa unveils a plan
   cutting €204bn from the budget, partly paid by a levy on the
   biggest digital firms. *AFP via Tech Xplore.*
6. **Bolsonaro taken to intensive care** — The jailed ex-president is
   in ICU with an acute bowel obstruction. He is stable and conscious.
   *Reuters.*
7. **Cartel violence kills 11 after kingpin arrest** — Eleven died in
   Sinaloa after troops captured cartel boss Fausto Isidro Meza
   Flores, 'El Chapo Isidro'. *Reuters.*
8. **Mamdani unveils plan to close Rikers Island** — Mayor Zohran
   Mamdani says New York will close the notorious jail 'once and for
   all', calling it a blight.
9. **India 486/4, lead 118; Pant 128 day four** — Rahul made 136 and
   Gill 98 as India took control; Pant then passed 600 with a
   day-four ton. *Cricinfo (Wellington Test).*
10. **Modi opens Nitish Setu bridge** — The PM inaugurates the
    Nitish Setu linking Patna and Vaishali in Bihar, named after
    Nitish Kumar. *The Daily Jagran.*
11. **Judge approves $7.25bn Roundup deal** — A Missouri judge
    approves Bayer's Roundup settlement; payouts of
    $10,000–$165,000 for lymphoma cases. *Reuters.*
12. **Rutte flies to Warsaw after Poland strikes** — The NATO chief
    heads to Warsaw today after Russian missiles landed in Poland;
    Tusk calls it a provocation.

### The rest of the day (13–48)

13. Estonia to shut Russia road crossings from 1 Dec.
14. Japan GDP shrinks 0.1% annualised in Q3.
15. US approved 879,000 AI chips for China in six months.
16. Trump: an Iran deal could last 20 years.
17. Zelenskyy: Crimea Bridge strikes a 'fair response'.
18. Denmark: Russia plotted to kill US-Ukrainian rapper.
19. FBI probing apparent hack of its criminal database.
20. US airlines warned of Al-Qaeda threat.
21. Third US aircraft carrier arrives in the Middle East.
22. South Africa votes; ANC fights to keep its cities.
23. Nepal PM Shah meets Modi on first bilateral visit.
24. Cyclone Akvan: 14 flights cancelled at Ranchi airport.
25. Air India extends Jeddah flight suspension to 24 Nov.
26. Prince William insures 10,000 forest workers.
27. Hegseth sets fresh limits on US-Canada defence ties.
28. South Korea: $75,000 bounty for exam-cheating tips.
29. Iran warns of 'fierce response' if its oil convoy is engaged.
30. Bahrain probes Patriot interceptor crash on Sitra Island.
31. Iran: Qeshm blasts were US munitions disposal.
32. COP31 AI pledge fails to win over major US tech firms.
33. Crude oil futures fall more than 3%.
34. Australia v England T20 series opens in Melbourne today.
35. Pat Cummins keeps Australia Test captaincy.
36. ICMR completes 100 tech transfers, signs 20 licences.
37. Trafalgar Square tree sets off from Oslo.
38. Palisades Fire: man convicted of starting the blaze.
39. Eleven killed as vehicle plunges into river in PoK.
40. France probes Depardieu over gang-rape claim.
41. Eisenkot invites Netanyahu's Likud to coalition talks.
42. Melania Trump seeks more ceasefires before Christmas.
43. Trump calls Putin a friend; Zelenskyy calls him a 'killer'.
44. EU and Indonesia sign free-trade deal after a decade.
45. Japan's pilotless air taxi completes passenger flight.
46. US Forest Service releases 1982 Bigfoot probe files.
47. Boy, 11, writes to NASA with a plan to save Hubble.
48. Anthropic shares fall a day after blockbuster IPO.

## Sources

All 48 stories were first reported 21–22 Nov 2026. Outlets: Reuters
(Sparta II, tankers, Bolsonaro, Bayer), Fars / Bahrain government
(Bahrain strikes), UKMTO (Hormuz), AP via Bytes Europe (COP31), AFP
via Tech Xplore (EU Big Tech tax), House Foreign Affairs Committee via
Reuters (879,000 AI chips), Cricinfo (Wellington Test day 3–4), Times
of India / CDS News (22 Nov front pages), The Daily Jagran (Modi,
Akvan, Prince William).

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

## Visual fixes in this round

- Lead 1's headline now shrinks to fit one line, so its body no longer
  runs into the credit line (caught on the first render of this round).
- Map labels for Warsaw and Gulf of Finland were moved apart with
  separate leader lines — the crowded Gulf/Europe cluster no longer
  collides.
- Brief bodies are capped at two lines by construction; list items are
  shrunk to fit one line each at build time.

## Checks

- `gen_image.py` run twice: byte-identical `entry.png` (1024×1024,
  PNG, under 1 MiB — see the submit log for the final sha256).
- `main.py` run twice with different `MAKEFUN_OUTPUT_DIR` values:
  identical output bytes.
- Kit check run on the exact commit to submit (see the check log);
  only `transcripts_present` may fail.


---

# Build report — news-image-20261122 (round 2)

## What changed vs round 1

Round 1 scored 0.968674 (outside the top 100; cutoff 0.987563) with
no illustrated hero at all — every top story was text only. Round 2
rebuilds the page around what the diagnosis found:

- Three large illustrated hero panels, drawn in code: Bahrain at
  night (base silhouettes, two blasts, drones, moon), the tankers off
  Oman at dusk (two hulls, fire, a spiked mine), and the Sparta II
  burning in the Gulf of Finland (containers, flames, rescue tug).
- A "THE DAY IN UTC" timeline with six moments (times marked
  approximate, with "times approximate · UTC" printed on the strip).
- Certainty tags on every hero and brief: REPORTED (confirmed by
  officials or wires), CLAIM (one side's account — the Bahrain
  strikes), FORECAST (a plan or proposal — the EU tax, the Rikers
  closure plan).
- The map is now a dot-matrix world map (continents as ellipses,
  sampled on a fixed grid) with 12 numbered pins whose labels were
  hand-placed with per-pin offsets — Wellington's label sits to the
  left of its pin, inside the frame.
- A DATE CHECK footer names the Peru M6.9 quake (20 Nov local,
  21 Nov 00:09 UTC) as deliberately left out, and says Japan's GDP
  fall and Estonia's border closure are older announcements shown as
  live follow-ups, not 22 Nov events.
- The 48 stories are unchanged from round 1 (same verified list),
  restructured as 3 heroes + 9 briefs + 36 in the list. One
  correction from fresh verification: the Sparta II was hit west of
  Gogland Island in the eastern Gulf of Finland (not just "the
  Baltic"), and its hero and pin now say so.

## Authorship

Both entrypoint files were written fresh from a blank file in this
session — new layout, new function breakdown, new names, new
illustration code — and each was then revised in later, separate
edits. No file was copied in from round 1 or any other entry.

## Visual fixes during this round

- First render: smoke ellipses and explosion bursts spilled above the
  hero panels and covered the masthead. All blast, flame and smoke
  shapes were moved and shrunk to stay inside their panels, and the
  round smoke blobs became lumpy three-ellipse puffs.
- First render: timeline times and the BY THE NUMBERS labels collided
  with the next section's title. The whole vertical budget was
  re-laid out (timeline line lower, numbers and briefs shifted down,
  map shortened to 122 px, list rows at 10.3 px).
- First render: the "GULF OF FINLAND" map label was clamped into the
  pin cluster and overlapped Warsaw. Labels now use hand-placed
  per-pin offsets and the clamp allows them just above the map box.
- Hero bodies were cut mid-sentence at two lines; they now start
  right under the headline and run to three lines, and were shortened
  to ~125–150 characters so each one ends cleanly.

## Checks

- `gen_image.py` run twice: byte-identical `entry.png` (1024×1024,
  PNG, under 1 MiB — see the verification below).
- `main.py` run twice with different `MAKEFUN_OUTPUT_DIR` values:
  identical output bytes.

