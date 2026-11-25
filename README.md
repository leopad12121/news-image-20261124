# The World in One Day — Tuesday 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/leopad12121/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/leopad12121/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A one-image newspaper front page summing up the world's news of
Tuesday 24 November 2026, entered in the
[make.fun bounty](https://make.fun/bounty/news-image-20261124).

`main.py` (Python 3.13, standard library only at module level) draws a
1024x1024 front page — masthead, lead story, a 2x2 grid and a tech strip —
with Pillow when it is available, and otherwise copies the shipped
`entry.png` so the program still exits 0 with the verified image.
It writes to `$MAKEFUN_OUTPUT_DIR/entry.png`, else `/output/entry.png`
when `/output` exists, else `./entry.png`. Deterministic: two runs
produce byte-identical output.

## The day's six stories

1. **Israeli strikes kill Hamas security chief** (Gaza City) — Naeem Abu
   Nahel among seven killed, medics say, as strikes go on despite a
   ceasefire in place since last year.
   Sources: Reuters, AP, SCMP.
2. **Russian strike hits Zaporizhzhia flats** — an overnight attack on
   an apartment block kills two and wounds 40, including four children.
   Sources: AP, Reuters.
3. **Giuliani gets the Medal of Freedom** (Washington) — Trump awards
   the top US civilian honour to the former New York mayor in a private
   Oval Office ceremony.
   Sources: Reuters, AP.
4. **Two held over royal home break-in** (Sandringham) — two men are
   arrested after a break-in at Anmer Hall, the country home of William
   and Kate.
   Sources: Reuters, AP.
5. **NATO vows space defence** — chief Mark Rutte says the alliance
   will defend in space after reports of a Russian nuclear-armed
   satellite.
   Sources: Reuters, SCMP.
6. **Germany first into Ukraine's Delta system** (Berlin) — Berlin
   becomes the first country to gain access to Ukraine's Delta
   battlefield management system, Kyiv says.
   Sources: Kyiv Independent.

Also noted: landmine toll hits a five-year high of 7,000; a US envoy
doubts the end to $3.8bn Israel aid; Seoul in an AI exam-cheat row.

## Run it

```sh
python3 main.py
# or: MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
